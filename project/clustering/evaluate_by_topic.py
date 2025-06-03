import os
import argparse
from typing import Optional, List, Tuple, Dict
import numpy as np
from sklearn.metrics import silhouette_score
from umap import UMAP
from models.topic import TopicEnum
from clustering.running_stage import run_embedding_stage, run_clustering_stage
from clustering.keyword_extractor import extract_top_keywords


def compute_silhouette_for_topic(
    topic: TopicEnum, method: str = "kmeans", n_clusters: Optional[int] = 10,
    eps: Optional[float] = 0.5, min_samples: Optional[int] = 5,
    umap_n_neighbors: int = 5, umap_min_dist: float = 0.1, since_hours: int = 24, 
    data_dir: str = "data", random_state: int = 42, top_kws: int = 3
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
        topic=topic, since_hours=since_hours,
        data_dir=data_dir, batch_size=32
    )
    if result is None:
        print(f"♨️ [{topic.value}] 기사 없음 → Silhouette 계산 스킵")
        return

    final_embs, ids_window, raw_texts, cleaned_texts = result

    emb_path = os.path.join(data_dir, f"{topic.value}_embs_768.npy")

    # 2) 클러스터링 + 내부 UMAP (save_db=False)
    labels, cluster_to_docs, label_to_cluster_id = run_clustering_stage(
        emb_path=emb_path, ids_window=ids_window, raw_texts=raw_texts,
        cleaned_texts=cleaned_texts, method=method, n_clusters=n_clusters,
        eps=eps, min_samples=min_samples, topic=topic,
        save_db=False,                           # DB에 저장하지 않음
        umap_n_neighbors=umap_n_neighbors,       # 내부 UMAP 튜닝 파라미터
        umap_min_dist=umap_min_dist,             # 내부 UMAP 튜닝 파라미터
        top_kws=top_kws
    )

    reducer = UMAP(
        n_neighbors=umap_n_neighbors,
        min_dist=umap_min_dist,
        n_components=10,
        metric="cosine",
        random_state=random_state
    )
    emb_reduced = reducer.fit_transform(final_embs)

    # 4) Silhouette 점수 계산 가능 여부 체크
    unique_labels = set(labels.tolist())
    # 클러스터가 1개이거나, 노이즈(-1)만 하나 있는 경우 계산 불가
    if len(unique_labels) <= 1 or (len(unique_labels) == 2 and -1 in unique_labels):
        print(f"⚠ [{topic.value}] 유효 클러스터 레이블 부족 → Silhouette 계산 불가")
        return

    score = silhouette_score(emb_reduced, labels, metric="cosine")
    print(f"✅ [{topic.value}] Silhouette Score ({method}): {score:.4f}")

    # 5) 키워드 추출 
    print("— 키워드 추출 결과 —")
    for lbl, docs in cluster_to_docs.items():
        # (1) 문장 전처리: None이나 빈 문자열 걸러내기
        docs = [d for d in docs if d and isinstance(d, str)]
        if not docs:
            print(f"  Cluster {lbl}: 문서가 없어 키워드 생략")
            continue

        # (2) TF-IDF 키워드 추출
        kws = extract_top_keywords(documents=docs, top_n=top_kws)
        print(f"  Cluster {lbl}: {', '.join(kws)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="토픽별 Silhouette 점수 계산 스크립트")
    parser.add_argument("--method", "-m", choices=["kmeans", "dbscan", "hdbscan"], default="kmeans", help="클러스터링 방법 (kmeans, dbscan, hdbscan)")
    parser.add_argument("--n_clusters", "-k", type=int, default=10, help="KMeans 클러스터 개수 또는 HDBSCAN의 min_cluster_size")
    parser.add_argument("--eps", "-e", type=float, default=0.5, help="DBSCAN eps 파라미터")
    parser.add_argument("--min_samples", "-s", type=int, default=10, help="DBSCAN/HDBSCAN min_samples 파라미터")
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
