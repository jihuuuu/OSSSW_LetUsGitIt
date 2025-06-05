import { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { getArticlesByNoteId } from "@/services/note";
import type { Article } from "@/types/article";

export default function NoteEditPage() {
  const { noteId } = useParams();
  const id=Number(noteId);
  const navigate = useNavigate();
  const location = useLocation();

  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [articles, setArticles] = useState<Article[]>([]);
//1. 노트 로딩
useEffect(() => {
  const loadNote = async () => {
    if (!noteId) return;

      const res = await fetch(`http://localhost:8000/users/notes/${noteId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      });

      const data = await res.json();
      if (!data?.result) return;

      setTitle(data.result.title || "");
      setText(data.result.text || "");

      const related = await getArticlesByNoteId(Number(noteId));
      setArticles(related);
  };

  loadNote();
}, [noteId]);
//2. 새 기사 병합
useEffect(() => {
  const incoming = location.state?.newArticles;
  if (!incoming || !Array.isArray(incoming)) return;

  setArticles((prev) => {
    const map = new Map<number, Article>();
    prev.forEach((a) => map.set(a.id, a));
    incoming.forEach((a: Article) => map.set(a.id, a));
    return Array.from(map.values());
  });
},  [location.key]);
  const handleSave = async () => {
    const res = await fetch(`http://localhost:8000/users/notes/${noteId}`, {
      method: "PUT",
      headers: { 
      "Content-Type": "application/json" ,
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`},
      body: JSON.stringify({ title,text , article_ids: articles.map((a) => a.id) }),
    });

    if (res.ok) {
      alert("노트 수정 완료!");
      navigate("/users/notes"); // 목록으로 돌아감
    } else {
      alert("수정 실패");
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-5">노트 편집</h1>
      <input
        className="w-full border p-2 mb-8"
        placeholder="제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="w-full border p-2 h-80 mb-10"
        placeholder="내용"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
    className="text-lg underline text-blue-600 mb-4"
    onClick={() =>
      navigate("/users/scraps", {
        state: {
          mode: "edit-note",
          originNoteId: noteId,
          selectedArticles: articles,
        },
      })
    }
  >
    기사 추가하기+
  </button>
      
      <h2 className="font-semibold text-2xl mb-2">연관 기사</h2>
      <ul className="list-disc pl-5 text-blue-600 mb-8">
        {articles.map((a) => (
          <li key={a.id}>
            <a href={a.link} target="_blank" rel="noreferrer">
              {a.title}
            </a>
            <button
        onClick={() =>
          setArticles((prev) => prev.filter((article) => article.id !== a.id))
        }
        className="ml-2 text-red-500 text-sm"
      >
        삭제
      </button>
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
