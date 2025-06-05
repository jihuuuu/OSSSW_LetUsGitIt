// utils/scrapArticles.ts
const STORAGE_KEY = "scrappedArticleIds";

export function getScrappedArticles(): number[] {
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : [];
}

export function addScrappedArticle(id: number) {
  const list = getScrappedArticles();
  if (!list.includes(id)) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...list, id]));
  }
}

export function removeScrappedArticle(id: number) {
  const list = getScrappedArticles().filter((x) => x !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

export function clearScrappedArticles() {
  localStorage.removeItem(STORAGE_KEY);
}
