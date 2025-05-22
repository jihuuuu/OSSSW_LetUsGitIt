// src/components/NoteAccordionList.tsx
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

import type { Note } from "@/types/note"; 

function formatDate(isoString: string) {
  const date = new Date(isoString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

export function NoteAccordionList({
  notes,
  onSelect,
}: {
  notes: Note[];
  onSelect: (note: Note) => void;
}) {
  return (
    <Accordion
      type="single"
      collapsible
      defaultValue={notes[0]?.id}
      className="flex flex-col gap-[var(--size-space-200)]"
    >
      {notes.map((note) => (
        <AccordionItem
          key={note.id}
          value={note.id}
          onClick={() => onSelect(note)}
          className="bg-color-background-default-secondary rounded-[var(--size-radius-200)] border border-color-border-default-default"
        >
          <AccordionTrigger className="flex flex-col text-left px-[var(--size-padding-lg)] py-[var(--size-padding-lg)]">
            <span className="text-[length:var(--body-strong-font-size)] font-[number:var(--body-strong-font-weight)] text-color-text-default-default">
              {note.title || "제목 없음"}
            </span>
            <span className="text-sm text-color-text-default-secondary">
              {formatDate(note.createdAt)}
            </span>
          </AccordionTrigger>
          <AccordionContent className="px-[var(--size-padding-lg)] pb-[var(--size-padding-lg)]">
            <p className="whitespace-pre-line text-[length:var(--body-base-font-size)] font-[number:var(--body-base-font-weight)] text-color-text-default-default">
              {note.content?.slice(0, 100) || "내용 없음"}
            </p>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
