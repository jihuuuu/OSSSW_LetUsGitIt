// src/services/scrap.ts
import type { ScrappedArticle } from "@/types/scrap";

/**
 * 스크랩된 기사 전체 조회 또는 키워드 검색 (최신순)
 */
export async function getScrappedArticles({
  userId,
  keyword = "",
  page,
  size,
}: {
  userId: number;
  keyword?: string;
  page: number;
  size: number;
}): Promise<{
  articles: ScrappedArticle[];
  totalPages: number;
}> {
  const params = new URLSearchParams({
    userId: String(userId),
    page: String(page),
    size: String(size),
  });

  if (keyword.trim()) {
    params.append("keyword", keyword);
  }

  const res = await fetch(`/api/scrap?${params.toString()}`);

  if (!res.ok) {
    throw new Error("스크랩된 기사 불러오기 실패");
  }

  return res.json(); // { articles, totalPages }
}

export async function getScrappedArticlesByKeyword(
  userId: number,
  keyword: string,
  page: number,
  size: number
): Promise<{
  articles: ScrappedArticle[];
  totalPages: number;
}> {
  const res = await fetch(
    `/api/scrap?userId=${userId}&keyword=${encodeURIComponent(keyword)}&page=${page}&size=${size}`
  );

  if (!res.ok) {
    throw new Error("스크랩된 기사 불러오기 실패");
  }

  return res.json(); // { articles, totalPages }
}