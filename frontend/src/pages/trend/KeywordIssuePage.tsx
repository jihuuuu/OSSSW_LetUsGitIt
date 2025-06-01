import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { KeywordGraph } from "@/components/KeywordGraph";
import LineChart from "@/components/LineChart"; // ✅ default import 방식
import type { PCluster } from "@/types/cluster";
import type { TrendItem } from "@/types/trend";

export default function KeywordIssuePage() {
  const [keyword, setKeyword] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [clusters, setClusters] = useState<PCluster[]>([]);
  const [trendData, setTrendData] = useState<TrendItem | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keyword.trim()) return;

    setLoading(true);
    setSubmitted(true);

    try {
      const res = await fetch(`http://localhost:8000/trends/search?keyword=${encodeURIComponent(keyword)}`);
      if (!res.ok) throw new Error("API 요청 실패");
      const data = await res.json();

      const clusters: PCluster[] = data.related_keywords.map((rk: any, idx: number) => ({
        id: rk.cluster_id,
        keywords: [
          ...rk.co_keywords.map((name: string, i: number) => ({
            id: idx * 100 + i,
            name,
          })),
          ...rk.frequent_keywords.map((name: string, i: number) => ({
            id: idx * 100 + rk.co_keywords.length + i,
            name,
          })),
          { id: -1, name: data.keyword }, // 검색한 키워드도 포함
        ],
      }));

      const trend: TrendItem = {
        keyword: data.keyword,
        total_counts: data.trend.reduce((sum: number, d: any) => sum + d.count, 0),
        daily_counts: data.trend,
      };

      setClusters(clusters);
      setTrendData(trend);
    } catch (err) {
      console.error("검색 실패:", err);
      setClusters([]);
      setTrendData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">키워드 검색</h1>

      <div className="flex justify-center mb-8">
        <div className="relative w-full max-w-xl">
          <Input
            type="text"
            placeholder="예: 트럼프"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            className="pl-10 pr-4 py-2"
          />
          <Search
            className="absolute left-3 top-2.5 text-gray-500 cursor-pointer"
            onClick={handleSearch}
          />
        </div>
      </div>

      {loading && <p className="text-center text-gray-500">불러오는 중...</p>}

      {submitted && !loading && trendData && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 border rounded shadow">
            <h2 className="text-lg font-semibold mb-2">연관 키워드</h2>
            <KeywordGraph clusters={clusters} />
          </div>
          <div className="p-4 border rounded shadow">
            <h2 className="text-lg font-semibold mb-2">언급량 추이</h2>
            <LineChart data={trendData.daily_counts} /> {/* ✅ 수정된 부분 */}
          </div>
        </div>
      )}
    </div>
  );
}
