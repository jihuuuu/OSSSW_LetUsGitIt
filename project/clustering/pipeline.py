# clustering/pipeline.py
from typing import List
from clustering.embedder import make_embeddings
from database.connection import SessionLocal
from models.article import Article
import numpy as np
import argparse
from collections import Counter
from clustering.embedder import make_embeddings
from clustering.cluster import (
    load_embeddings,
    run_kmeans,
    run_dbscan,
    save_labels_to_db,
    fetch_article_ids,
)
from clustering.keyword_extractor import extract_keywords_per_cluster

def fetch_all_texts(limit: int | None = None) -> List[str]:
    """
    DB에서 분석할 기사 텍스트(제목+요약)를 모두 꺼냅니다.
    limit을 주면 최근 N건만.
    """
    session = SessionLocal()
    try:
        query = session.query(Article.title, Article.summary)
        if limit:
            query = query.order_by(Article.fetched_at.desc()).limit(limit)
        rows = query.all()
        # 제목과 요약을 합쳐 하나의 텍스트로
        texts = [f"{t.title} {t.summary or ''}".strip() for t in rows]
        return texts
    finally:
        session.close()

def run_embedding_stage(limit: int | None = None, batch_size: int = 32):
    """
    1) DB에서 기사 텍스트 불러오기
    2) 임베딩 생성
    3) (선택) 파일로 저장하거나 다음 단계에 반환
    """
    texts = fetch_all_texts(limit=limit)
    if not texts:
        print("⚠️ 분석할 기사 텍스트가 없습니다.")
        return None

    print(f"▶️ {len(texts)}개 기사에 대해 임베딩 생성 시작…")
    embeddings = make_embeddings(texts, batch_size=batch_size)
    print("✅ 임베딩 생성 완료:", embeddings.shape)
    
    # 예: 파일로 저장 (옵션)
    np.save("data/article_embeddings.npy", embeddings)
    print("✅ embeddings.npy 저장 완료")

    return embeddings

def run_clustering_stage(
    emb_path: str,
    method: str,
    n_clusters: int | None,
    eps: float | None,
    min_samples: int | None,
    limit: int | None,
    save_db: bool,
):
    # 1) 임베딩 로드
    embeddings = load_embeddings(emb_path)
    print(f"▶️ loaded embeddings: {embeddings.shape}")

    # 2) 클러스터링 수행
    if method == "kmeans":
        labels = run_kmeans(embeddings, n_clusters)
    else:
        labels = run_dbscan(embeddings, eps, min_samples)

    # 3) 클러스터 요약 출력
    counts = Counter(labels)
    print("클러스터 요약:")
    for lbl, cnt in counts.items():
        print(f"  - Cluster {lbl}: {cnt} articles")

    # 4) 대표 키워드 추출
    texts = fetch_all_texts(limit=limit)
    keywords = extract_keywords_per_cluster(texts, labels, top_n=3)
    print("\n대표 키워드 (클러스터별):")
    for lbl, kws in keywords.items():
        print(f"  - Cluster {lbl}: {', '.join(kws)}")

    # 5) DB에 저장
    if save_db:
        article_ids = fetch_article_ids(limit=limit)
        if len(article_ids) != len(labels):
            print("⚠️ 오류: Article ID 수와 임베딩 수가 일치하지 않습니다.")
            return
        save_labels_to_db(article_ids, labels)


def main():
    parser = argparse.ArgumentParser(description="뉴스 파이프라인: 임베딩 및 클러스터링")
    # 클러스터링 관련 인자만 유지
    parser.add_argument("--method", choices=["kmeans", "dbscan"], default="kmeans", help="클러스터링 알고리즘 선택")
    parser.add_argument("--n-clusters", type=int, default=10, help="KMeans 클러스터 수")
    parser.add_argument("--eps", type=float, default=0.5, help="DBSCAN eps 파라미터")
    parser.add_argument("--min-samples", type=int, default=5, help="DBSCAN min_samples 파라미터")
    parser.add_argument("--limit", type=int, help="최근 N건만 처리")
    parser.add_argument("--save-db", action="store_true", help="DB에 클러스터 라벨 저장")

    args = parser.parse_args()

    # 1) 임베딩 단계 수행 (항상 실행)
    embs = run_embedding_stage(limit=args.limit, batch_size=32)
    if embs is None:
        return
    
    # 2) 클러스터링 단계 수행
    run_clustering_stage(
        emb_path="data/article_embeddings.npy",
        method=args.method,
        n_clusters=args.n_clusters,
        eps=args.eps,
        min_samples=args.min_samples,
        limit=args.limit,
        save_db=args.save_db,
    )


if __name__ == "__main__":
    main()
