import os
import argparse
from typing import Optional, Dict
from collections import defaultdict

from models.topic import TopicEnum
from clustering.running_stage import run_embedding_stage, run_clustering_stage
from clustering.keyword_extractor import extract_top_keywords
from database.connection import SessionLocal
from models.article import Article

def inspect_cluster_article_list(
    topic: TopicEnum,
    method: str = "kmeans",
    n_clusters: Optional[int] = 10,
    eps: Optional[float] = 0.5,
    min_samples: Optional[int] = 5,
    since_hours: int = 24,
    data_dir: str = "data",
    random_state: int = 42,
    top_kws: int = 3
) -> None:
    """
    실험용: 각 토픽별 클러스터 안의 기사 리스트와 키워드를 출력합니다.

    매개변수:
    - topic: TopicEnum 멤버 (예: TopicEnum.정치)
    - method: "kmeans", "dbscan", "hdbscan"
    - n_clusters: KMeans 클러스터 수 또는 HDBSCAN의 min_cluster_size
    - eps: DBSCAN eps 파라미터
    - min_samples: DBSCAN/HDBSCAN min_samples 파라미터
    - since_hours: 최근 N시간 내 기사 사용
    - data_dir: 임베딩 캐시 디렉토리
    - random_state: 난수 시드
    - top_kws: 각 클러스터별 추출할 키워드 수
    """
    # 1) 임베딩 생성 또는 로드
    result = run_embedding_stage(
        topic=topic,
        since_hours=since_hours,
        data_dir=data_dir,
        batch_size=32
    )
    if result is None:
        print(f"♨️ [{topic.value}] 기사 없음 → 스킵")
        return

    final_embs, ids_window, raw_texts, cleaned_texts = result

    emb_path = os.path.join(data_dir, f"{topic.value}_embs_768.npy")

    # 2) 클러스터링
    labels, cluster_to_docs, _ = run_clustering_stage(
        emb_path=emb_path,
        ids_window=ids_window,
        raw_texts=raw_texts,
        cleaned_texts=cleaned_texts,
        method=method,
        n_clusters=n_clusters,
        eps=eps,
        min_samples=min_samples,
        topic=topic,
        save_db=False,
        top_kws=top_kws
    )

    # 3) 클러스터별 ID 수집
    cluster_to_ids: Dict[int, list] = defaultdict(list)
    for idx, lbl in enumerate(labels):
        cluster_to_ids[lbl].append(ids_window[idx])

    # DB 세션 생성
    session = SessionLocal()

    print("── 클러스터 별 기사 제목 및 키워드 ──")
    for lbl, id_list in cluster_to_ids.items():
        docs = [d for d in cluster_to_docs.get(lbl, []) if d]
        kws_str = ", ".join(extract_top_keywords(documents=docs, cluster_id=lbl, top_n=top_kws)) if docs else "키워드 없음"

        print(f"Cluster {lbl} ({len(id_list)}개 문서) – 키워드: {kws_str}")
        for aid in id_list:
            article = session.query(Article).filter(Article.id == aid).first()
            title = article.title if article else f"[ID: {aid}] DB에 없음"
            print(f"   ▶ {title}")
        print()

    session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="토픽별 클러스터 기사 리스트 출력 스크립트")
    parser.add_argument("--method", "-m", choices=["kmeans", "dbscan", "hdbscan"], default="kmeans", help="클러스터링 방법")
    parser.add_argument("--n_clusters", "-k", type=int, default=10, help="클러스터 개수 또는 min_cluster_size")
    parser.add_argument("--eps", "-e", type=float, default=0.5, help="DBSCAN eps 파라미터")
    parser.add_argument("--min_samples", "-s", type=int, default=10, help="DBSCAN/HDBSCAN min_samples 파라미터")
    parser.add_argument("--since_hours", "-t", type=int, default=24, help="최근 N시간 내 기사 사용")
    parser.add_argument("--data_dir", "-d", type=str, default="data", help="임베딩 캐시 디렉토리")
    parser.add_argument("--random_state", "-r", type=int, default=42, help="난수 시드")

    args = parser.parse_args()
    for topic in TopicEnum:
        print(f"\n===== [{topic.value}] 출력 시작 ({args.method}) =====")
        inspect_cluster_article_list(
            topic=topic,
            method=args.method,
            n_clusters=args.n_clusters,
            eps=args.eps,
            min_samples=args.min_samples,
            since_hours=args.since_hours,
            data_dir=args.data_dir,
            random_state=args.random_state,
            top_kws=3
        )
