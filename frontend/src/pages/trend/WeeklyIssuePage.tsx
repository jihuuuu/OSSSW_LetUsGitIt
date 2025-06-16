// src/pages/Trend/WeeklyIssuePage.tsx
import { useEffect, useState } from 'react';
import LineChart from '@/components/LineChart';

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

export default function WeeklyIssuePage() {
  const [keywords, setKeywords] = useState<{ keyword: string; count: number }[]>([]);
  const [trendData, setTrendData] = useState<Record<string, any>[]>([]);
   const [animationKey, setAnimationKey] = useState(0); // ⭐ animation trigger
  useEffect(() => {
    fetch('http://3.39.180.27:8000/trends/weekly')
      .then(res => res.json())
      .then((data: ApiResponse) => {
        const kwList = data.trend_data.map((d: TrendItem) => ({
          keyword: d.keyword,
          count: d.total_counts
        }));
        setKeywords(kwList);

        const chartData = data.trend_data[0]?.daily_counts.map((_, i: number) => {
          const point: Record<string, any> = { date: data.trend_data[0].daily_counts[i].date };
          data.trend_data.forEach((kw: TrendItem) => {
            point[kw.keyword] = kw.daily_counts[i].count;
          });
          return point;
        }) || [];

        setTrendData(chartData);
      });
  }, []);

  // ⭐ 10초마다 animationKey 증가
  useEffect(() => {
    const timer = setInterval(() => {
      setAnimationKey(prev => prev + 1);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="max-w-screen-xl mx-auto px-4 grid grid-cols-5 gap-6">
      {/* 왼쪽 키워드 박스 */}
      <div className="col-span-1">
        <div className="bg-white rounded shadow p-4">
          <h2 className="text-blue-600 text-lg font-bold mb-4">이주의 키워드</h2>
          <ul key={animationKey} className="space-y-4">
            {keywords.slice(0, 5).map((item, idx) => (
              <li
                key={idx}
                className="flex justify-between items-center opacity-0 translate-y-4 animate-fade-slide-in"
                style={{
                  animationDelay: `${idx * 0.2}s`,
                  animationFillMode: "forwards",
                }}
              >
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-semibold text-blue-600 border border-blue-400 rounded-full w-6 h-6 flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="text-md font-medium">{item.keyword}</span>
                </div>
                <span className="text-sm text-gray-500">{item.count}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
  
      {/* 오른쪽 라인 차트 */}
      <div className="col-span-4">
        <LineChart data={trendData} />
      </div>
    </div>
  );
}
