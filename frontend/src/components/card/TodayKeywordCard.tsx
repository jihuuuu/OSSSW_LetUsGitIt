// 📄 src/components/TodayKeywordPreview.tsx

import React, { useEffect, useState } from "react";
import axios from "axios";
import { TodayKeywordGraph } from "@/components/TodayKeywordGraph";
import { motion } from "framer-motion";
type ClusterOut = {
  cluster_id: number;
  keywords: string[];
  num_articles: number; // API에서 받아오는 기사 수
  // (그 외 필드는 이 컴포넌트에서 사용하지 않으므로 생략)
};

export const TodayKeywordPreview: React.FC = () => {
  const [clusters, setClusters] = useState<ClusterOut[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 컴포넌트 마운트 시점에 /clusters/today 호출
    async function fetchTodayClusters() {
      try {
        const response = await axios.get<ClusterOut[]>(
          "http://localhost:8000/clusters/today"
        );
        // API가 20개 중 상위 20개를 반환하므로, 상위 10개만 사용
        const topTen = response.data.slice(0, 10);
        setClusters(topTen);
      } catch (e) {
        console.error("클러스터 데이터 로드 실패:", e);
        setError("오늘의 키워드 클러스터를 불러오는 데 실패했습니다.");
      }
    }

    fetchTodayClusters();
  }, []);

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!clusters) {
    return (
      <div className="p-6 text-center">
        <p className="text-gray-500">오늘의 키워드 클러스터를 불러오는 중...</p>
      </div>
    );
  }

  return (
    <div className="w-full overflow-hidden">
    <h1 className="text-2xl font-bold text-center mb-4">오늘의 키워드</h1>
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      viewport={{ once: true, amount: 0.2 }}
    >
      <TodayKeywordGraph
        clusters={clusters.map((cl) => ({
          cluster_id: cl.cluster_id,
          keywords: cl.keywords,
          num_articles: cl.num_articles,
        }))}
      />
    </motion.div>
  </div>
  );
};
