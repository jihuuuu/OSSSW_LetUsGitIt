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

  // useEffect(() => {
  //   fetch('/api/trends/weekly')
  //     .then(res => res.json())
  //     .then((data: ApiResponse) => {
  //       setKeywords(data.trend_data.map((d: TrendItem) => ({
  //         keyword: d.keyword,
  //         count: d.total_counts
  //       })));

  //       const chartData = data.trend_data[0]?.daily_counts.map((_: any, i: number) => {
  //         const point: Record<string, any> = { date: data.trend_data[0].daily_counts[i].date };
  //         data.trend_data.forEach((kw: TrendItem) => {
  //           point[kw.keyword] = kw.daily_counts[i].count;
  //         });
  //         return point;
  //       }) || [];

  //       setTrendData(chartData);
  //     });
  // }, []);

  useEffect(() => {
    const dummyData = {
      start_date: '2025-05-10',
      end_date: '2025-05-16',
      top_keywords: ['이재명', '총선'],
      trend_data: [
        {
          keyword: '이재명',
          total_counts: 123,
          daily_counts: [
            { date: '2025-05-10', count: 12 },
            { date: '2025-05-11', count: 18 },
            { date: '2025-05-12', count: 10 },
            { date: '2025-05-13', count: 21 },
            { date: '2025-05-14', count: 26 },
            { date: '2025-05-15', count: 17 },
            { date: '2025-05-16', count: 19 }
          ]
        },
        {
          keyword: '총선',
          total_counts: 99,
          daily_counts: [
            { date: '2025-05-10', count: 10 },
            { date: '2025-05-11', count: 14 },
            { date: '2025-05-12', count: 13 },
            { date: '2025-05-13', count: 15 },
            { date: '2025-05-14', count: 12 },
            { date: '2025-05-15', count: 16 },
            { date: '2025-05-16', count: 19 }
          ]
        }
      ]
    };
  
    // 상태 업데이트
    setKeywords(dummyData.trend_data.map((d) => ({
      keyword: d.keyword,
      count: d.total_counts
    })));
  
    const chartData = dummyData.trend_data[0].daily_counts.map((_, i) => {
      const point: Record<string, any> = { date: dummyData.trend_data[0].daily_counts[i].date };
      dummyData.trend_data.forEach((kw) => {
        point[kw.keyword] = kw.daily_counts[i].count;
      });
      return point;
    });
  
    setTrendData(chartData);
  }, []);
  

  return (
    <div className="grid grid-cols-3 gap-6">
      <div className="col-span-1">
        <div className="bg-white rounded shadow p-4">
          <h2 className="text-lg font-bold mb-2">주간 키워드</h2>
          <ul className="space-y-1">
            {keywords.map((item, idx) => (
              <li key={idx} className="flex justify-between">
                <span>{item.keyword}</span>
                <span className="text-sm text-gray-500">{item.count}건</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="col-span-2">
        <LineChart data={trendData} />
      </div>
    </div>
  );
}
