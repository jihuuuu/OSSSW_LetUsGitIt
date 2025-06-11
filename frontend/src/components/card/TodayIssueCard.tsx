// src/components/TodayIssuePreview.tsx
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

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
  const [index, setIndex] = useState(0);

  useEffect(() => {
    axios.get("http://localhost:8000/clusters/today")
      .then(res => setClusters(res.data.slice(0, 10))) // 상위 3개만 표시
      .catch(err => console.error(err));
  }, []);
// 🔁 5초마다 index 변경 (빈 그룹 제외)
useEffect(() => {
  const interval = setInterval(() => {
    setIndex((prev) => {
      const groupCount = clusterGroups.length;
      return groupCount === 0 ? 0 : (prev + 1) % groupCount;
    });
  }, 5000);
  return () => clearInterval(interval);
}, [clusters]);

  // 🔢 클러스터를 3개씩 묶기
  const clusterGroups: Cluster[][] = [];
  for (let i = 0; i < clusters.length; i += 5) {
    clusterGroups.push(clusters.slice(i, i + 5));
  }
  return (
    <section className="w-full flex flex-col items-center justify-center px-4 sm:px-6">
      {/* 제목 */}
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        viewport={{ once: true }}
        className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-14 text-center"
      >
        실시간 오늘의 이슈를 확인하세요
      </motion.h2>

      {/* 카드 */}
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        viewport={{ once: true, amount: 0.2 }}
        className="w-full max-w-4xl bg-white shadow-md rounded-xl px-10 py-8"
      >
        <div className="flex justify-between items-baseline mb-6">
          <h3 className="text-xl font-bold text-blue-500">오늘의 이슈</h3>
          <button
            onClick={() => navigate("/today/issue")}
            className="text-sm text-blue-500 hover:underline"
          >
            더보기
          </button>
        </div>

        <div className="relative h-[16rem] overflow-hidden">
          <ol key={index} className="flex flex-col gap-5">
            {clusterGroups[index]?.map((cluster, i) => (
              <li
                key={cluster.cluster_id}
                className="flex items-center gap-4 opacity-0 translate-y-4 animate-fade-slide-in"
                style={{
                  animationDelay: `${i * 0.2}s`,
                  animationFillMode: "forwards",
                }}
              >
                <span className="bg-blue-500 text-white rounded-full w-7 h-7 flex items-center justify-center text-sm font-bold">
                  {index * 5 + i + 1}
                </span>
                <span className="text-gray-800 text-lg font-medium truncate">
                  {cluster.keywords.join(", ")}
                </span>
              </li>
            ))}
          </ol>
        </div>
      </motion.div>
    </section>
  );
}
