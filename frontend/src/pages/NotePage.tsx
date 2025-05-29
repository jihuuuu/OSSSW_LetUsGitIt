import { useEffect, useState } from "react";
import { getNotesByKeyword, getNotesByPage, updateNote } from "../services/note";
import { NoteAccordionList } from "../components/NoteAccordionList";
import PaginationComponent from "../components/PaginationComponent";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "../components/ui/sheet";
import Logo from "../components/ui/logo";
import type { Note } from "@/types/note";
import { Input } from "@/components/ui/input";
import Header from "@/components/Header";
import { getArticlesByNoteId } from "@/services/note"; // ✅ 연관 기사 가져오는 서비스
import type { Article } from "@/types/article";
import NoteEditSheet from "@/components/NoteEditSheet";

export default function NotePage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [editedNote, setEditedNote] = useState<Note | null>(null);
  const [relatedArticles, setRelatedArticles] = useState<Article[]>([]);
  const [keyword, setKeyword] = useState("");

  const size = 10;

const mapNote = (note: any): Note => ({
  id: Number(note.note_id),          // ✅ id를 number로 변환
  title: note.title,
  text: note.text ?? "",             // 혹시 없으면 기본값
  createdAt: note.created_at,        // ✅ createdAt으로 변환
});

const loadNotes = async (page: number) => {
  const res = await fetch(
    `http://localhost:8000/users/notes?keyword=${encodeURIComponent(keyword)}&page=${page}&size=10&_=${Date.now()}`
  );
  const data = await res.json();
  const rawNotes = data.result.notes || [];
  setNotes(rawNotes.map(mapNote)); // ✅ 변환 후 저장
};

  useEffect(() => {
  loadNotes(currentPage);
}, [currentPage, keyword]);

  const handleSelect = async (note: Note) => {
  try {
    setSelectedNote(note);
    setEditedNote({ ...note });
    const articles = await getArticlesByNoteId(Number(note.id));
    setRelatedArticles(articles);
  } catch (err) {
    console.error("❌ 노트 기사 조회 중 오류:", err);
    alert("노트에 연결된 기사를 불러올 수 없습니다.");
  }
};


  const handleSave = async () => {
    if (!editedNote) return;
    await fetch(`http://localhost:8000/users/notes/${editedNote.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: editedNote.title,
      content: editedNote.text,
    }),
  });
    alert("노트 수정 완료!");
    setSelectedNote(null);
    loadNotes(currentPage);
  };

  const handleSearch = () => {
    setCurrentPage(1);
    loadNotes(1);
    setSelectedNote(null);
    setEditedNote(null);
    setRelatedArticles([]);
  };

  return (
    <>
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">NOTE</h1>
        <div className="px-2 py -1">
          <Header />
        </div>
      </header>

      <main className="min-h-screen px-6 py-10 pr-[400px] flex flex-col items-center">
        <div className="w-full max-w-4xl bg-[#ebf2ff] rounded-lg p-10 flex flex-col items-center gap-6">
          <p className="text-gray-500 text-center text-[16px]">
            노트 제목을 입력하세요
          </p>
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

        <div className="w-full max-w-2xl space-y-4 my-12">
          <NoteAccordionList notes={notes} onSelect={handleSelect} />
        </div>

        <div className="flex justify-center">
          <PaginationComponent
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      </main>

      <NoteEditSheet
      open={!!selectedNote}
      note={editedNote}
      articles={relatedArticles}
      onClose={() => {
        setSelectedNote(null);
        setEditedNote(null);
        setRelatedArticles([]);
      }}
      onChange={(updated) => setEditedNote(updated)}
      onSave={handleSave}
/>

    </>
  );
}