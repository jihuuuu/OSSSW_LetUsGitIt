from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict
from typing import Dict, List

from database.connection import SessionLocal
from models.article import Article
from clustering.pipeline import run_embedding_stage, run_clustering_stage

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=Dict[int, List[dict]])
async def list_clusters(db: Session = Depends(get_db)):
    """
    cluster가 지정된 기사만 가져와
    클러스터별로 최신순 2개씩 묶어서 반환합니다.
    """
    # 1) cluster가 NULL인 건 제외하고, cluster → fetched_at(desc) 순서로 가져오기
    articles = (
        db.query(Article)
          .filter(Article.cluster != None)
          .order_by(Article.cluster, Article.fetched_at.desc())
          .all()
    )

    if not articles:
        raise HTTPException(status_code=404, detail="클러스터된 기사가 없습니다")

    # 2) 클러스터별로 2개까지만 보여주기
    grouped: Dict[int, List[dict]] = defaultdict(list)
    for a in articles:
        key = a.cluster
        if len(grouped[key]) < 2:
            grouped[key].append({
                "id": a.id,
                "title": a.title,
                "summary": a.summary,
                "url": getattr(a, "url", None),
                "fetched_at": a.fetched_at.isoformat(),
            })

    return grouped

@router.get("/{cluster_id}", response_model=List[dict])
async def get_cluster_articles(cluster_id: int, db: Session = Depends(get_db)):
    """
    주어진 cluster_label에 속한 기사 목록을 반환합니다.
    """
    articles = (
        db.query(Article)
        .filter(Article.cluster == cluster_id)
        .order_by(Article.fetched_at.desc())
        .all()
    )
    if not articles:
        raise HTTPException(status_code=404, detail=f"No articles found for cluster {cluster_id}")

    # 직렬화
    result = []
    for a in articles:
        result.append({
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "url": getattr(a, "url", None),
            "cluster_label": a.cluster,
            "fetched_at": a.fetched_at.isoformat(),
        })
    return result
