import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { Star } from "lucide-react";
import Header from "@/components/Header";
import { useNavigate } from "react-router-dom";

import type { Article } from "@/types/article";

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

  const [currentPage, setCurrentPage] = useState(1);
  const articlesPerPage = 10;

  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
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
        const ids = res.data.articles.map((a: any) => Number(a.article_id || a.id));
        setFavorites(new Set(ids));
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
          Authorization: `Bearer accessToken`,
        },
      }
    );

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

  const indexOfLast = currentPage * articlesPerPage;
  const indexOfFirst = indexOfLast - articlesPerPage;
  const currentArticles = cluster?.articles.slice(indexOfFirst, indexOfLast) || [];
  const totalPages = cluster ? Math.ceil(cluster.articles.length / articlesPerPage) : 0;
  
const navigate = useNavigate();
const handleCreateNotePage = () => {
  const selected = Array.from(selectedArticles)
    .map((id) => cluster?.articles.find((a) => a.id === id))
    .filter((a): a is Article => !!a);

  if (selected.length === 0) {
    alert("기사를 1개 이상 선택해주세요.");
    return;
  }

  const defaultText = selected
    .map((article) => `• ${article.title}\n${article.link}`)
    .join("\n\n");

  navigate("/note/new", {
    state: {
      defaultText,
      articles: selected,
    },
  });
};
  return (
    <div className="min-h-screen bg-white">
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">오늘의 이슈 10</h1>
        <div className="px-2 py -1">
                  <Header />
                </div>
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
                {currentArticles.map((article) => (
                  <li key={article.id} className="py-4 flex justify-between items-start gap-4">
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
                      <p
                        onClick={() => window.open(article.link, "_blank")}
                        className="text-sm font-medium text-blue-700 hover:underline cursor-pointer mb-1"
                      >
                        • {article.title}
                      </p>

                      <a
                        href={article.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-500 break-all"
                      >
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

              {/* Pagination (Prev / Next only) */}
              {totalPages > 1 && (
                <div className="flex justify-center mt-6 gap-4 items-center">
                  <button
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 bg-white border rounded disabled:opacity-40"
                  >
                    Prev
                  </button>
                  <span className="text-sm text-gray-600">
                    Page {currentPage} of {totalPages}
                  </span>
                  <button
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 bg-white border rounded disabled:opacity-40"
                  >
                    Next
                  </button>
                </div>
              )}
            </div>

            {/* Sticky note button */}
            <div className="sticky bottom-4 flex justify-end pr-4 mt-6">
              {noteMode ? (
                <button
                  onClick={handleCreateNotePage}
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
          </>
        ) : (
          <p className="text-center text-gray-500 mt-20">불러오는 중...</p>
        )}
      </main>

      
    </div>
  );
}