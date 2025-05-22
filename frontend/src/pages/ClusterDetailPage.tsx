import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Logo from "@/components/ui/logo"; // 로고 컴포넌트 경로 수정 필요
import { Star } from "lucide-react"; // 아이콘 라이브러리 사용 (또는 직접 SVG 가능)

interface Article {
  article_id: number;
  title: string;
  link: string;
}

interface ClusterDetail {
  cluster_id: number;
  keywords: string[];
  articles: Article[];
}

export default function ClusterDetailPage() {
  const { clusterId } = useParams();
  const [cluster, setCluster] = useState<ClusterDetail | null>(null);
  const [favorites, setFavorites] = useState<Set<number>>(new Set());

  useEffect(() => {
    // 실제 백엔드 연동 시엔 아래 axios 사용
    // axios.get(`/api/clusters/${clusterId}`).then((res) => {
    //   setCluster(res.data);
    // });

    // 백 연결 전 테스트용 (임시 더미 데이터)
    setCluster({
      cluster_id: 1,
      keywords: ["클러스터", "키워드", "예시"],
      articles: [
        { article_id: 1, title: "공차, 블랙 밀크티 '맛있어'…", link: "http://www.dyenews.co.kr/news/articleView.html?idxno=801677" },
        { article_id: 2, title: "예시예시 ‘피그마’ 예시", link: "http://www.news.co.kr/news/example" },
        { article_id: 2, title: "예시2 ‘피그마’ 예시", link: "http://www.news.co.kr/news/example" }
      ]
    });
  }, [clusterId]);

  const toggleFavorite = (id: number) => {
    setFavorites((prev) => {
      const updated = new Set(prev);
      updated.has(id) ? updated.delete(id) : updated.add(id);
      return updated;
    });
  };

  return (
    <div className="min-h-screen bg-white">
      {/* 헤더 */}
      <header className="relative bg-sky-400 h-20 flex items-center px-6">
        <div className="absolute left-6 top-1/2 transform -translate-y-1/2">
          <Logo />
        </div>
        <h1 className="text-white text-xl font-bold mx-auto">오늘의 이슈 10</h1>
      </header>

      {/* 내용 */}
      <main className="max-w-4xl mx-auto p-6">
        {cluster ? (
          <>
            <h2 className="text-center text-2xl font-bold my-6">
              {cluster.keywords.join(" ")}
            </h2>

            <div className="bg-gray-50 border rounded-md p-4 shadow">
              <p className="text-xl font-semibold mb-4">관련기사</p>
              <ul className="divide-y divide-gray-200">
                {cluster.articles.map((article) => (
                    <li key={article.article_id} className="py-4 flex justify-between items-start gap-4">
                    {/* 왼쪽: 기사 제목 + 링크 */}
                    <div className="flex flex-col text-left flex-1">
                      <p className="text-sm leading-snug">• {article.title}</p>
                      <a
                        href={article.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-600 break-all"
                      >
                        {article.link}
                      </a>
                    </div>
                  
                    {/* 오른쪽: 별 아이콘 */}
                    <button onClick={() => toggleFavorite(article.article_id)}>
                      <Star
                        className={`w-5 h-5 mt-1 ${
                          favorites.has(article.article_id)
                            ? "text-yellow-400 fill-yellow-400"
                            : "text-gray-300"
                        }`}
                      />
                    </button>
                  </li>
                  
                ))}
              </ul>
            </div>
          </>
        ) : (
          <p className="text-center text-gray-500 mt-20">불러오는 중...</p>
        )}
      </main>
    </div>
  );
}
