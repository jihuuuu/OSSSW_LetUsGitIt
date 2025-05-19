# clustering/cluster.py

import argparse
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from collections import Counter
from database.connection import SessionLocal
from models.article import Article  # Article.title+summary

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

def save_labels_to_db(article_ids: list[int], labels: np.ndarray):
    """
    Article 테이블에 cluster_label 컬럼이 있다고 가정하고,
    해당 필드를 업데이트합니다.
    """
    session = SessionLocal()
    try:
        for art_id, label in zip(article_ids, labels):
            session.query(Article).filter(Article.id == art_id).update({
                Article.cluster: int(label)
            })
        session.commit()
        print("✅ DB에 클러스터 라벨을 저장했습니다.")
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
