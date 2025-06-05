import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import PaginationComponent from "@/components/PaginationComponent";
import Logo from "@/components/ui/logo";
import Header from "@/components/Header";
import api from "@/services/api"; //  axios 인스턴스 import
import { addSelectedArticle, getSelectedArticles, removeSelectedArticle } from "@/utils/selectedArticles";
type Article = {
  id: number;
  title: string;
  link: string;
  published: string;
};

export default function ScrapbookPage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [keyword, setKeyword] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [noteMode, setNoteMode] = useState(false);
  const [selectedArticles, setSelectedArticles] = useState<Set<number>>(new Set());

  const location = useLocation();
  const mode = location.state?.mode;
  const originNoteId = location.state?.originNoteId;
  const preselected = location.state?.selectedArticles || [];


  const fetchScrapArticles = async () => {
    try {
      const res = await api.get("/users/scraps", {
        params: {
          title: keyword,
          page,
          size: 10,
        },
      });
      setArticles(res.data.articles);
      setTotalPages(res.data.totalPages);
    } catch (err) {
      console.error("스크랩 기사 로딩 실패:", err);
    }
  };

  useEffect(() => {
    fetchScrapArticles();
    // 초기 상태 설정
    const localSelected = getSelectedArticles();
    setSelectedArticles(new Set(localSelected));
    if (mode === "edit-note") {
    setNoteMode(true);
    setSelectedArticles(new Set(preselected.map((a: Article) => a.id)));
  }
  }, [page]);

  const handleSearch = () => {
    setPage(1);
    fetchScrapArticles();
  };
  const navigate = useNavigate();

const handleCreateNotePage = () => {
  const selected = Array.from(selectedArticles)
    .map((id) => articles.find((a) => a.id === id))
    .filter((a): a is Article => !!a);

  if (selected.length === 0) {
    alert("기사를 1개 이상 선택해주세요.");
    return;
  }
  if (location.state?.mode === "edit-note") {
    navigate(`/note/${location.state.originNoteId}/edit`, {
      state: {
        newArticles: selected,
      },
    });
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
      {/* 상단 헤더 */}
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="px-2 py-1">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">SCRAPBOOK</h1>
        <div className="px-2 py-1">
          <Header />
        </div>
      </header>

      {/*  본문 */}
      <main className="px-6 py-10 flex flex-col items-center">
        <div className="w-full max-w-4xl bg-[#ebf2ff] rounded-lg p-10 flex flex-col items-center gap-6">
          <p className="text-gray-500 text-center text-[16px]">
            기사 제목을 입력하세요
          </p>
          <div className="flex w-full max-w-sm items-center gap-2">
            <Input
              placeholder="예: 남지수"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <Button onClick={handleSearch}>Submit</Button>
          </div>
        </div>

        <div className="w-full max-w-4xl mt-10 space-y-2">
          {articles.map((a) => (
  <div key={a.id} className="flex items-start gap-2">
    {noteMode && (
      <input
        type="checkbox"
        checked={selectedArticles.has(a.id)}
        onChange={(e) => {
          setSelectedArticles((prev) => {
            const updated = new Set(prev);
            if (e.target.checked) {
          updated.add(a.id);
          addSelectedArticle(a.id); // ✅ 로컬 반영
          } else {
          updated.delete(a.id);
          removeSelectedArticle(a.id); // ✅ 로컬 반영
      }
            return updated;
          });
        }}
      />
    )}

    <a
      href={a.link}
      target="_blank"
      rel="noopener noreferrer"
      className="text-blue-600 hover:underline"
    >
      {a.title}
    </a>
  </div>
))}
        </div>

        <div className="mt-8">
          <PaginationComponent
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </div>

  {/* Sticky note button */}
            <div className="sticky bottom-4 flex justify-end pr-4 mt-6">
              {noteMode ? (
                <button
                  onClick={handleCreateNotePage}
                  className="px-4 py-2 bg-sky-500 text-white rounded-full shadow"
                  >
                    {mode === "edit-note" ? "➕ 현재 노트에 추가" : "note"}
              </button>
              ) : (
            <div className="flex items-center">
            <button
            onClick={() => setNoteMode(true)}
            className="w-12 h-12 rounded-full border text-2xl shadow"
        >
      ✏️
      </button>
  {/* 기존 noteMode와 별도로 새로운 버튼 */}
    <button
    className="ml-2 px-3 py-2 rounded bg-green-500 text-white text-sm"
    onClick={() => {
      const selectedIds = getSelectedArticles();
      const selected = articles.filter((a) =>
        selectedIds.includes(a.id)
      );
      navigate("/notes", {
        state: { newArticles: selected },
      });
    }}
  >
    ➕ 기존 노트에 추가
  </button>
</div>
              )}
            </div>
      </main>
    </div>
  );
}