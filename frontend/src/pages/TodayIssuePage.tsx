// TodayIssuePage.tsx

import React, { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { useNavigate } from "react-router-dom";
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
  const navigate = useNavigate();

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
      {/* 헤더 */}
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">오늘의 이슈 10</h1>
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
                  <li key={article.article_id}>
                    <a
                      href={article.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ color: '#000000', textDecoration: 'none' /* hover 효과는 아래 예시 참고 */ }}
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
    </div>
  );
}
