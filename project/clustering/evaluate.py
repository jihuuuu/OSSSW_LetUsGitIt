import numpy as np
from sklearn.metrics import silhouette_score
from clustering.cluster import load_embeddings, run_kmeans

def evaluate_silhouette(
    emb_path: str,
    ks: list[int],
) -> dict[int, float]:
    """
    emb_path 에서 임베딩을 불러와서,
    각 K 대해 KMeans 클러스터링을 수행한 후 실루엣 점수를 반환.
    """
    print(">>> silhouette 평가 스크립트 시작")

    embeddings = load_embeddings(emb_path)
    scores = {}
    for k in ks:
        labels = run_kmeans(embeddings, k)
        score = silhouette_score(embeddings, labels)
        print(f"K={k} → silhouette={score:.4f}")
        scores[k] = score
    return scores

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--emb-path", default="data/article_embeddings.npy")
    parser.add_argument("--ks", nargs="+", type=int, default=[5,10,15,20,25])
    args = parser.parse_args()

    evaluate_silhouette(args.emb_path, args.ks)
