import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import type { Note } from "@/types/note"; // 이미 있을 수 있음
import { useNavigate } from "react-router-dom"; // ✅ useNavigate 추가

type NoteAccordionListProps = {
  notes: Note[];
  onSelect: (note: Note) => void | Promise<void>; // ✅ async도 허용
};

function formatDate(isoString: string) {
  const date = new Date(isoString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

export function NoteAccordionList({ notes, onSelect }: NoteAccordionListProps) {
  const navigate = useNavigate(); // ✅ useNavigate 훅 사용
  return (
    <Accordion
      type="single"
      collapsible
      defaultValue={notes[0]?.id !== undefined ? String(notes[0].id) : undefined}
      className="flex flex-col gap-[var(--size-space-200)]"
    >
      {notes.map((note) => {
        const fallbackId = `${note.title ?? "no-title"}-${note.createdAt}`;
        const stringId = note.id !== undefined ? String(note.id) : fallbackId;

        return (
          <AccordionItem
            key={stringId}
            value={stringId}
            className="bg-color-background-default-secondary rounded-[var(--size-radius-200)] border border-color-border-default-default"
          >
            <AccordionTrigger
              className="flex flex-col text-left px-[var(--size-padding-lg)] py-[var(--size-padding-lg)]"
            >
              <span className="text-[length:var(--body-strong-font-size)] font-[number:var(--body-strong-font-weight)] text-color-text-default-default">
                {note.title || "제목 없음"}
              </span>
              <span className="text-sm text-color-text-default-secondary">
                {formatDate(note.createdAt)}
              </span>
            </AccordionTrigger>

            <AccordionContent className="px-[var(--size-padding-lg)] pb-[var(--size-padding-lg)]">
              <p className="whitespace-pre-line text-[length:var(--body-base-font-size)] font-[number:var(--body-base-font-weight)] text-color-text-default-default">
                {note.text?.slice(0, 100) || "내용 없음"}
              </p>
              <div className="mt-4 text-right">
                <button
                onClick={() => navigate(`/note/${note.id}/edit`)} // ✅ 여기서 이동
                className="text-sm text-blue-500 hover:underline"
              >
                편집하기
              </button>
              </div>
            </AccordionContent>
          </AccordionItem>
        );
      })}
    </Accordion>
  );
}
