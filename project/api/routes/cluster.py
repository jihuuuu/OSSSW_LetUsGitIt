# routers/clusters.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from database.deps import get_db
from models.article import Cluster, ClusterArticle, Article, ClusterKeyword, Keyword
from pydantic import BaseModel, HttpUrl

router = APIRouter()

# --- Pydantic 응답 스키마 정의 ---
class ArticleOut(BaseModel):
    article_id: int
    title: str
    summary: str
    link: HttpUrl
    published: datetime

class ClusterOut(BaseModel):
    cluster_id: int
    created_at: datetime
    label: int
    num_articles: int
    keywords: List[str]
    articles: List[ArticleOut]

    class Config:
        orm_mode = True


@router.get("/today", response_model=List[ClusterOut])
async def list_clusters(db: Session = Depends(get_db)):
    """
    시스템 클러스터별로 최신순 2개 기사만 묶어서 배열로 반환합니다.
    """
    # Cluster → ClusterArticle → Article, 그리고 ClusterKeyword → Keyword 를 한 번에 로드
    clusters = (
        db.query(Cluster)
          .options(
              joinedload(Cluster.cluster_article)
                .joinedload(ClusterArticle.article),
              joinedload(Cluster.cluster_keyword)
                .joinedload(ClusterKeyword.keyword)
          )
          .order_by(Cluster.label)
          .all()
    )
    if not clusters:
        raise HTTPException(status_code=404, detail="클러스터된 기사가 없습니다")

    result: List[ClusterOut] = []
    for cl in clusters:
        # 최신순으로 정렬 후 최대 2개 기사만 선택
        top2 = sorted(
            cl.cluster_article,
            key=lambda ca: ca.article.published,
            reverse=True
        )[:2]

        articles_out = [
            ArticleOut(
                article_id=ca.article.id,
                title=ca.article.title,
                summary=ca.article.summary,
                link=ca.article.link,
                published=ca.article.published
            )
            for ca in top2
        ]

        keywords = [ck.keyword.name for ck in cl.cluster_keyword]

        result.append(
            ClusterOut(
                cluster_id=cl.id,
                created_at=cl.created_at,
                label=cl.label,
                num_articles=len(cl.cluster_article),
                keywords=keywords,
                articles=articles_out
            )
        )

    return result


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
