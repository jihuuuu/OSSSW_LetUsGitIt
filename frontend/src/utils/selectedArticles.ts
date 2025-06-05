// utils/selectedArticles.ts

export function getSelectedArticles(): number[] {
  const raw = localStorage.getItem("selectedArticleIds");
  return raw ? JSON.parse(raw) : [];
}

export function addSelectedArticle(id: number) {
  const list = getSelectedArticles();
  if (!list.includes(id)) {
    localStorage.setItem("selectedArticleIds", JSON.stringify([...list, id]));
  }
}

export function removeSelectedArticle(id: number) {
  const list = getSelectedArticles().filter((x) => x !== id);
  localStorage.setItem("selectedArticleIds", JSON.stringify(list));
}

export function clearSelectedArticles() {
  localStorage.removeItem("selectedArticleIds");
}
