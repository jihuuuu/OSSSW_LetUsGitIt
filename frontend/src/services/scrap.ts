// ✅ src/services/scrap.ts
import api from "./api";
import type { ScrappedArticle } from "@/types/scrap";

export async function getScrappedArticles({
  keyword = "",
  page,
  size,
}: {
  keyword?: string;
  page: number;
  size: number;
}): Promise<{
  articles: ScrappedArticle[];
  totalPages: number;
}> {
  const res = await api.get("/users/scraps", {
    params: { keyword, page, size },
  });
  return res.data;
}  

export async function getScrappedArticlesByKeyword(keyword: string, page: number, size: number) {
  const res = await api.get("/users/scraps", {
    params: { keyword, page, size },
  });
  return res.data;
}
