# clustering/pipeline_by_topic.py

import argparse
import numpy as np
from typing import Dict, List, Optional
from models.topic import TopicEnum
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from clustering.embedder import STOPWORDS_KO
from clustering.cache_redis import load_embedding_cache
from clustering.running_stage import (
    run_embedding_stage,
    run_clustering_stage,
    run_keyword_extraction
)


def run_all_topics_pipeline(
    clustering_method: str = "kmeans",
    k: Optional[int] = 10,
    eps: Optional[float] = None,
    min_samples: Optional[int] = None,
    since_hours: Optional[int] = 24,
    data_dir: str = "data",
    save_db : bool = False,
):
    # 토픽별 커스텀 파라미터 맵 (필요한 만큼 추가/수정)
    topic_params: Dict[TopicEnum, Dict[str, float]] = {
        TopicEnum.정치:   {"k": 12},
        TopicEnum.경제: {"k": 10},
        TopicEnum.스포츠:   {"k": 24},
        TopicEnum.국제: {"k": 7},
        TopicEnum.문화:   {"k": 28},
        TopicEnum.사회: {"k": 18}
        # 나머지 토픽은 args 기본값 사용
    }

    """
    모든 토픽 순회하며 순차적으로 임베딩, 클러스터링, 키워드 추출 단계를 실행합니다.
    """
    for topic in TopicEnum:
        # 기본값과 오버라이드를 합침
        base = {"k": k, "eps": eps, "min_samples": min_samples}
        override = topic_params.get(topic, {})
        params = {**base, **override}
        
        print(f"\n===== [{topic.value}] 파이프라인 시작 =====")

        # 1) 임베딩 단계
        emb_result = run_embedding_stage(
            topic=topic,
            since_hours=since_hours,
            data_dir=data_dir,
            batch_size=32
        )
        if emb_result is None:
            print(f"----- [{topic.value}] 임베딩 단계 건너뜀 -----")
            continue

        emb_array, ids_window, raw_texts, cleaned_texts = emb_result

        # emb_path 생성 (토픽별 .npy 임베딩 파일 경로)
        # emb_path = os.path.join(data_dir, f"{topic.value}_embs_768.npy")

        # --- 글로벌 IDF 학습 (전체 말뭉치) ---
        global_vec = TfidfVectorizer(
            stop_words=list(STOPWORDS_KO),
            max_features=300,      # 필요에 따라 조정
            min_df=0.02,
            max_df=1.0,
            use_idf=True,
            smooth_idf=True,
            sublinear_tf=True,
            norm='l2'
        )
        global_vec.fit(cleaned_texts)

        labels, cluster_to_docs, label_to_cluster_id = run_clustering_stage(
            embeddings=emb_array,
            ids_window=ids_window,
            raw_texts=raw_texts,
            cleaned_texts=cleaned_texts,
            method=clustering_method,
            n_clusters=params["k"],
            eps=params["eps"],
            min_samples=params["min_samples"],
            topic=topic,
            save_db=save_db
        )

        # 3) 키워드 추출 단계
        kw_map = run_keyword_extraction(
            cluster_to_docs=cluster_to_docs,
            label_to_cluster_id=label_to_cluster_id,
            top_n=3,
            save_db=save_db,
            global_vectorizer=global_vec
        )
        for lbl, kws in kw_map.items():
            print(f"  Cluster {lbl} 키워드: {', '.join(kws)}")

        print(f"===== [{topic.value}] 파이프라인 완료 =====\n")


def main():
    parser = argparse.ArgumentParser(description="뉴스 클러스터링 & 키워드 파이프라인")
    parser.add_argument("--method", choices=["kmeans", "dbscan", "hdbscan"], default="kmeans",
                        help="클러스터링 알고리즘 선택 (default: kmeans)")
    parser.add_argument("--n-clusters", type=int, default=10,
                        help="KMeans 클러스터 수 (HDBSCAN 사용 시에는 --min-cluster-size 사용, 기본값: 10)")
    parser.add_argument("--eps", type=float, default=0.5,
                        help="DBSCAN eps 파라미터 (default: 0.5)")
    parser.add_argument("--min-samples", type=int, default=10,
                        help="DBSCAN/HDBSCAN min_samples 파라미터 (default: 10)")
    parser.add_argument("--since-hours", type=int, default=24,
                        help="최근 N시간 내 기사만 처리 (default: 24)")
    parser.add_argument("--data-dir", type=str, default="data",
                        help="임베딩 캐시 저장 디렉토리 (default: data)")
    parser.add_argument("--save-db", action="store_true", default=False,
                        help="DB에 저장하려면 이 옵션을 추가")
    args = parser.parse_args()

    run_all_topics_pipeline(
        clustering_method=args.method,
        k=args.n_clusters,
        eps=args.eps,
        min_samples=args.min_samples,
        since_hours=args.since_hours,
        data_dir=args.data_dir,
        save_db=args.save_db
    )


if __name__ == "__main__":
    main()
