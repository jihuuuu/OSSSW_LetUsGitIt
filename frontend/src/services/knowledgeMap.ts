// 📄 /src/services/knowledgeMap.ts
import api from "@/services/api";
// ✅ 토큰 가져오는 함수 (예: localStorage 사용)
function getAuthHeader() {
  const token = localStorage.getItem("access_token"); // 혹은 "token"
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export async function fetchLatestKnowledgeMap() {
  const res = await api.get("/users/knowledge_map/graph", getAuthHeader());
  console.log("📦 지식맵 응답 전체:", res);
  return res.data;
}

// 키워드 이름 조회
export async function fetchKeywordName(id: number) {
  const res = await api.get(`/users/keywords/${id}`);
  return res.data;
}

// 특정 키워드 관련 기사 조회
export async function fetchArticlesByKeywordCluster(keywordId: number) {
  const res = await api.get(`/users/keywords/${keywordId}/articles`);
  return res.data;
}
