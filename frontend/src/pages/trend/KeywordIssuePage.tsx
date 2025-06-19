import { useEffect, useState } from "react";
import { RelatedKeywordGraph } from "@/components/RelatedKeywordGraph";
import LineChart from "@/components/LineChart";
import type { PCluster } from "@/types/cluster";
import type { TrendItem } from "@/types/trend";

export default function KeywordIssuePage() {
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);
  const [clusters, setClusters] = useState<PCluster[]>([]);
  const [trendData, setTrendData] = useState<TrendItem | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://3.37.87.202:8000/trends/suggested_keywords")
    .then((res) => {
      if (!res.ok) throw new Error("추천 키워드 요청 실패");
      return res.json();
    })
    .then((data) => {
      setKeywords(data.keywords);
    })
    .catch((err) => {
      console.error("추천 키워드 로딩 실패:", err);
      setKeywords([]); // 실패해도 화면 깨지지 않도록 초기화
    });
  }, []);

  const getInitialSound = (str: string): string => {
    const ch = str[0];
    const code = ch.charCodeAt(0) - 44032;
    if (code < 0 || code > 11171) return ch;
    const initials = [
      "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ",
      "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ",
      "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
    ];
    return initials[Math.floor(code / 588)];
  };

  const groupByInitial = (words: string[]): Record<string, string[]> => {
    const grouped: Record<string, string[]> = {};
    for (const word of words) {
      const initial = getInitialSound(word);
      if (!grouped[initial]) grouped[initial] = [];
      grouped[initial].push(word);
    }
    for (const key in grouped) {
      grouped[key].sort((a, b) => a.localeCompare(b, "ko", { sensitivity: "base" }));
    }
    return Object.fromEntries(
      Object.entries(grouped).sort(([a], [b]) => a.localeCompare(b, "ko"))
    );
  };

  const handleSearch = async (kw: string) => {
    if (!kw.trim()) return;
    setLoading(true);
    setSelectedKeyword(kw);

    try {
      const res = await fetch(`http://3.37.87.202:8000/trends/search?keyword=${encodeURIComponent(kw)}`);
      if (!res.ok) throw new Error("API 요청 실패");
      const data = await res.json();

      // 중심 키워드 노드 정의
      const centralKeyword = {
        id: -999,
        name: data.keyword,
        clusterId: -1,
      };

      // 1️⃣ 관련 클러스터들
      const clusters: PCluster[] = data.related_keywords.map(
        (rk: any, idx: number) => ({
          id: rk.cluster_id,
          label: rk.co_keywords?.[0]            // 대표 키워드가 있으면 사용
                ?? rk.frequent_keywords?.[0]    // 없으면 frequent 중 첫 번째
                ?? `Cluster ${idx + 1}`,        // 전부 없으면 fallback
          keywords: [
            ...rk.co_keywords.map((name: string, i: number) => ({
              id: idx * 100 + i,
              name,
              clusterId: rk.cluster_id,
            })),
            ...rk.frequent_keywords.map((name: string, i: number) => ({
              id: idx * 100 + rk.co_keywords.length + i,
              name,
              clusterId: rk.cluster_id,
            })),
          ],
        })
      );

      // 2️⃣ 중심 클러스터 (label 필수!)
      clusters.unshift({
        id: -1,
        label: data.keyword,        // 중심 키워드 자체를 라벨로
        keywords: [centralKeyword],
      });

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

  const grouped = groupByInitial(keywords);

  return (
    <div className="max-w-[1100px] mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4 text-center">키워드 검색</h1>
  
      {!selectedKeyword && (
        <>
          <p className="text-center text-gray-600 mb-6">
            🔍 일주일 간 이슈 키워드로 선정된 단어들입니다. 원하는 키워드를 눌러 연관 키워드와 언급량 추이를 확인해보세요!
          </p>
          <div className="space-y-6">
            {Object.entries(grouped).map(([initial, wordList]) => (
              <div key={initial}>
                <h2 className="font-bold text-lg mb-2">{initial}</h2>
                <div className="flex flex-wrap gap-2">
                  {wordList.map((word) => (
                    <button
                      key={word}
                      onClick={() => handleSearch(word)}
                      className="px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-sm"
                    >
                      {word}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
  
      {selectedKeyword && (
        <div className="text-right mb-4">
          <button
            onClick={() => {
              setSelectedKeyword(null);
              setClusters([]);
              setTrendData(null);
            }}
            className="text-sm text-blue-600 hover:underline"
          >
            ← 추천 키워드 다시 보기
          </button>
        </div>
      )}
  
      {loading && <p className="text-center text-gray-500">불러오는 중...</p>}
  
      {selectedKeyword && !loading && trendData && (
        <div className="grid grid-cols-1 md:grid-cols-[1fr_1fr] gap-6">
          {/* 연관 키워드 그래프 */}
          <div className="p-4 border rounded shadow bg-white">
            <h2 className="text-lg font-semibold mb-2">연관 키워드</h2>
            <RelatedKeywordGraph clusters={clusters} />
          </div>
  
          {/* 언급량 추이 */}
          <div className="p-4 border rounded shadow bg-white overflow-x-auto">
            <h2 className="text-lg font-semibold mb-2">언급량 추이</h2>
            <div className="min-w-[500px]">
              <LineChart
                data={trendData.daily_counts.map((d) => ({
                  date: d.date,
                  [trendData.keyword]: d.count,
                }))}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
  
}
