// src/pages/NoteEditSheetPreview.tsx
import { useState } from "react";
import NoteEditSheet from "@/components/NoteEditSheet";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";

export default function NoteEditSheetPreview() {
  const [open, setOpen] = useState(true);

  const [note, setNote] = useState<Note>({
    id: 1,
    title: "AI 요약 정리",
    text: "ChatGPT가 요약해준 기사 내용입니다.",
    createdAt: "2023-10-01",
  });

  const [articles, setArticles] = useState<Article[]>([
    {
      id: 1,
      title: "ChatGPT 활용법 총정리",
      summary: "ChatGPT를 활용하는 방법에 대한 기사입니다.",
      published: "2023-10-01",
      link: "https://example.com/article1",
    },
    {
      id: 2,
      title: "AI 시대의 윤리 문제",
      summary: "AI 시대에 발생할 수 있는 윤리 문제에 대한 기사입니다.",
    published: "2023-10-02",
      link: "https://example.com/article2",
    },
  ]);

  const handleSave = () => {
    alert("저장되었습니다!");
    setOpen(false);
  };

  return (
    <NoteEditSheet
      open={open}
      note={note}
      articles={articles}
      onClose={() => setOpen(false)}
      onChange={(n) => setNote(n)}
      onSave={handleSave}
    />
  );
}
