import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { Star } from "lucide-react";

interface Article {
  id: number;
  title: string;
  link: string;
}

interface ClusterDetail {
  cluster_id: number;
  keywords: string[];
  articles: Article[];
}

export default function ClusterDetailPage() {
  const { clusterId } = useParams();
  const [cluster, setCluster] = useState<ClusterDetail | null>(null);
  const [favorites, setFavorites] = useState<Set<number>>(new Set());
  const [loadingIds, setLoadingIds] = useState<Set<number>>(new Set());

  const [noteMode, setNoteMode] = useState(false);
  const [selectedArticles, setSelectedArticles] = useState<Set<number>>(new Set());
  const [isNoteModalOpen, setIsNoteModalOpen] = useState(false);
  const [noteContent, setNoteContent] = useState("");

  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
    /*// 더미 데이터로 초기화 (서버 연결 전)
    const dummyCluster: ClusterDetail = {
      cluster_id: 1,
      keywords: ["OOO", "전 대통령", "공판 출석"],
      articles: [
        {
          article_id: 12,
          title: "'내란혐의' OOO 첫 법원 공개출석...포토라인 말없이 통과",
          link: "http://www.dyenews.co.kr/news/articleView.html?idxno=801677",
        },
        {
          article_id: 9,
          title: "예시예시 '피그마' 예시",
          link: "http://www.news.co.kr/news/example",
        },
      ],
    };
    const dummyScrapIds = [12];
    setCluster(dummyCluster);
    setFavorites(new Set(dummyScrapIds));*/

    // 서버 연결 시 주석 해제
     axios.get(`http://localhost:8000/clusters/today/${clusterId}/articles`).then((res) => {
    setCluster(res.data);
  });

  axios
    .get("http://localhost:8000/users/scraps", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
    .then((res) => {
      const ids = res.data.articles.map((a: any) => Number(a.article_id || a.id)); // ✅ ID로만 추출
      setFavorites(new Set(ids)); // ✅ 상태에 저장
    })
    .catch((err) => {
      console.error("스크랩 기사 로딩 실패:", err);
    });
}, [clusterId]);

  const handleScrap = async (articleId: number) => {
  if (loadingIds.has(articleId)) return;

  setLoadingIds((prev) => new Set(prev).add(articleId));
  const isScrapped = favorites.has(articleId);

  try {
    const url = `http://localhost:8000/users/articles/${articleId}/${isScrapped ? "unscrap" : "scrap"}`;
    const method = isScrapped ? "put" : "post";

    const res = await axios({
      method,
      url,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (res.data?.isSuccess) {
      setFavorites((prev) => {
        const updated = new Set(prev);
        isScrapped ? updated.delete(articleId) : updated.add(articleId);
        return updated;
      });
    } else {
      console.error("스크랩 응답 실패:", res.data?.message);
    }
  } catch (err) {
    console.error("스크랩 요청 실패:", err);
  } finally {
    setLoadingIds((prev) => {
      const updated = new Set(prev);
      updated.delete(articleId);
      return updated;
    });
  }
};

  const submitNote = async () => {
    const res = await axios.post(
      "http://localhost:8000/users/notes",
      {
        articleIds: Array.from(selectedArticles),
        text: noteContent,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );
    console.log("노트 응답:", res.data); // 👈 이거 추가!
    
    if (res.data?.isSuccess) {
      alert("노트가 저장되었습니다.");
      setIsNoteModalOpen(false);
      setSelectedArticles(new Set());
      setNoteContent("");
      setNoteMode(false);
    } else {
      alert("노트 저장 실패: " + (res.data?.message || "알 수 없는 오류"));
    }
    
  };

  return (
    <div className="min-h-screen bg-white relative">
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">오늘의 이슈 10</h1>
      </header>

      <main className="max-w-4xl mx-auto p-6">
        {cluster ? (
          <>
            <h2 className="text-center text-2xl font-bold my-6">
              {cluster.keywords.join(" ")}
            </h2>

            <div className="bg-gray-50 border rounded-md p-4 shadow">
              <p className="font-semibold text-lg mb-4">관련기사</p>
              <ul className="divide-y divide-gray-200">
                {cluster.articles.map((article) => (
                  <li
                    key={article.id}
                    className="py-4 flex justify-between items-start gap-4"
                  >
                    <div className="flex flex-col text-left flex-1">
                      {noteMode && (
                        <input
                          type="checkbox"
                          checked={selectedArticles.has(article.id)}
                          onChange={(e) => {
                            setSelectedArticles((prev) => {
                              const updated = new Set(prev);
                              e.target.checked
                                ? updated.add(article.id)
                                : updated.delete(article.id);
                              return updated;
                            });
                          }}
                          className="mb-1"
                        />
                      )}
                      <p className="text-sm mb-1">• {article.title}</p>
                      <a
                        href={article.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-600 break-all"
                      >
                        {article.link}
                      </a>
                    </div>

                    <button onClick={() => handleScrap(article.id)}>
                      <Star
                        className={`w-5 h-5 mt-1 ${
                          favorites.has(article.id)
                            ? "text-yellow-400 fill-current"
                            : "text-gray-300"
                        }`}
                      />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </>
        ) : (
          <p className="text-center text-gray-500 mt-20">불러오는 중...</p>
        )}
      </main>

      {/* 우측 하단 고정 버튼 */}
      <div className="fixed bottom-6 right-6 z-[9999]">
        {noteMode ? (
          <button
            onClick={() => setIsNoteModalOpen(true)}
            className="px-4 py-2 bg-sky-500 text-white rounded-full shadow"
          >
            note
          </button>
        ) : (
          <button
            onClick={() => setNoteMode(true)}
            className="w-12 h-12 rounded-full border text-2xl shadow"
          >
            ✏️
          </button>
        )}
      </div>

      {/* 노트 작성 모달 */}
      {isNoteModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-md shadow-lg w-96">
            <h2 className="text-lg font-bold mb-2">노트 작성</h2>
            <textarea
              rows={5}
              className="w-full border rounded p-2 mb-4"
              placeholder="노트 내용을 입력하세요"
              value={noteContent}
              onChange={(e) => setNoteContent(e.target.value)}
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsNoteModalOpen(false)}
                className="text-sm text-gray-500"
              >
                취소
              </button>
              <button
                onClick={submitNote}
                className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
              >
                저장
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}