# clustering/cluster.py

import argparse
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from collections import Counter
from database.connection import SessionLocal
from models.article import Cluster
from models.article import ClusterArticle
from models.article import Article

def load_embeddings(path: str) -> np.ndarray:
    """
    NumPy 파일(.npy)에서 임베딩 벡터를 불러옴
    """
    return np.load(path)

def fetch_article_ids(limit: int | None = None) -> list[int]:
    """
    DB에서 최근 순으로 Article.id 를 가져옵니다.
    임베딩 saved 순서와 일치해야 합니다.
    """
    session = SessionLocal()
    try:
        query = session.query(Article.id).order_by(Article.fetched_at.desc())
        if limit:
            query = query.limit(limit)
        ids = [r[0] for r in query.all()]
        return ids
    finally:
        session.close()

def run_kmeans(embeddings: np.ndarray, n_clusters: int) -> np.ndarray:
    """
    KMeans 로 클러스터링 수행하고 각 샘플의 레이블을 반환합니다.
    """
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(embeddings)
    return labels

def run_dbscan(embeddings: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    """
    DBSCAN 으로 클러스터링 수행하고 각 샘플의 레이블을 반환합니다.
    """
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(embeddings)
    return labels

def save_clusters_to_db(article_ids: list[int], labels: np.ndarray):
    """
    npy나 run_clustering_stage 결과를 바탕으로
    Cluster 테이블과 ClusterArticle 매핑 테이블에
    클러스터 결과를 저장합니다.
    """
    session = SessionLocal()
    try:
        # 1) 레이블별 Cluster 레코드 생성
        label_to_cluster_id: dict[int, int] = {}
        for lbl in sorted(set(labels)):
            cluster = Cluster(label=int(lbl), num_articles=0)
            session.add(cluster)
            session.flush()  # cluster.id 채워짐
            label_to_cluster_id[int(lbl)] = cluster.id

        # 2) 매핑 테이블에 Article ↔ Cluster 연결
        mappings = []
        for art_id, lbl in zip(article_ids, labels):
            cid = label_to_cluster_id[int(lbl)]
            mappings.append(
                ClusterArticle(article_id=art_id, cluster_id=cid)
            )
            # 각 Cluster.num_articles 카운트
            # (원한다면 나중에 업데이트하거나, bulk로 처리 가능)
        session.bulk_save_objects(mappings)

        # 3) num_articles 업데이트 (선택)
        for lbl, cid in label_to_cluster_id.items():
            count = labels.tolist().count(lbl)
            session.query(Cluster).filter(Cluster.id == cid).update({
                Cluster.num_articles: count
            })

        session.commit()
        print("✅ Cluster 테이블과 매핑 테이블에 저장 완료")
    finally:
        session.close()

def print_cluster_summary(labels: np.ndarray):
    """
    각 클러스터별로 몇 개의 샘플이 있는지 출력합니다.
    """
    counts = Counter(labels)
    print("클러스터 요약:")
    for label, cnt in counts.items():
        print(f"  - Cluster {label}: {cnt} articles")
