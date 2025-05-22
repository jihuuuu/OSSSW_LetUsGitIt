import { useEffect, useState } from "react";
import { getNotesByPage, updateNote } from "../services/note";
import { NoteAccordionList } from "../components/NoteAccordionList";
import PaginationComponent from "../components/PaginationComponent";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "../components/ui/sheet";
import Logo from "../components/ui/logo"; // ✅ 빠졌던 로고 import
import type { Note } from "@/types/note"; 
import { Input } from "@/components/ui/input"

function NotePage() {
  const [notes, setNotes] = useState<any[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedNote, setSelectedNote] = useState<any>(null);
  const [editedNote, setEditedNote] = useState<any>(null);
  const [search, setSearch] = useState("");
  const [keyword, setKeyword] = useState("");

  const size = 10;

  const loadNotes = async (page: number) => {
    const { notes, totalPages } = await getNotesByPage(page, size);
    setNotes(notes);
    setTotalPages(totalPages);
  };

  useEffect(() => {
    loadNotes(currentPage);
  }, [currentPage]);

  const handleSelect = (note: any) => {
    setSelectedNote(note);
    setEditedNote({ ...note });
  };

  const handleSave = async () => {
    await updateNote(editedNote.id, {
      title: editedNote.title,
      content: editedNote.content,
    });
    alert("노트 수정 완료!");
    setSelectedNote(null);
    loadNotes(currentPage);
  };

  return (
    <>
      <div className="min-h-screen flex flex-col">
        {/* ✅ 좌우 분할 구조 */}
        <div className="flex flex-1">
          {/* ✅ 왼쪽 로고 영역 */}
          <div className="w-[200px] p-6 border-r flex flex-col items-center">
            <Logo />
          </div>

          {/* ✅ 오른쪽 메인 콘텐츠 */}
          <div className="flex-1 px-16 py-20 relative">
            <h1 className="text-2xl font-bold mb-10 text-center">NOTE</h1>

            {/* ✅ 검색 input */}
             <div className="mb-6 max-w-md mx-auto">
          <Input
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSearch();
              }
            }}
            placeholder="검색어를 입력하세요"
            className="border rounded-full px-4 py-2 w-full"
          />
        </div>

            {/* ✅ 노트 리스트 */}
            <div className="w-full max-w-2xl mx-auto space-y-4 mb-12">
              <NoteAccordionList notes={notes} onSelect={handleSelect} />
            </div>

            {/* ✅ 페이지네이션 */}
            <div className="flex justify-center">
              <PaginationComponent
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            </div>
          </div>
        </div>
      </div>

      {/* ✅ 오른쪽 수정 패널 */}
      {selectedNote && (
        <Sheet open={true}>
          <SheetContent>
            <SheetHeader className="mb-4">
              <SheetTitle>노트 수정</SheetTitle>
            </SheetHeader>
            <div className="flex flex-col gap-4">
              <input
                type="text"
                className="border p-2 rounded w-full"
                value={editedNote?.title || ""}
                onChange={(e) =>
                  setEditedNote((prev: any) => ({
                    ...prev,
                    title: e.target.value,
                  }))
                }
              />
              <textarea
                className="border p-2 rounded w-full h-40 resize-none"
                value={editedNote?.content || ""}
                onChange={(e) =>
                  setEditedNote((prev: any) => ({
                    ...prev,
                    content: e.target.value,
                  }))
                }
              />
            </div>
            <SheetFooter className="mt-6 flex justify-between">
              <button
                onClick={() => setSelectedNote(null)}
                className="text-sm text-gray-500"
              >
                CLOSE
              </button>
              <button
                onClick={handleSave}
                className="bg-primary text-primary-foreground px-4 py-2 rounded"
              >
                SAVE
              </button>
            </SheetFooter>
          </SheetContent>
        </Sheet>
      )}
    </>
  );
}

export default NotePage;
