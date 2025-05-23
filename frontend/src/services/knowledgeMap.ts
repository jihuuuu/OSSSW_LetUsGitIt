// src/services/knowledgeMap.ts
import api from "./api";
import type { PCluster } from "@/types/cluster";
import type { KnowledgeMap } from "@/types/knowledgeMap";

export async function fetchArticlesByKeywordCluster(keyword: string, page = 1, size = 10) {
  const res = await api.get(`/keywords/${keyword}/clusters/articles`, {
    params: { page, size }
  });
  return res.data;
}
export async function fetchKeywordName(keywordId: number) {
  const res = await api.get(`/keywords/${keywordId}`);
  return res.data.result; // { name: "..." } 형태로 오는 경우
}
export async function fetchLatestKnowledgeMap(): Promise<KnowledgeMap | null> {
  try {
    const res = await api.get("/users/knowledge_maps/graph");
    const { result } = res.data;

    const clusterMap = new Map<number, PCluster>();

    for (const node of result.nodes) {
      if (node.type === "cluster") {
        const clusterId = parseInt(node.id.replace("cl-", ""));
        clusterMap.set(clusterId, {
          id: clusterId,
          label: node.label,
          keywords: [],
        });
      }
    }

    for (const edge of result.edges) {
      const source = edge.source;
      const target = edge.target;

      // keyword 연결만 처리 (source가 cl-, target이 kw-)
      const clusterId = parseInt((source as string).replace("cl-", ""));
      const keywordId = parseInt((target as string).replace("kw-", ""));
      const keywordNode = result.nodes.find((n: any) => n.id === target);
      if (!keywordNode) continue;

      const keyword = {
        id: keywordId,
        name: keywordNode.label,
        count: 1,
        clusterId,
      };

      const cluster = clusterMap.get(clusterId);
      if (cluster) {
        cluster.keywords.push(keyword);
      }
    }

    return {
      id: Date.now(), // fake ID
      clusters: Array.from(clusterMap.values()),
    };
  } catch (err) {
    console.error("지식맵 불러오기 실패", err);
    return null;
  }
}