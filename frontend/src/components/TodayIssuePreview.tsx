// src/components/TodayIssuePreview.tsx
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

interface Article {
  article_id: number;
  title: string;
  link: string;
}

interface Cluster {
  cluster_id: number;
  keywords: string[];
  articles: Article[];
}

export default function TodayIssuePreview() {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get("http://localhost:8000/clusters/today")
      .then(res => setClusters(res.data.slice(0, 3))) // 상위 3개만 표시
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="bg-white shadow-md rounded-xl p-4 w-[400px]">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-blue-500">오늘의 이슈</h2>
        <button
          onClick={() => navigate("/today/issue")}
          className="text-sm text-blue-500 hover:underline"
        >
          더보기
        </button>
      </div>
      <ol className="space-y-2">
        {clusters.map((cluster, i) => (
          <li key={cluster.cluster_id} className="flex items-center gap-2">
            <span className="bg-blue-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
              {i + 1}
            </span>
            {cluster.keywords.join(", ")}
          </li>
        ))}
      </ol>
    </div>
  );
}
