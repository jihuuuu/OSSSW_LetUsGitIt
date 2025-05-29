import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getArticlesByNoteId } from "@/services/note";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import type { Note } from "@/types/note";
import type { Article } from "@/types/article";

export default function NoteEditPage() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [note, setNote] = useState<Note | null>(
    location.state?.note || null
  );
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    if (note) {
      getArticlesByNoteId(Number(note.id)).then(setArticles);
    }
  }, [note]);

  const handleSave = async () => {
    if (!note) return;
    await fetch(`http://localhost:8000/users/notes/${note.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: note.title,
        content: note.text,
      }),
    });
    alert("노트가 수정되었습니다.");
    navigate("/notes");
  };

  if (!note) return <div>잘못된 접근입니다.</div>;

  return (
    <div className="p-10 max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">노트 수정</h2>
      <Input
        className="mb-4"
        value={note.title}
        onChange={(e) => setNote({ ...note, title: e.target.value })}
      />
      <Textarea
        className="mb-4 min-h-[200px]"
        value={note.text}
        onChange={(e) => setNote({ ...note, text: e.target.value })}
      />
      <button
        className="bg-sky-500 text-white px-4 py-2 rounded"
        onClick={handleSave}
      >
        저장
      </button>
    </div>
  );
}
