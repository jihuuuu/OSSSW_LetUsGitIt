import { useEffect, useState } from "react";
import { KeywordGraph } from "@/components/KeywordGraph";
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
    // fetch("http://localhost:8000/trends/suggested_keywords")
    // .then((res) => {
    //   if (!res.ok) throw new Error("추천 키워드 요청 실패");
    //   return res.json();
    // })
    // .then((data) => {
    //   setKeywords(data.keywords);
    // })
    // .catch((err) => {
    //   console.error("추천 키워드 로딩 실패:", err);
    //   setKeywords([]); // 실패해도 화면 깨지지 않도록 초기화
    // });
    setKeywords([
      "국민의 힘", "고급", "금리", "기업",
      "나혼아", "나이스", "나이지리아", "네거티브", "나고야", "낭떠러지",
      "더불어민주당", "두산", "대선", "대통령",
      "로봇", "러시아",
      "모비스", "무리",
      "ㅂㅂㅂ", "ㅇㅇㅇ", "ㅇㅇㅇㅇㅇ", "ㅇㅇㅇㅇ", "ㅇㅇ", "ㅇㅇㅇ",
      "사과", "소수", "사이다", "사이다", "숭례문",
      "이준석", "율용도",
      "트럼프", "서울", "이재명"
    ]);
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
      const res = await fetch(`http://localhost:8000/trends/search?keyword=${encodeURIComponent(kw)}`);
      if (!res.ok) throw new Error("API 요청 실패");
      const data = await res.json();

      const clusters: PCluster[] = data.related_keywords.map((rk: any, idx: number) => ({
        id: rk.cluster_id,
        keywords: [
          ...rk.co_keywords.map((name: string, i: number) => ({ id: idx * 100 + i, name })),
          ...rk.frequent_keywords.map((name: string, i: number) => ({ id: idx * 100 + rk.co_keywords.length + i, name })),
          { id: -1, name: data.keyword },
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

  const grouped = groupByInitial(keywords);

  return (
    <div className="max-w-4xl mx-auto p-6">
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 border rounded shadow">
            <h2 className="text-lg font-semibold mb-2">연관 키워드</h2>
            <KeywordGraph clusters={clusters} />
          </div>
          <div className="p-4 border rounded shadow">
            <h2 className="text-lg font-semibold mb-2">언급량 추이</h2>
            <LineChart
              data={trendData.daily_counts.map((d) => ({
                date: d.date,
                [trendData.keyword]: d.count,
              }))}
            />
          </div>
        </div>
      )}
    </div>
  );
}
