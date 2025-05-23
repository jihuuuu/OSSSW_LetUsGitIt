// TodayIssuePage.tsx

import React, { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo";
import { useNavigate } from "react-router-dom";

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

const dummyClusters = [
    {
      cluster_id: 1,
      created_at: "2025-05-16T12:00:00",
      label: 3,
      num_articles: 27,
      keywords: ["이재명", "총선", "서울"],
      articles: [
        {
          article_id: 1001,
          title: "이재명 총선 유세, 서울 집중",
          summary: "이재명 후보가 서울에서 집중 유세를 펼쳤다...",
          link: "https://news.site/article/1001",
          published: "2025-05-15T19:00:00",
        },
        {
          article_id: 1002,
          title: "서울 유세 현장 열기",
          summary: "수많은 시민이 몰린 서울 유세 현장...",
          link: "https://news.site/article/1002",
          published: "2025-05-15T18:30:00",
        },
      ],
    },
    {
      cluster_id: 2,
      created_at: "2025-05-16T13:00:00",
      label: 5,
      num_articles: 15,
      keywords: ["후보", "유세", "정책"],
      articles: [
        {
          article_id: 2001,
          title: "OOO 후보 정책 발표",
          summary: "OOO 후보가 새로운 복지 정책을 발표했다...",
          link: "https://news.site/article/2001",
          published: "2025-05-15T20:00:00",
        },
        {
          article_id: 2002,
          title: "공약 유세 현장",
          summary: "열띤 분위기의 공약 유세 현장...",
          link: "https://news.site/article/2002",
          published: "2025-05-15T20:30:00",
        },
      ],
    },
];

export default function TodayIssuePage() {
    const [clusters, setClusters] = useState(dummyClusters); // 더미데이터
    const navigate = useNavigate();
  
    return (
      <div className="min-h-screen bg-white">
        {/* 헤더 */}
        <header className="relative bg-sky-400 h-20 flex items-center px-6">
          <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
            <Logo />
          </div>
          <h1 className="text-white text-xl font-bold mx-auto">오늘의 이슈 10</h1>
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
                  onClick={() => navigate(`/cluster/${cluster.cluster_id}`)}
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
                        className="text-blue-600 hover:underline"
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