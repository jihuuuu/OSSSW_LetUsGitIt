import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import type { Note } from "@/types/note";
import { useNavigate } from "react-router-dom";
import { Pencil } from "lucide-react";

type NoteAccordionListProps = {
  notes: Note[];
  onSelect: (note: Note) => void | Promise<void>;
  onDelete?: (id: Note["id"]) => void | Promise<void>;
};

function formatDate(isoString: string) {
  const date = new Date(isoString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}
export function NoteAccordionList({ notes, onSelect, onDelete }: NoteAccordionListProps) {
  const navigate = useNavigate();
  return (
    <div className="w-full max-w-3xl mx-auto font-sans text-base"> {/* ✅ 통일된 너비 + 폰트 */}
      <Accordion type="single" collapsible className="w-full">
  {notes.map((note) => (
    <AccordionItem key={note.id} value={`note-${note.id}`} className="mb-4">
      <AccordionTrigger>
        <div className="flex flex-col text-left w-full">
          <span className="font-semibold">{note.title}</span>
          <span className="text-sm text-gray-500">{note.createdAt}</span>
        </div>
      </AccordionTrigger>
      <AccordionContent>
        <p className="whitespace-pre-wrap mb-4">{note.text}</p>
        <div className="flex gap-2 justify-end">
           <button
                onClick={async () => {
                  console.log("편집하려는 note id:", note.id); // ← 이거 찍어보세요
                  await onSelect(note);               // ✅ 노트 선택 처리 먼저
                  navigate(`/note/${note.id}/edit`, {
                state: {
                newArticles: [], // ✅ 최소한 빈 배열이라도 넘겨야 병합 useEffect가 안전하게 동작함
  },
});  // ✅ 그 후에 이동
          }}
            className="text-sm text-blue-500 hover:underline"
            >
           편집
          </button>
          {onDelete && (
            <button
              className="px-3 py-1 rounded bg-red-500 text-white text-sm"
              onClick={() => onDelete(note.id)}
            >
              삭제
            </button>
          )}
        </div>
      </AccordionContent>
    </AccordionItem>
  ))}
</Accordion>

    </div>
  );
}
