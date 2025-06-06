// TodayIssuePage.tsx

import { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { useNavigate, useLocation } from "react-router-dom";
import Header from "@/components/Header";

interface Article {
  article_id: number;
  title: string;
  summary: string;
  link: string;
  published: string;
}

interface Cluster {
  cluster_id: number;
  created_at: string;
  label: number;
  num_articles: number;
  keywords: string[];
  articles: Article[];
}

export default function TodayIssuePage() {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedArticles, setSelectedArticles] = useState<Set<number>>(new Set());
  const navigate = useNavigate();
  const location = useLocation();
  const mode = location.state?.mode;
  const originNoteId = location.state?.originNoteId;
  const preselected = location.state?.selectedArticles || [];
  const [noteMode, setNoteMode] = useState(false);

  const handleArticleSelect = (articleId: number, checked: boolean) => {
  setSelectedArticles((prev) => {
    const updated = new Set(prev);
    checked ? updated.add(articleId) : updated.delete(articleId);
    return updated;
  });
};
const handleCreateNote = () => {
  const selected = clusters
    .flatMap((cluster) => cluster.articles)
    .filter((a) => selectedArticles.has(a.article_id));

  if (selected.length === 0) {
    alert("기사를 선택해주세요.");
    return;
  }

  const defaultText = selected
    .map((a) => `• ${a.title}\n${a.link}`)
    .join("\n\n");

  navigate("/note/new", {
    state: {
      defaultText,
      articles: selected,
    },
  });
};

const handleAddToExistingNote = () => {
  const selected = clusters
    .flatMap((cluster) => cluster.articles)
    .filter((a) => selectedArticles.has(a.article_id));

  if (selected.length === 0) {
    alert("기사를 선택해주세요.");
    return;
  }

  navigate("/notes", {
    state: {
      newArticles: selected,
    },
  });
};


  useEffect(() => {
    const fetchClusters = async () => {
      try {
        const res = await axios.get<Cluster[]>("http://localhost:8000/clusters/today")
        console.log("▶️ /clusters/today response:", res.data);
        setClusters(res.data);
      } catch (err: any) {
        console.error("클러스터 불러오기 실패:", err);
        setError("데이터를 불러오지 못했습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchClusters();
    if (mode === "edit-note") {
    setNoteMode(true);
    setSelectedArticles(new Set(preselected.map((a: Article) => a.article_id)));
  }
  }, []);
  

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">로딩 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <header className="h-15 bg-blue-500 text-white px-6 flex items-center justify-between mb-2">
              <div className="flex items-center">
                <Logo />
              </div>
              <h1 className="text-white text-3xl font-bold mx-auto">오늘의 이슈 10</h1>
              <div className="px-2 py -1">
                <Header />
              </div>
            </header>

      {/* 본문 */}
      <main className="px-6 py-8 space-y-6">
        {clusters.map((cluster, index) => (
          <section key={cluster.cluster_id}>
            {/* 키워드 + (+) 버튼 */}
            <div className="flex justify-between items-center">
              <h2 className="font-bold text-lg">
                {index + 1}. {cluster.keywords.join(" ")}
              </h2>
              <button
                onClick={() => navigate(`/clusters/${cluster.cluster_id}`)}
                className="text-blue-500 hover:underline text-sm"
              >
                더보기
              </button>
            </div>

            <div className="bg-gray-50 border rounded-md shadow px-4 py-2 mt-2">
              <p className="font-semibold mb-2">관련기사</p>
              <ul className="list-disc list-inside text-sm space-y-1">
                {cluster.articles.map((article) => (
  <li key={article.article_id} className="flex items-start gap-2">
    {noteMode && (
      <input
        type="checkbox"
        checked={selectedArticles.has(article.article_id)}
        onChange={(e) =>
          handleArticleSelect(article.article_id, e.target.checked)
        }
      />
    )}
    <a
      href={article.link}
      target="_blank"
      rel="noopener noreferrer"
      style={{ color: '#000', textDecoration: 'none' }}
      onMouseEnter={e => (e.currentTarget.style.textDecoration = 'underline')}
      onMouseLeave={e => (e.currentTarget.style.textDecoration = 'none')}
    >
      {article.title}
    </a>
  </li>
))}
              </ul>
            </div>
          </section>
        ))}
      </main>
      <div className="sticky bottom-4 right-4 flex justify-end mt-6 pr-4">
  {noteMode ? (
    <div className="flex gap-2">
      <button
        onClick={handleCreateNote}
        className="px-4 py-2 bg-sky-500 text-white rounded-full shadow"
      >
        ✏️ 새 노트 작성
      </button>
      <button
        onClick={handleAddToExistingNote}
        className="px-4 py-2 bg-green-500 text-white rounded-full shadow"
      >
        ➕ 기존 노트에 추가
      </button>
    </div>
  ) : (
    <button
      onClick={() => setNoteMode(true)}
      className="w-12 h-12 rounded-full border text-2xl shadow"
    >
      ✏️
    </button>
  )}
</div>
    </div>
  );
}
function setNoteMode(arg0: boolean) {
  throw new Error("Function not implemented.");
}

