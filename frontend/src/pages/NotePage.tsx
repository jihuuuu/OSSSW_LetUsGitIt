// src/pages/NotePage.tsx
import { useEffect, useState } from "react";
import { getAllNotes, updateNote } from "../services/note";
import { Button } from "../components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "../components/ui/sheet";
import { Separator } from "../components/ui/separator";
import { X } from "lucide-react";
import Logo from "../components/ui/logo";

function NotePage() {
  const [notes, setNotes] = useState<any[]>([]);
  const [selectedNote, setSelectedNote] = useState<any>(null);
  const [editedNote, setEditedNote] = useState<any>(null);

  useEffect(() => {
    getAllNotes().then(setNotes);
  }, []);

  const handleSelect = (note: any) => {
    setSelectedNote(note);
    setEditedNote({ ...note });
  };

  const handleSave = async () => {
    if (!editedNote) return;
    try {
      await updateNote(editedNote.id, {
        title: editedNote.title,
        content: editedNote.content,
      });
      alert("노트 수정 완료!");
      setSelectedNote(null);
      const updated = await getAllNotes();
      setNotes(updated);
    } catch {
      alert("수정 실패");
    }
  };

  return (
    <>
      <div className="min-h-screen flex flex-col">
        {/* 상단 영역 */}
        <div className="flex flex-1">
          {/* 왼쪽 로고 영역 */}
          <div className="w-[200px] p-6 border-r flex flex-col items-center">
            <Logo />
          </div>

          {/* 메인 콘텐츠 */}
          <div className="flex-1 px-16 py-20 relative">
            <h1 className="text-2xl font-bold mb-10 text-center">NOTE</h1>
            <div className="mb-6 max-w-md mx-auto">
              <input
                type="text"
                placeholder="검색어를 입력하세요"
                className="border rounded-full px-4 py-2 w-full"
              />
            </div>

            {/* 노트 리스트 */}
            <div className="w-full max-w-2xl mx-auto space-y-4 mb-32">
              {notes.map((note, idx) => (
                <div
                  key={idx}
                  onClick={() => handleSelect(note)}
                  className="bg-gray-100 hover:bg-gray-200 p-4 rounded-lg cursor-pointer"
                >
                  <div className="font-bold">{note.title}</div>
                  <div className="text-sm text-gray-600">
                    {note.content?.slice(0, 80)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ✅ 페이지네이션: 고정 위치 */}
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex gap-2 text-sm text-gray-600">
          <Button variant="outline">← Previous</Button>
          <Button className="bg-blue-500 text-white">1</Button>
          <Button variant="outline">2</Button>
          <Button variant="outline">3</Button>
          <Button variant="outline">Next →</Button>
        </div>
      </div>

      {/* 사이드 시트 - 오른쪽 오버레이 */}
      {selectedNote && (
        <Sheet open={true}>
          <SheetContent
            className="fixed right-0 top-0 h-screen w-[400px] bg-white shadow-lg z-50 p-0"
            showCloseButton={false}
          >
            <SheetHeader className="flex items-start pl-6 pr-3 pt-3 pb-4 border-none">
              <div className="flex items-start justify-between w-full">
                <SheetTitle className="flex-1 mt-3 text-lg font-semibold text-[#49454f]">
                  <input
                    className="w-full outline-none"
                    value={editedNote?.title}
                    onChange={(e) =>
                      setEditedNote({ ...editedNote, title: e.target.value })
                    }
                  />
                </SheetTitle>
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-12 h-12 rounded-full"
                  onClick={() => setSelectedNote(null)}
                >
                  <X className="w-6 h-6" />
                </Button>
              </div>
            </SheetHeader>

            <div className="flex-1 w-full px-6 py-4">
              <textarea
                className="w-full h-full resize-none border border-gray-300 p-2 rounded"
                value={editedNote?.content}
                onChange={(e) =>
                  setEditedNote({ ...editedNote, content: e.target.value })
                }
              />
            </div>

            <div className="w-full">
              <Separator className="w-full" />
              <SheetFooter className="flex justify-start gap-2 p-6 pt-4">
                <Button
                  className="h-10 px-6 py-2.5 bg-[#77aafb] text-white rounded-full"
                  onClick={handleSave}
                >
                  Save
                </Button>
                <Button
                  variant="outline"
                  className="h-10 px-6 py-2.5 border-[#79747e] text-[#77aafb] rounded-full"
                  onClick={() => setSelectedNote(null)}
                >
                  Cancel
                </Button>
              </SheetFooter>
            </div>
          </SheetContent>
        </Sheet>
      )}
    </>
  );
}

export default NotePage;
