# clustering/pipeline.py
from typing import List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.article import Article, Cluster, ClusterKeyword, Keyword
import numpy as np
import argparse
from collections import Counter
from clustering.keyword_extractor import extract_keywords_per_cluster
from clustering.cache import load_embedding_cache, save_embedding_cache
from clustering.embedder import make_embeddings
from clustering.cluster import (
    load_embeddings,
    run_kmeans,
    run_dbscan,
    save_clusters_to_db,
    fetch_article_ids,
)
from clustering.keyword_extractor import extract_keywords_per_cluster


# 1) 임베딩용: (id, text) 튜플 반환
def fetch_texts_with_ids(limit: int | None = None, since_hours: int | None = None):
    session = SessionLocal()
    try:
        q = session.query(Article.id, Article.title, Article.summary)
        if since_hours is not None:
            cutoff = datetime.utcnow() - timedelta(hours=since_hours)
            q = q.filter(Article.published >= cutoff)
        if limit:
            q = q.order_by(Article.fetched_at.desc()).limit(limit)
        rows = q.all()
    finally:
        session.close()
    return [(aid, f"{title} {summary or ''}".strip()) for aid, title, summary in rows]

# 2) 클러스터링&키워드용: 순수 문자열 리스트 반환
def fetch_all_texts(limit: int | None = None, since_hours: int | None = None) -> list[str]:
    session = SessionLocal()
    try:
        q = session.query(Article.title, Article.summary)
        if since_hours is not None:
            cutoff = datetime.utcnow() - timedelta(hours=since_hours)
            q = q.filter(Article.published >= cutoff)
        if limit:
            q = q.order_by(Article.fetched_at.desc()).limit(limit)
        rows = q.all()
    finally:
        session.close()
    return [f"{t.title} {t.summary or ''}".strip() for t in rows]


def run_embedding_stage(
    *,
    batch_size: int = 32,
    since_hours: int = 24,
    id_path: str = "data/article_ids.npy",
    emb_path: str = "data/article_embeddings.npy",
):
    # 1) 지난 since_hours 기사와 텍스트
    rows = fetch_texts_with_ids(since_hours=since_hours)
    if not rows:
        print("⚠️ 분석할 기사 텍스트가 없습니다.")
        return None

    ids_window, texts_window = zip(*rows)
    ids_window = list(ids_window)
    texts_window = list(texts_window)

    # 2) 기존 캐시 로드
    cached_ids, cached_embs = load_embedding_cache(id_path, emb_path)

    # 3) 최신 윈도우 내에서 재사용 가능한 인덱스
    reused_embs = []
    new_texts = []
    new_ids = []
    for aid, txt in zip(ids_window, texts_window):
        if aid in cached_ids:
            idx = int(np.where(cached_ids == aid)[0][0])
            reused_embs.append(cached_embs[idx])
        else:
            new_ids.append(aid)
            new_texts.append(txt)

    # 4) 새로운 임베딩 생성
    if new_texts:
        new_embs = make_embeddings(new_texts, batch_size=batch_size)
        print(f"✅ 신규 {len(new_ids)}개 임베딩 생성")
    else:
        new_embs = np.zeros((0, cached_embs.shape[1] if cached_embs.size else new_embs.shape[1]))
        print("✅ 신규 임베딩 없음, 모두 캐시 재사용")

    # 5) 최종 윈도우 임베딩 배열 재조합
    final_embs = []
    new_idx = 0
    for aid in ids_window:
        if aid in cached_ids:
            idx = int(np.where(cached_ids == aid)[0][0])
            final_embs.append(cached_embs[idx])
        else:
            final_embs.append(new_embs[new_idx])
            new_idx += 1
    final_embs = np.stack(final_embs, axis=0)
    final_ids = np.array(ids_window, dtype=int)

    # 6) 캐시에 덮어쓰기
    save_embedding_cache(final_ids, final_embs, id_path, emb_path)
    print(f"✅ 캐시가 지난 {since_hours}시간 윈도우({len(final_ids)}개)로 갱신되었습니다")

    return final_embs


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

    # 5) DB에 저장
    if save_db:
        article_ids = fetch_article_ids(limit=limit)
        # if len(article_ids) != len(labels):
        #     print("⚠️ 오류: Article ID 수와 임베딩 수가 일치하지 않습니다.")
        #     return
        save_clusters_to_db(article_ids, labels)

    # 4) 대표 키워드 추출
    raw_texts = fetch_all_texts(limit=limit)
    from clustering.embedder import preprocess_text
    texts = [preprocess_text(t) for t in raw_texts]
    # 📌 디버깅용 로그 추가: 전처리 후 공백률 확인
    non_empty = [t for t in texts if t.strip()]
    empty_count = len(texts) - len(non_empty)
    print("── 전처리 디버깅 ──")
    print(f"전체 기사 수: {len(texts)}")
    print(f"빈 문자열 수: {empty_count}")
    print(f"공백이 아닌 예시 3개: {non_empty[:3]}")
    print("──────────────────")

    db: Session = SessionLocal()
    try:
        keywords: Dict[int, List[str]] = extract_keywords_per_cluster(
            texts=texts,      
            labels=labels,    
            db=db,            
            top_n=3,
            max_features=1000
        )
    finally:
        db.close()

    print("\n대표 키워드 (클러스터별):")
    for lbl, kws in keywords.items():
        print(f"  - Cluster {lbl}: {', '.join(kws)}")

    # --- 여기에 DB 저장 로직 추가 ---
    for lbl, kws in keywords.items():
        # 방금 저장된 Cluster 객체를 label별로 최신(created_at 기준)으로 조회
        cluster = db.query(Cluster) \
                    .filter_by(label=lbl) \
                    .order_by(Cluster.created_at.desc()) \
                    .first()
        if not cluster:
            print(f"⚠️ Cluster {lbl}를 찾지 못해 스킵합니다.")
            continue

        for name in kws:
            # Keyword 테이블에서 이름으로 조회, 없으면 새로 생성
            kw = db.query(Keyword).filter_by(name=name).first()
            if not kw:
                kw = Keyword(name=name)
                db.add(kw)
                db.flush()   # kw.id가 채워지도록

            # 중복 삽입 방지
            exists = db.query(ClusterKeyword) \
                       .filter_by(cluster_id=cluster.id, keyword_id=kw.id) \
                       .first()
            if not exists:
                db.add(ClusterKeyword(
                    cluster_id=cluster.id,
                    keyword_id=kw.id
                ))

    db.commit()
    print("✅ ClusterKeyword 관계에 키워드를 저장했습니다.")


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
