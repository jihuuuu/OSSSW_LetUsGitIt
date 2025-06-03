import os
import argparse
from typing import Optional, List, Tuple, Dict
import numpy as np
from sklearn.metrics import silhouette_score
from umap import UMAP
from models.topic import TopicEnum
from clustering.running_stage import run_embedding_stage
from clustering.cluster import run_kmeans, run_dbscan, run_hdbscan

def compute_silhouette_for_topic(
    topic: TopicEnum,
    method: str = "kmeans",
    n_clusters: Optional[int] = 10,
    eps: Optional[float] = 0.5,
    min_samples: Optional[int] = 5,
    since_hours: int = 24,
    data_dir: str = "data",
    random_state: int = 42
) -> None:
    """
    1) run_embedding_stage를 호출해 SBERT 임베딩을 만들거나 캐시에서 로드
    2) UMAP으로 차원 축소 (768 → 10)
    3) run_kmeans/run_dbscan/run_hdbscan를 직접 호출해 레이블 생성
    4) Silhouette 점수 계산 및 출력

    - topic: TopicEnum 멤버 (예: TopicEnum.정치)
    - method: "kmeans", "dbscan", "hdbscan" 중 하나
    - n_clusters: KMeans 클러스터 수 또는 HDBSCAN의 min_cluster_size
    - eps: DBSCAN eps 파라미터
    - min_samples: DBSCAN/HDBSCAN min_samples 파라미터
    """

    # 1) run_embedding_stage 호출 → (final_embs, ids_window, raw_texts, cleaned_texts) 반환
    result = run_embedding_stage(
        topic=topic,
        since_hours=since_hours,
        data_dir=data_dir,
        batch_size=32
    )
    if result is None:
        print(f"♨️ [{topic.value}] 기사 없음 → Silhouette 계산 스킵")
        return

    final_embs, ids_window, raw_texts, cleaned_texts = result

    # 2) UMAP 차원 축소 (768 → 10)
    reducer = UMAP(
        n_neighbors=5,
        min_dist=0.02,
        n_components=10,
        metric="cosine",
        random_state=random_state
    )
    emb_reduced = reducer.fit_transform(final_embs)
    print(f"▶️ [{topic.value}] 차원 축소 완료: {emb_reduced.shape}")

    # 3) 클러스터링 수행
    if method == "kmeans":
        if n_clusters is None:
            raise ValueError("KMeans를 사용할 때는 n_clusters를 지정해야 합니다.")
        labels = run_kmeans(emb_reduced, n_clusters)
    elif method == "dbscan":
        if eps is None or min_samples is None:
            raise ValueError("DBSCAN을 사용할 때는 eps와 min_samples를 모두 지정해야 합니다.")
        labels = run_dbscan(emb_reduced, eps=eps, min_samples=min_samples)
    elif method == "hdbscan":
        if n_clusters is None or min_samples is None:
            raise ValueError("HDBSCAN을 사용할 때는 min_cluster_size(n_clusters)와 min_samples를 지정해야 합니다.")
        labels = run_hdbscan(emb_reduced, min_cluster_size=n_clusters, min_samples=min_samples)
    else:
        raise ValueError(f"지원하지 않는 클러스터링 방법: {method}")

    # 4) Silhouette 점수 계산 가능 여부 체크
    unique_labels = set(labels.tolist())
    # 클러스터가 1개이거나, 노이즈(-1)만 하나 있는 경우 계산 불가
    if len(unique_labels) <= 1 or (len(unique_labels) == 2 and -1 in unique_labels):
        print(f"⚠ [{topic.value}] 유효 클러스터 레이블 부족 → Silhouette 계산 불가")
        return

    score = silhouette_score(emb_reduced, labels, metric="cosine")
    print(f"✅ [{topic.value}] Silhouette Score ({method}): {score:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="토픽별 Silhouette 점수 계산 스크립트")
    parser.add_argument("--method", "-m", choices=["kmeans", "dbscan", "hdbscan"], default="kmeans", help="클러스터링 방법 (kmeans, dbscan, hdbscan)")
    parser.add_argument("--n_clusters", "-k", type=int, default=10, help="KMeans 클러스터 개수 또는 HDBSCAN의 min_cluster_size")
    parser.add_argument("--eps", "-e", type=float, default=0.5, help="DBSCAN eps 파라미터")
    parser.add_argument("--min_samples", "-s", type=int, default=5, help="DBSCAN/HDBSCAN min_samples 파라미터")
    parser.add_argument("--since_hours", "-t", type=int, default=24, help="최근 N시간 이내 기사만 사용 (기본: 24시간)")
    parser.add_argument("--data_dir", "-d", type=str, default="data", help="임베딩 캐시가 저장된 디렉토리")
    parser.add_argument("--random_state", "-r", type=int, default=42, help="난수 시드")

    args = parser.parse_args()

    for topic in TopicEnum:
        print(f"\n===== [{topic.value}] Silhouette 계산 시작 ( {args.method} )=====")
        compute_silhouette_for_topic(
            topic=topic,
            method=args.method,
            n_clusters=args.n_clusters,
            eps=args.eps,
            min_samples=args.min_samples,
            since_hours=args.since_hours,
            data_dir=args.data_dir,
            random_state=args.random_state
        )
