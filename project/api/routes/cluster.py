from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime

from database.deps import get_db
from models.article import Cluster, ClusterArticle, Article, ClusterKeyword, Keyword
from pydantic import BaseModel, HttpUrl
from operator import attrgetter

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
          .order_by(Cluster.created_at.desc())  # 최신 클러스터부터
          .limit(10) # 최근 10개 클러스터만
          .all()
    )
    clusters.sort(key=attrgetter("num_articles"), reverse=True)  # 기사 수 기준으로 정렬
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


@router.get("/today/{cluster_id}/articles", response_model=dict)
async def get_cluster_articles(cluster_id: int, db: Session = Depends(get_db)):
    cl = db.get(Cluster, cluster_id)
    if not cl:
        raise HTTPException(404, f"No cluster with id {cluster_id}")

    # 관련 기사
    articles = (
        db.query(Article)
        .join(ClusterArticle, ClusterArticle.article_id == Article.id)
        .filter(ClusterArticle.cluster_id == cluster_id)
        .order_by(Article.fetched_at.desc())
        .all()
    )
    if not articles:
        raise HTTPException(404, f"No articles found for cluster {cluster_id}")

    article_dicts = []
    for a in articles:
        article_dicts.append({
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "url": a.link,
            "cluster_id": cluster_id,
            "fetched_at": a.fetched_at.isoformat(),
        })

    # 관련 키워드
    keywords = (
        db.query(Keyword.name)
        .join(ClusterKeyword, ClusterKeyword.keyword_id == Keyword.id)
        .filter(ClusterKeyword.cluster_id == cluster_id)
        .all()
    )
    keyword_list = [k[0] for k in keywords]

    return {
        "cluster_id": cluster_id,
        "keywords": keyword_list,
        "articles": article_dicts,
    }
