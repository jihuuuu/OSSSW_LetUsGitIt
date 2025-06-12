from models.topic import TopicEnum
from typing import List, Dict, Tuple, Optional
import numpy as np
import os
from collector.rss_collector import fetch_texts_with_ids_by_topic
from clustering.embedder import make_embeddings, preprocess_text
from clustering.cache import load_embedding_cache, save_embedding_cache
from umap import UMAP
from collections import Counter
import time
from clustering.keyword_extractor import extract_top_keywords
from models.article import ClusterKeyword, Keyword
from database.connection import SessionLocal
from sklearn.feature_extraction.text import TfidfVectorizer
from clustering.cache_redis import load_embedding_cache, save_embedding_cache
from clustering.cluster import (
    load_embeddings, run_kmeans, run_dbscan, run_hdbscan,
    save_clusters_to_db, fetch_article_ids
)


def run_embedding_stage(
    topic: TopicEnum, since_hours: int = 24,
    data_dir: str = "data", batch_size: int = 32,
) -> Tuple[np.ndarray, List[int], List[str], List[str]] | None:
    """
    1) 특정 topic 기사 ID와 원문 리스트(fetched within since_hours) 가져오기
    2) 전처리→캐시 로드→새 임베딩 생성→캐시 업데이트
    """
    # 1) 최근 since_hours 시간 동안 발행된 topic별 기사 가져오기
    rows = fetch_texts_with_ids_by_topic(topic=topic, since_hours=since_hours)
    if not rows:
        print(f"♨️ [{topic.value}] 기사 없음 → 임베딩 단계 스킵")
        return None

    ids_window, raw_texts = zip(*rows)
    ids_window = list(ids_window)
    raw_texts = list(raw_texts)

    # 2) 전처리
    cleaned_texts = [preprocess_text(t) for t in raw_texts]

    # 3) Redis 캐시 로드 (TTL 기반 자동 만료)
    cached_ids, cached_embs = load_embedding_cache(topic.value)

    # 4) 캐시된 임베딩과 신규 텍스트 분리
    new_ids, new_texts, reused_embs = [], [], []
    for aid, text in zip(ids_window, cleaned_texts):
        if aid in cached_ids:
            idx = int(np.where(cached_ids == aid)[0][0])
            reused_embs.append(cached_embs[idx])
        else:
            new_ids.append(aid)
            new_texts.append(text)

    # 5) 신규 임베딩 생성
    if new_texts:
        new_embs = make_embeddings(new_texts, batch_size=batch_size)
        print(f"✅ [{topic.value}] 신규 {len(new_ids)}개 임베딩 생성")
    else:
        new_embs = np.zeros((0, cached_embs.shape[1] if cached_embs.size else 0))
        print(f"✅ [{topic.value}] 신규 임베딩 없음 → 캐시 재사용만")

    # 6) 최종 임베딩 재조합
    final_embs_list, new_idx = [], 0
    for aid in ids_window:
        if aid in cached_ids:
            idx = int(np.where(cached_ids == aid)[0][0])
            final_embs_list.append(cached_embs[idx])
        else:
            final_embs_list.append(new_embs[new_idx])
            new_idx += 1
    final_embs = np.vstack(final_embs_list)
    final_ids = np.array(ids_window, dtype=int)

    # 7) Redis 캐시 업데이트 (TTL = since_hours * 3600초)
    ttl_seconds = since_hours * 3600
    save_embedding_cache(final_ids, final_embs, topic.value, ttl=ttl_seconds)
    print(f"✅ [{topic.value}] Redis 캐시 갱신 (TTL={ttl_seconds}s): {len(final_ids)}개")

    return final_embs, ids_window, raw_texts, cleaned_texts


def run_clustering_stage(
    emb_path: str, ids_window: List[int], raw_texts: List[str],
    cleaned_texts: List[str], method: str, n_clusters: Optional[int], 
    eps: Optional[float], min_samples: Optional[int], topic, 
    save_db: bool, umap_n_neighbors: int = 5, umap_min_dist: float = 0.02,
    top_kws: int = 3, model_name: str = 'jhgan/ko-sbert-sts'
) -> Tuple[np.ndarray, Dict[int, List[str]], Dict[int, int]]:
    # 1) 임베딩 로드
    embeddings = load_embeddings(emb_path)
    print(f"▶️ loaded embeddings: {embeddings.shape}")

    # 1-1) 차원 축소 (UMAP)
    embeddings = UMAP(n_neighbors=umap_n_neighbors, min_dist=umap_min_dist, 
                      n_components=10, random_state=42, metric='cosine').fit_transform(embeddings)
    print(f"▶️ reduced embeddings: {embeddings.shape}")

    # 2) 클러스터링 수행
    if method == "kmeans":
        labels = run_kmeans(embeddings, n_clusters)
    elif method == "dbscan":
        labels = run_dbscan(embeddings, eps, min_samples)
    else:  # hdbscan
        labels = run_hdbscan(embeddings, min_cluster_size=n_clusters, min_samples=min_samples)

    counts = Counter(labels)
    print("클러스터 요약:")
    for lbl, cnt in counts.items():
        print(f"  - Cluster {lbl}: {cnt} articles")

    # 3) DB에 저장
    label_to_cluster_id : Dict[int, int] = {}
    if save_db:
        t0 = time.time()
        label_to_cluster_id = save_clusters_to_db(article_ids=ids_window, labels=labels, topic=topic)
        print(f"DB 클러스터 저장 시간: {time.time() - t0:.2f}s")
    else:
        label_to_cluster_id = {}

    # 클러스터별 문서 묶음 생성 (키워드 추출용)
    cluster_to_docs: Dict[int, List[str]] = {}
    for idx, lbl in enumerate(labels):
        aid = ids_window[idx]
        doc = cleaned_texts[idx]
        if not doc:   # None 이거나 빈 문자열인 경우
            # 아예 스킵 (None 이 추가되는 걸 방지)
            continue        
        cluster_to_docs.setdefault(lbl, []).append(doc)

    # 6) 리턴: labels, docs 묶음, label→cluster_id 매핑
    return labels, cluster_to_docs, label_to_cluster_id


def run_keyword_extraction(
    cluster_to_docs: Dict[int, List[str]],
    label_to_cluster_id : Dict[int, int],
    top_n: int = 3, save_db: bool = True,
    global_vectorizer: TfidfVectorizer = None
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

        # 글로벌 벡터라이저를 넘겨줍니다
        kws = extract_top_keywords(
            documents=docs, cluster_id=cid, top_n=top_n,
            global_vectorizer=global_vectorizer
        )
        kw_map[label] = kws

        if save_db:
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

    if save_db:
        db.commit()
        print("✅ ClusterKeyword 관계에 키워드를 저장했습니다.")
    db.close()

    return kw_map
