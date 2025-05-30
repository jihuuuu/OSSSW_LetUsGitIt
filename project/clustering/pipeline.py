# clustering/pipeline.py
from typing import List, Dict
from database.connection import SessionLocal
from models.article import ClusterKeyword, Keyword
import numpy as np
import argparse
from collections import Counter
from clustering.keyword_extractor import extract_top_keywords
from clustering.cache import load_embedding_cache, save_embedding_cache
from clustering.embedder import make_embeddings, preprocess_text
from collector.rss_collector import fetch_texts_with_ids, fetch_all_texts
import time
from clustering.cluster import (
    load_embeddings, run_kmeans, run_dbscan, run_hdbscan,
    save_clusters_to_db, fetch_article_ids
)
from collector.rss_collector import fetch_texts_with_ids, fetch_all_texts


def run_embedding_stage(
    *, limit: int | None = None, batch_size: int = 32,
    since_hours: int = 24, id_path: str = "data/article_ids.npy",
    emb_path: str = "data/article_embeddings.npy",
):
    # 1) 지난 since_hours 기사와 텍스트
    rows = fetch_texts_with_ids(since_hours=since_hours)
    if not rows:
        print("⚠️ 분석할 기사 텍스트가 없습니다.")
        return None

    ids_window, raw_texts = zip(*rows)
    ids_window = list(ids_window)
    raw_texts = list(raw_texts)

    # 1-1) 전처리 (한 번만!)
    cleaned_texts = [preprocess_text(t) for t in raw_texts]
    # cleaned_texts[i] 는 ids_window[i] 에 대한 전처리 결과

    # 2) 기존 캐시 로드
    cached_ids, cached_embs = load_embedding_cache(id_path, emb_path)

    # 3) 최신 윈도우 내에서 재사용 가능한 인덱스
    reused_embs = []
    new_texts = []
    new_ids = []
    for aid, txt in zip(ids_window, raw_texts):
        if aid in cached_ids:
            idx = int(np.where(cached_ids == aid)[0][0])
            reused_embs.append(cached_embs[idx])
        else:
            new_ids.append(aid)
            new_texts.append(txt)

    # 4) 새로운 임베딩 생성: 이미 전처리된 cleaned_texts 중 새로 필요한 부분만
    if new_texts:
        # new_ids 와 new_texts 순서에 맞춰 인덱스 뽑기
        idxs = [ids_window.index(aid) for aid in new_ids]
        new_cleaned = [cleaned_texts[i] for i in idxs]
        new_embs = make_embeddings(new_cleaned, batch_size=batch_size)
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

    return final_embs, ids_window, raw_texts, cleaned_texts


def run_clustering_stage(
    emb_path: str, method: str, n_clusters: int | None,
    eps: float | None, min_samples: int | None, 
    limit: int | None, save_db: bool, clean_map: Dict[int, str],
    top_kws : int = 3, model_name: str = 'jhgan/ko-sbert-sts'
):
    # 1) 임베딩 로드
    embeddings = load_embeddings(emb_path)
    print(f"▶️ loaded embeddings: {embeddings.shape}")

    # 1-1) 차원 축소 (UMAP)
    from umap import UMAP
    embeddings = UMAP(n_components=10, random_state=42).fit_transform(embeddings)
    print(f"▶️ reduced embeddings: {embeddings.shape}")

    # 2) 클러스터링 수행
    if method == "kmeans":
        labels = run_kmeans(embeddings, n_clusters)
    elif method == "dbscan":
        labels = run_dbscan(embeddings, eps, min_samples)
    else:  # hdbscan
        labels = run_hdbscan(embeddings, min_cluster_size=n_clusters, min_samples=min_samples)

    # 3) 클러스터 요약 출력
    counts = Counter(labels)
    print("클러스터 요약:")
    for lbl, cnt in counts.items():
        print(f"  - Cluster {lbl}: {cnt} articles")

    # 4) DB에 저장
    label_to_cluster_id : Dict[int, int] = {}
    if save_db:
        article_ids = fetch_article_ids(limit=limit)
        t0 = time.time()
        label_to_cluster_id = save_clusters_to_db(article_ids, labels)
    print(f"DB 클러스터 저장 시간: {time.time() - t0:.2f}s")

    # 클러스터별 문서 묶음 생성 (키워드 추출용)
    t1 = time.time()
    cluster_to_docs: Dict[int, List[str]] = {}
    article_ids = fetch_article_ids(limit=limit)
    for aid, lbl in zip(article_ids, labels):
        doc = clean_map.get(aid)
        if not doc:   # None 이거나 빈 문자열인 경우
            # 아예 스킵 (None 이 추가되는 걸 방지)
            continue        
        cluster_to_docs.setdefault(lbl, []).append(doc)
    print(f"문서 묶음 생성 시간: {time.time() - t1:.2f}s")

    # 6) 리턴: labels, docs 묶음, label→cluster_id 매핑
    return labels, cluster_to_docs, label_to_cluster_id


