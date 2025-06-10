import argparse
import logging
import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from clustering.running_stage import run_embedding_stage, run_clustering_stage
from clustering.keyword_extractor import extract_top_keywords
from models.topic import TopicEnum
from scipy import sparse


# 기본 data 디렉토리
DATA_DIR = 'data'

# 토픽별 클러스터링 파라미터 오버라이드
topic_params = {
    TopicEnum.정치: {"n_clusters": 12},
    TopicEnum.경제: {"n_clusters": 10},
    TopicEnum.스포츠: {"n_clusters": 24},
    TopicEnum.국제: {"n_clusters": 7},
    TopicEnum.문화: {"n_clusters": 28},
    TopicEnum.사회: {"n_clusters": 18}
}

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# --- TF-IDF 집중도 지표 함수 ---
def herfindahl_index(feature_matrix: np.ndarray) -> float:
    weights = feature_matrix.sum(axis=0)
    total = weights.sum()
    if total == 0:
        return 0.0
    p = weights / total
    return float((p ** 2).sum())

def entropy_index(feature_matrix: np.ndarray) -> float:
    weights = feature_matrix.sum(axis=0)
    total = weights.sum()
    if total == 0:
        return 0.0
    p = weights / total
    # epsilon to avoid log(0)
    return float((-p * np.log(p + 1e-12)).sum())

def gini_coefficient(feature_matrix: np.ndarray) -> float:
    weights = np.sort(feature_matrix.sum(axis=0))
    n = weights.size
    cum = np.cumsum(weights)
    if cum[-1] == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return float(( (2 * index - n - 1) * weights ).sum() / (n * cum[-1]))

def top_k_ratio(feature_matrix: np.ndarray, k: int) -> float:
    weights = feature_matrix.sum(axis=0)
    total = weights.sum()
    if total == 0:
        return 0.0
    topk = np.sort(weights)[-k:]
    return float(topk.sum() / total)


def evaluate_concentration(tfidf_matrix, labels, k: int) -> dict:
    X = tfidf_matrix.toarray() if sparse.issparse(tfidf_matrix) else tfidf_matrix
    res = {}
    for lbl in np.unique(labels):
        idx = np.where(labels == lbl)[0]
        cluster_mat = X[idx]
        res[int(lbl)] = {
            'HHI': herfindahl_index(cluster_mat),
            'Entropy': entropy_index(cluster_mat),
            'Gini': gini_coefficient(cluster_mat),
            f'Top{k}_Ratio': top_k_ratio(cluster_mat, k)
        }
    return res

# --- 스크립트 진입점 ---
def main():
    parser = argparse.ArgumentParser(description="모든 토픽 키워드 평가 스크립트")
    parser.add_argument('--method', choices=['kmeans','dbscan','hdbscan'], default='kmeans', help='클러스터링 알고리즘')
    parser.add_argument('--n_clusters', '-k', type=int, default=20, help='클러스터 개수 또는 min_cluster_size')
    parser.add_argument('--eps', type=float, default=None, help='DBSCAN/HDBSCAN eps')
    parser.add_argument('--min_samples', type=int, default=None, help='DBSCAN/HDBSCAN min_samples')
    parser.add_argument('--umap_n_neighbors', type=int, default=15, help='UMAP n_neighbors')
    parser.add_argument('--umap_min_dist', type=float, default=0.1, help='UMAP min_dist')
    parser.add_argument('--top_n', type=int, default=3, help='대표 키워드 수')
    parser.add_argument('--max_features', type=int, default=300, help='TF-IDF max_features')
    parser.add_argument('--min_df', type=float, default=0.02, help='TF-IDF min_df')
    parser.add_argument('--max_df', type=float, default=1.0, help='TF-IDF max_df')
    parser.add_argument('--smooth_idf', action='store_true', help='TF-IDF smooth_idf')
    parser.add_argument('--sublinear_tf', action='store_true', help='TF-IDF sublinear_tf')
    parser.add_argument('--norm', choices=['l1','l2',None], default='l2', help='TF-IDF norm')
    args = parser.parse_args()

    all_results = {}
    for topic in TopicEnum:

        # 토픽별 파라미터 오버라이드 병합
        override = topic_params.get(topic, {})
        n_clusters = override.get('n_clusters', args.n_clusters)
        eps = override.get('eps', args.eps)
        min_samples = override.get('min_samples', args.min_samples)

        # 1) 임베딩 생성/로딩 + 전처리
        emb_res = run_embedding_stage(
            topic=topic, since_hours=24,
            data_dir=DATA_DIR, batch_size=32
        )
        if emb_res is None:
            logger.warning(f'[{topic.value}] 기사 없음, 스킵')
            continue
        final_embs, ids_window, raw_texts, cleaned_texts = emb_res

        # 2) 클러스터링
        emb_path = os.path.join(DATA_DIR, f'{topic.value}_embs_768.npy')
        labels, cluster_to_docs, label_to_cluster_id = run_clustering_stage(
            emb_path=emb_path,
            ids_window=ids_window,
            raw_texts=raw_texts,
            cleaned_texts=cleaned_texts,
            method=args.method,
            n_clusters=n_clusters,
            eps=eps,
            min_samples=min_samples,
            topic=topic,
            save_db=False,
            umap_n_neighbors=args.umap_n_neighbors,
            umap_min_dist=args.umap_min_dist
        )
        logger.info(f'[{topic.value}] 클러스터링 완료: {len(np.unique(labels))} clusters')


        # 3) 글로벌 IDF 학습
        global_vec = TfidfVectorizer(
            max_features=args.max_features,
            min_df=args.min_df,
            max_df=args.max_df,
            use_idf=True,
            smooth_idf=args.smooth_idf,
            sublinear_tf=args.sublinear_tf,
            norm=args.norm
        )
        global_vec.fit(cleaned_texts)

        # 4) 클러스터별 로컬 TF × 글로벌 IDF 및 키워드 추출
        for lbl in np.unique(labels):
            docs = [d for d in cluster_to_docs[lbl] if d and isinstance(d, str)]
            print(f"[{topic.value}] Cluster {lbl}")
            if not docs:
                metrics = {'HHI':0.0, 'Entropy':0.0, 'Gini':0.0, f'Top{args.top_n}_Ratio':0.0}
                print(json.dumps({topic.value: {int(lbl): {'keywords':'','metrics':metrics}}}, ensure_ascii=False))
                continue
            # 키워드 추출
            kws = extract_top_keywords(documents=docs, cluster_id=lbl, top_n=args.top_n, max_features=args.max_features, global_vectorizer=global_vec)
            # 로컬 TF × 글로벌 IDF
            tfidf_local = global_vec.transform(docs)
            X_local = tfidf_local.toarray() if sparse.issparse(tfidf_local) else tfidf_local
            # 지표 계산
            hhi = herfindahl_index(X_local)
            entro = entropy_index(X_local)
            gini = gini_coefficient(X_local)
            top_ratio = top_k_ratio(X_local, args.top_n)
            # 바로 출력
            print(f"  Keywords: {', '.join(kws)}")
            print(f"  HHI: {hhi:.4f}")
            print(f"  Entropy: {entro:.4f}")
            print(f"  Gini: {gini:.4f}")
            print(f"  Top{args.top_n}_Ratio: {top_ratio:.4f}")

if __name__ == '__main__':
    main()