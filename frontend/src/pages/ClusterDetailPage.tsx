import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { Star } from "lucide-react";
import Header from "@/components/Header";
import { useNavigate } from "react-router-dom";

import type { Article } from "@/types/article";
import { useAuth } from "@/context/AuthContext";
// import needed functions or objects from articleUtils, e.g.:
import { getSelectedArticles, addSelectedArticle, removeSelectedArticle } from "@/utils/selectedArticles";
import { getScrappedArticles, addScrappedArticle, removeScrappedArticle } from "@/utils/scrapArticles";
import useLogoutWatcher from "@/hooks/useLogoutWatcher";
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
  const { isLoggedIn, accessToken, login } = useAuth();

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) login(token);
  }, []);

  useLogoutWatcher();


  useEffect(() => {
    axios.get(`http://localhost:8000/clusters/today/${clusterId}/articles`).then((res) => {
      setCluster(res.data);
    });

  const fetchData = async () => {
    try {
      const res = await axios.get("http://localhost:8000/users/scraps", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const ids = res.data.articles.map((a: any) =>
        Number(a.article_id || a.id)
      );

      const localScraps = getScrappedArticles();
      const merged = new Set([...ids, ...localScraps]);

      setFavorites(merged);
    } catch (err) {
      console.error("스크랩 기사 로딩 실패:", err);
    }
  };

  fetchData();
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
          if (isScrapped) {
          updated.delete(articleId);
          removeScrappedArticle(articleId);
          } else {
          updated.add(articleId);
          addScrappedArticle(articleId);
    }
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

  const indexOfLast = currentPage * articlesPerPage;
  const indexOfFirst = indexOfLast - articlesPerPage;
  const currentArticles = cluster?.articles.slice(indexOfFirst, indexOfLast) || [];
  const totalPages = cluster ? Math.ceil(cluster.articles.length / articlesPerPage) : 0;
  
const navigate = useNavigate();

const handleCreateNotePage = () => {
  const selectedIds = getSelectedArticles();

  if (selectedIds.length === 0) {
    alert("기사를 선택해주세요.");
    return;
  }

  const selected = cluster?.articles.filter((a) => selectedIds.includes(a.id)) || [];

  const defaultText = selected
    .map((a) => `• ${a.title}\n${a.link}`)
    .join("\n\n");

  navigate("/note/new", {
    state: {
      defaultText,
      articles: selected,
    },
  });
};
  return (
     <div className="min-h-screen flex flex-col  justify-start">
              <Header />
      <main className="w-[90%] mx-auto p-6">
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
                        <label className="flex items-center mb-1">
                          <input
                            type="checkbox"
                            checked={selectedArticles.has(article.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                addSelectedArticle(article.id);
                              } else {
                                removeSelectedArticle(article.id);
                              }
                              setSelectedArticles((prev) => {
                                const updated = new Set(prev);
                                e.target.checked
                                  ? updated.add(article.id)
                                  : updated.delete(article.id);
                                return updated;
                              });
                            }}
                            className="w-5 h-5 mb-1"
                          />
                        </label>
                      )}
                      <p
                        onClick={() => window.open(article.link, "_blank")}
                        className="text-base font-medium text-black-700 hover:underline cursor-pointer mb-1"
                      >
                        {article.title}
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
  {isLoggedIn ? (
    noteMode ? (
      <div className="flex items-center">
        <button
          onClick={handleCreateNotePage}
          className="px-4 py-2 bg-sky-500 text-white rounded-full shadow"
        >
          🆕 새 노트 생성
        </button>
        <button
          className="ml-2 px-3 py-2 rounded bg-green-500 text-white text-sm"
          onClick={() => {
            const selectedIds = getSelectedArticles();
            const selected = cluster?.articles.filter((a) =>
              selectedIds.includes(a.id)
            );
            navigate("/users/notes", {
              state: { mode: "select-note", newArticles: selected },
            });
          }}
        >
          ➕ 기존 노트에 추가
        </button>
        <button
          className="px-4 py-2 bg-yellow-300 text-white rounded-full shadow text-sm"
          onClick={() => {
            setNoteMode(false);
            setSelectedArticles(new Set());
            getSelectedArticles().forEach((id) =>
              removeSelectedArticle(id)
            );
          }}
        >
          ❌ 취소
        </button>
      </div>
    ) : (
      <button
        onClick={() => setNoteMode(true)}
        className="w-12 h-12 rounded-full border text-2xl shadow"
      >
        ✏️
      </button>
    )
  ) : (
    <button
      onClick={() => navigate("/login")}
      className="px-4 py-2 bg-blue-500 text-white rounded-full shadow"
    >
      📝 로그인 후 사용가능
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