def run_keyword_extraction(
    cluster_to_docs: Dict[int, List[str]],
    label_to_cluster_id : Dict[int, int],
    top_n: int = 3,
) -> Dict[int, List[str]]:
    # TF-IDF 기반
    # 또는 SBERT 병렬 추출: parallel_extract_keywords
    db = SessionLocal()
    kw_map: Dict[int, List[str]] = {}

    for label, docs in cluster_to_docs.items():
        # 0) None 혹은 빈 문자열 제거
        docs = [d for d in docs if d and isinstance(d, str)]
        if not docs:
            print(f"⚠️ Cluster {label}: 전처리된 문서가 없어서 스킵합니다.")
            continue        
        cid = label_to_cluster_id.get(label)
        if cid is None:
            print(f"⚠️ label {label}에 매핑된 Cluster ID가 없어 스킵합니다.")
            continue

        # TF-IDF 기반으로 top_n 키워드 추출 + DB 저장
        kws = extract_top_keywords(documents=docs, db=db, cluster_id=cid, top_n=top_n)
        kw_map[label] = kws

        # 2) Keyword / ClusterKeyword 테이블에 저장
        for name in kws:
            # (a) Keyword 테이블에 없으면 생성
            kw_obj = db.query(Keyword).filter_by(name=name).first()
            if not kw_obj:
                kw_obj = Keyword(name=name)
                db.add(kw_obj)
                db.flush()   # kw_obj.id 확보

            # (b) ClusterKeyword 매핑이 없으면 생성
            exists = (
                db.query(ClusterKeyword)
                  .filter_by(cluster_id=cid, keyword_id=kw_obj.id)
                  .first()
            )
            if not exists:
                db.add(ClusterKeyword(cluster_id=cid, keyword_id=kw_obj.id))

    db.commit()
    db.close()
    print("✅ ClusterKeyword 관계에 키워드를 저장했습니다.")
    return kw_map


def main():
    parser = argparse.ArgumentParser(description="뉴스 파이프라인: 임베딩 및 클러스터링")
    # 클러스터링 관련 인자만 유지
    parser.add_argument("--method", choices=["kmeans", "dbscan", "hbscan"], default="kmeans", help="클러스터링 알고리즘 선택")
    parser.add_argument("--n-clusters", type=int, default=10, help="KMeans 클러스터 수")
    parser.add_argument("--eps", type=float, default=0.5, help="DBSCAN eps 파라미터")
    parser.add_argument("--min-samples", type=int, default=5, help="DBSCAN min_samples 파라미터")
    parser.add_argument("--limit", type=int, help="최근 N건만 처리")
    parser.add_argument("--save-db", action="store_true", default=True, help="DB에 클러스터 라벨 저장")
    parser.add_argument("--top-kws", type=int, default=3, help="추출할 대표 키워드 수")

    args = parser.parse_args()

    
    # 1) 임베딩 단계 수행 (항상 실행)
    result = run_embedding_stage(limit=args.limit, batch_size=32)
    if result is None:
        return
    embs, ids, raw_texts, cleaned_texts = result
    
    
    # 2) 클러스터링: 결과 리턴받기
    raw_map = dict(zip(ids, raw_texts))
    clean_map = dict(zip(ids, cleaned_texts))
    labels, cluster_docs, label_map = run_clustering_stage(
        emb_path="data/article_embeddings.npy",
        method=args.method, n_clusters=args.n_clusters,
        eps=args.eps, min_samples=args.min_samples,
        limit=args.limit, save_db=args.save_db, clean_map=clean_map
    )


    # 3) 키워드 추출 → DB 저장
    t2 = time.time()
    kw_map = run_keyword_extraction(
        cluster_to_docs=cluster_docs,
        label_to_cluster_id=label_map, top_n=args.top_kws
    )
    for lbl, kws in kw_map.items():
        print(f"Cluster {lbl} 키워드: {', '.join(kws)}")
    print(f"키워드 추출 시간: {time.time() - t2:.2f}s")


if __name__ == "__main__":
    main()
