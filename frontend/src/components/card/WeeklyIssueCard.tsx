import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ 추가
import LineChart from '@/components/LineChart';
import { motion } from "framer-motion";
type DailyCount = { date: string; count: number };
type TrendItem = {
  keyword: string;
  total_counts: number;
  daily_counts: DailyCount[];
};
type ApiResponse = {
  start_date: string;
  end_date: string;
  top_keywords: string[];
  trend_data: TrendItem[];
};

export default function WeeklyIssuePreview() {
  const [trendData, setTrendData] = useState<Record<string, any>[]>([]);
  const navigate = useNavigate(); // ✅ 추가

  useEffect(() => {
    fetch('http://54.180.26.163:8000/trends/weekly')
      .then(res => res.json())
      .then((data: ApiResponse) => {
        const chartData = data.trend_data[0]?.daily_counts.map((_: any, i: number) => {
          const point: Record<string, any> = { date: data.trend_data[0].daily_counts[i].date };
          data.trend_data.forEach((kw: TrendItem) => {
            point[kw.keyword] = kw.daily_counts[i].count;
          });
          return point;
        }) || [];
        setTrendData(chartData);
      });
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      viewport={{ once: true, amount: 0.2 }}
      className="bg-white p-4"
    >
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-blue-500">뉴스 트렌드</h2>
        <button
          onClick={() => navigate("/trend")}
          className="text-sm text-blue-500 hover:underline"
        >
          더보기
        </button>
      </div>
      <div className="h-[400px]">
        <LineChart data={trendData} />
      </div>
    </motion.div>
  );
}
