import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getArticlesByNoteId } from "@/services/note";
import type { Article } from "@/types/article";

export default function NoteEditPage() {
  const { noteId } = useParams();
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    const loadNote = async () => {
      if (!noteId) return;  // noteId가 없으면 중단

    const res = await fetch(`http://localhost:8000/users/notes/${noteId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });

    const data = await res.json();
    console.log("📌 Note 데이터:", data);

    setTitle(data.result.title || "");
    setText(data.result.text || "");

    const related = await getArticlesByNoteId(Number(noteId));
    setArticles(related);
  };

    loadNote();
  }, [noteId]);

  const handleSave = async () => {
    const res = await fetch(`http://localhost:8000/users/notes/{noteId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, content: text }),
    });

    if (res.ok) {
      alert("노트 수정 완료!");
      navigate("users/notes"); // 목록으로 돌아감
    } else {
      alert("수정 실패");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">노트 편집</h1>
      <input
        className="w-full border p-2 mb-4"
        placeholder="제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="w-full border p-2 h-40 mb-4"
        placeholder="내용"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <h2 className="font-semibold mb-2">연관 기사</h2>
      <ul className="list-disc pl-5 text-blue-600 mb-6">
        {articles.map((a) => (
          <li key={a.id}>
            <a href={a.link} target="_blank" rel="noreferrer">
              {a.title}
            </a>
          </li>
        ))}
      </ul>
      <div className="flex justify-end gap-2">
        <button onClick={() => navigate(-1)}>취소</button>
        <button
          onClick={handleSave}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          저장
        </button>
      </div>
    </div>
  );
}
