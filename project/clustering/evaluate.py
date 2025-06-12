import numpy as np
from sklearn.metrics import silhouette_score
from clustering.cluster import load_embeddings, run_kmeans, run_hdbscan
from umap import UMAP

def evaluate_silhouette(
    emb_path: str,
    ks: list[int],
    method: str,
    hdbscan_min_samples: int = 10,
    umap_n_neighbors: int=10,
    umap_min_dist: float=0.02,
    umap_n_components: int=10
) -> dict[int, float]:
    """
    emb_path 에서 임베딩을 불러와서,
    각 K 대해 KMeans 클러스터링을 수행한 후 실루엣 점수를 반환.
    """
    print(">>> silhouette 평가 스크립트 시작")
    embeddings = load_embeddings(emb_path)
    print(f"▶️ loaded embeddings: {embeddings.shape}")

    # 2) UMAP 차원 축소
    reducer = UMAP(
        n_neighbors=umap_n_neighbors,
        min_dist=umap_min_dist,
        n_components=umap_n_components,
        metric="cosine",
        random_state=42
    )
    reduced = reducer.fit_transform(embeddings)  # shape: (N_docs, umap_n_components)
    print(f"▶️ reduced embeddings: {reduced.shape}")

    scores = {}
    for k in ks:
        if method == "kmeans":
            labels = run_kmeans(reduced, k)
            print(f"> KMeans: K={k}")
        else:  # hdbscan
            # run_hdbscan 출력이 np.array 형태의 labels이라고 가정
            labels = run_hdbscan(reduced, min_cluster_size=k, min_samples=hdbscan_min_samples)
            print(f"> HDBSCAN: min_cluster_size={k}, min_samples={hdbscan_min_samples}")

        # 군집이 1개 밖에 안 나왔거나 모두 노이즈(-1)인 경우 실루엣 계산 불가
        unique_labels = set(labels)
        if len(unique_labels - {-1}) <= 1:
            print(f"  - 경고: 클러스터가 충분하지 않아 silhouette을 계산할 수 없습니다 (labels={unique_labels}).")
            scores[k] = float("nan")
            continue

        score = silhouette_score(reduced, labels)
        print(f"  → silhouette={score:.4f}")
        scores[k] = score

    return scores


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="실루엣 점수 평가 스크립트")
    parser.add_argument("--emb-path", default="data/article_embeddings_768.npy")
    parser.add_argument("--ks", nargs="+", type=int, default=[5,10,15,20,25])
    parser.add_argument("--umap-n-neighbors", type=int, default=10)
    parser.add_argument("--umap-min-dist", type=float, default=0.02)
    parser.add_argument("--umap-n-components", type=int, default=10)
    parser.add_argument("--method", choices=["kmeans", "hdbscan"], default="kmeans", help="클러스터링 알고리즘 선택 (기본: kmeans)")
    parser.add_argument("--hdbscan-min-samples", type=int, default=5, help="HDBSCAN min_samples 파라미터 (기본: 5)")
    args = parser.parse_args()


    evaluate_silhouette(
        emb_path=args.emb_path,
        ks=args.ks,
        method=args.method,
        hdbscan_min_samples=args.hdbscan_min_samples,
        umap_n_neighbors=args.umap_n_neighbors,
        umap_min_dist=args.umap_min_dist,
        umap_n_components=args.umap_n_components
    )
