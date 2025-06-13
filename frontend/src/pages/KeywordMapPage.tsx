import { useEffect, useState } from "react";
import { fetchLatestKnowledgeMap } from "@/services/knowledgeMap";
import { KeywordGraph } from "@/components/KeywordGraph";

export default function KeywordMapPage() {
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchLatestKnowledgeMap()
      .then((res) => {
        const data = res as { nodes?: any[]; edges?: any[] };
        setNodes(data.nodes || []);
        setEdges(data.edges || []);
      })
      .catch((err) => console.error("지식맵 그래프 로딩 실패", err))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <p className="p-4 text-center">로딩 중...</p>;

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">📚 나의 최신 지식맵</h2>
      {nodes.length > 0 ? (
        <KeywordGraph nodes={nodes} edges={edges} />
      ) : (
        <p className="text-sm text-gray-500">지식맵이 없습니다.</p>
      )}
    </div>
  );
}