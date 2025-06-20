import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import type { Article } from "@/types/article";
import { clearSelectedArticles } from "@/utils/selectedArticles";
import useLogoutWatcher from "@/hooks/useLogoutWatcher";

export default function NoteCreatePage() {
  useLogoutWatcher();
  const location = useLocation();
  const navigate = useNavigate();

  const defaultText = location.state?.defaultText || "";
  const [title, setTitle] = useState("");
  const [text, setText] = useState(defaultText);
  const [articles, setArticles] = useState<Article[]>(location.state?.articles || []);

  const handleSave = async () => {
    const res = await fetch("http://52.79.50.169:8000/users/notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
      body: JSON.stringify({
        title,
        text,
        article_ids: articles.map((a) => a.id),
      }),
    });

    const data = await res.json();
    if (data.isSuccess) {
      alert("노트가 저장되었습니다.");
      navigate("/users/notes"); // 또는 원하는 경로
    } else {
      alert("노트 저장 실패");
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-5">노트 작성</h1>
      <input
        type="text"
        placeholder="노트 제목"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="w-full border p-2 mb-8"
      />
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full border p-2 h-80 mb-10"
      />
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
        <button onClick={() => {
          clearSelectedArticles();// 선택한 기사 초기화 (필요하다면 여기에 초기화 로직 추가)
          navigate(-1);
        }}>취소</button>
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
