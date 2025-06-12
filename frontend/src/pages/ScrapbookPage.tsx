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
  {/* 🧠 선택된 기사 배열 */}
  const selected = articles.filter((a) =>
    getSelectedArticles().includes(a.id)
  );

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
        tempTitle: localStorage.getItem("tempNoteTitle"),
        tempText: localStorage.getItem("tempNoteText"),
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
    <div>
      {/* 상단 헤더 */}
      <header className="mb-10">
                    <Header />
      </header>

      {/*  본문 */}
      <main className="w-[80%]  mx-auto flex flex-col items-center">
        <div className="w-full max-w-4xl bg-[#ebf2ff] rounded-lg p-10 flex flex-col items-center gap-6">
          <p className="text-gray-500 text-center text-[16px]">
            기사 제목을 입력하세요
          </p>
          <div className="flex w-full max-w-sm items-center gap-2">
            <Input
              placeholder="예: AI"
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
        className="w-5 h-5 mb-1"
      />
    )}

    <a
      href={a.link}
      target="_blank"
      rel="noopener noreferrer"
      className="text-blue-600 text-lg hover:underline"
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
            {/* 🧩 하단 통합 버튼 영역 */}
<div className="sticky bottom-4 flex justify-end pr-4 mt-6 space-x-2">

  {/* ✏️ 체크박스 모드 진입 */}
  {!noteMode && (
    <button
      onClick={() => setNoteMode(true)}
      className="w-12 h-12 rounded-full border text-2xl shadow"
    >
      ✏️
    </button>
  )}

  {/* 🆕 새 노트 생성 */}
  {noteMode && mode !== "edit-note" && (
    <button
      className="px-4 py-2 bg-blue-500 text-white rounded-full shadow text-sm"
      onClick={() => {
        if (selected.length === 0) {
          alert("기사를 선택해주세요.");
          return;
        }

        const defaultText = selected
          .map((a) => `• ${a.title}\n${a.link}`)
          .join("\n\n");

        navigate("/note/new", {
          state: { defaultText, articles: selected },
        });
      }}
    >
      🆕 새 노트 생성
    </button>
  )}

  {/* 📌 기존 노트에 추가 */}
  {noteMode && mode!=="edit-note" &&(
    <button
      className="px-4 py-2 bg-green-500 text-white rounded-full shadow text-sm"
      onClick={() => {
        if (selected.length === 0) {
          alert("기사를 선택해주세요.");
          return;
        }

        navigate("/users/notes", {
          state: { mode: "select-note", newArticles: selected },
        });
      }}
    >
      ➕ 기존 노트에 추가
    </button>
  )}

  {/* ❌ 체크박스 모드 종료 */}
   {noteMode && mode !== "edit-note" && (
    <button
      className="px-4 py-2 bg-yellow-300 text-white rounded-full shadow text-sm"
      onClick={() => {
        setNoteMode(false);
        setSelectedArticles(new Set()); // 선택 해제
        // 모든 선택된 기사 id를 로컬 저장소에서 제거
        getSelectedArticles().forEach((id) => removeSelectedArticle(id));
      }}
    >
      ❌ 취소
    </button>
  )}

  {/* 🔄 현재 편집 중인 노트에 추가 (edit-note 모드일 때만) */}
  {noteMode && mode === "edit-note" && (
    <button
      onClick={handleCreateNotePage}
      className="px-4 py-2 bg-sky-500 text-white rounded-full shadow text-sm"
    >
      ➕ 현재 노트에 추가
    </button>
  )}

</div>
      </main>
    </div>
  );
}