from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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

@router.post("/run")
async def run_full_pipeline(
    method: str = "kmeans",
    n_clusters: int = 10,
    eps: float = 0.5,
    min_samples: int = 5,
    limit: int = 100,
    save_db: bool = True,
):
    """
    임베딩 생성부터 클러스터링, DB 저장까지 전체 파이프라인을 실행합니다.
    """
    # 1) 임베딩
    embeddings = run_embedding_stage(limit=limit)
    if embeddings is None:
        raise HTTPException(status_code=400, detail="No articles available for embedding")

    # 2) 클러스터링
    run_clustering_stage(
        emb_path="data/article_embeddings.npy",
        method=method,
        n_clusters=n_clusters,
        eps=eps,
        min_samples=min_samples,
        limit=limit,
        save_db=save_db,
    )

    return {"message": "Pipeline executed successfully"}

@router.get("/{cluster_id}", response_model=List[dict])
async def get_cluster_articles(cluster_id: int, db: Session = Depends(get_db)):
    """
    주어진 cluster_id에 속한 기사 목록을 반환합니다.
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
