// src/pages/NotePage.tsx

import { useEffect, useState } from "react";
import { NoteAccordionList } from "../components/NoteAccordionList";
import PaginationComponent from "../components/PaginationComponent";
import Logo from "../components/ui/logo";
import Header from "@/components/Header";
import { Input } from "@/components/ui/input";
import { useNavigate, useLocation } from "react-router-dom";
import api from "@/services/api";
import { getNotesByKeyword, getNotesByPage } from "@/services/note";
import type { Note } from "@/types/note";

export default function NotePage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [keyword, setKeyword] = useState("");
  const navigate = useNavigate();
  const location = useLocation();
  const incomingArticles = location.state?.newArticles || [];

  const size = 10;

  const loadNotes = async () => {
    try {
      const { notes, totalPages } = await getNotesByPage(currentPage, size);
      setNotes(notes.filter((n) => n.state !== false)); // 소프트 삭제된 것 제외
      setTotalPages(totalPages);
    } catch (err) {
      console.error("노트 로딩 실패:", err);
    }
  };

  useEffect(() => {
    loadNotes();
  }, [currentPage, keyword]);

  const handleSearch = async () => {
    try {
      const { notes, totalPages } = await getNotesByKeyword(keyword, currentPage, size);
      setNotes(notes.filter((n) => n.state !== false)); // 소프트 삭제된 것 제외
      setTotalPages(totalPages);
    } catch (err) {
      console.error("노트 로딩 실패:", err);
    }
    setCurrentPage(1); // 키워드 바뀌면 1페이지로 초기화
  };

  const handleSelect = (note: Note) => {
    navigate(`/notes/${note.id}/edit`, {
    state: {
      note,
      newArticles: incomingArticles,
    },
  });
  };

  const handleDelete = async (noteId: number) => {
    const confirmDelete = window.confirm("정말 이 노트를 삭제하시겠습니까?");
    if (!confirmDelete) return;

    try {
      const res = await api.put(`/users/notes/${noteId}`, {
        state: false, // 소프트 삭제
      });

      if (res.data.isSuccess) {
        alert("삭제되었습니다.");
        loadNotes();
      } else {
        alert("삭제 실패: " + (res.data.message || "알 수 없는 오류"));
      }
    } catch (err) {
      alert("삭제 중 오류 발생");
      console.error(err);
    }
  };

  return (
    <>
      <div className="min-h-screen flex flex-col justify-start">
            <header className="h-25 bg-blue-500 text-white px-6 flex items-center justify-between mb-20">
              <div className="flex items-center">
                <Logo />
              </div>
              <div className="px-2 py -1">
                <Header />
              </div>
            </header>

      <main className="min-h-screen flex flex-col items-center">
        <div className="w-full max-w-4xl bg-[#ebf2ff] rounded-lg p-10 flex flex-col items-center gap-6">
          <p className="text-gray-500 text-center text-[16px]">노트 제목을 입력하세요</p>
          <div className="flex w-full max-w-sm items-center gap-2">
            <Input
              placeholder="예: AI 기사 요약"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="border rounded-full px-4 py-2 w-full"
            />
          </div>
        </div>

        <div className="w-full space-y-4 my-12">
          <NoteAccordionList
            notes={notes}
            onSelect={handleSelect}
            onDelete={handleDelete}
          />
        </div>

        <div className="flex justify-center">
          <PaginationComponent
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      </main>
      </div>
    </>
  );
}
