from operator import attrgetter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from collections import defaultdict
from typing import Dict, List

from database.deps import get_db
from models.article import ClusterArticle, Article, Cluster
from clustering.pipeline import run_embedding_stage, run_clustering_stage

router = APIRouter()

@router.get("/today", response_model=Dict[int, List[dict]])
async def list_clusters(db: Session = Depends(get_db)):
    """
    시스템 클러스터별 최신순 2개 기사만 묶어서 반환
    """
    # 1) Cluster → ClusterArticle → Article 를 한 번에 로드
    clusters = (
        db.query(Cluster)
          .options(
              joinedload(Cluster.cluster_article)           # ClusterArticle 객체
              .joinedload(ClusterArticle.article)                        # 그 안의 Article 객체
          )
          .order_by(Cluster.created_at.desc())  # 최신 클러스터부터
          .limit(10) # 최근 10개 클러스터만
          .all()
    )
    clusters.sort(key=attrgetter("num_articles"), reverse=True)  # 기사 수 기준으로 정렬
    if not clusters:
        raise HTTPException(404, "클러스터된 기사가 없습니다")

    # 2) 클러스터별로 2개까지만 보여주기
    grouped: Dict[int, List[dict]] = defaultdict(list)
    for cl in clusters:
        seen_ids = set()
        cnt = 0
        # 클러스터 레이블별로 최대 2개만
        for ca in cl.cluster_article[:2]:
            art = ca.article
            if art.id in seen_ids:  # db 단계에서 유니크 조합 제약을 걸 수도 있따
                continue
            seen_ids.add(art.id)
            grouped[cl.label].append({
                "id":           art.id,
                "title":        art.title,
                "summary":      art.summary,
                "url":          art.link,                     # Article.link 컬럼:contentReference[oaicite:2]{index=2}
                "fetched_at":   art.fetched_at.isoformat(),
            })
            cnt += 1
            if cnt >= 2:
                break

    return grouped

@router.get("/today/{cluster_id}/articles", response_model=List[dict])
async def get_cluster_articles(cluster_id: int, db: Session = Depends(get_db)):
    """
    특정 클러스터 ID의 모든 기사 목록을 최신순으로 반환
    """
    # 1) Cluster가 존재하는지 확인
    cl = db.get(Cluster, cluster_id)
    if not cl:
        raise HTTPException(404, f"No cluster with id {cluster_id}")

    # 2) ClusterArticle → Article 로 매핑된 기사들 꺼내기
    articles = (
        db.query(Article)
          .join(ClusterArticle, ClusterArticle.article_id == Article.id)
          .filter(ClusterArticle.cluster_id == cluster_id)
          .order_by(Article.fetched_at.desc())
          .all()
    )
    if not articles:
        raise HTTPException(404, f"No articles found for cluster {cluster_id}")

    # 직렬화
    result = []
    for a in articles:
        result.append({
            "id":            a.id,
            "title":         a.title,
            "summary":       a.summary,
            "url":           a.link,
            "cluster_id":    cluster_id,
            "fetched_at":    a.fetched_at.isoformat(),
        })
    return result
