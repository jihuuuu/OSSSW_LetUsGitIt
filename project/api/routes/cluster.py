from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, aliased
from typing import List
from datetime import datetime, timedelta, timezone
from database.deps import get_db
from models.article import Cluster, ClusterArticle, Article, ClusterKeyword, Keyword
from pydantic import BaseModel, HttpUrl
from operator import attrgetter
from api.schemas.cluster import *
from models.topic import TopicEnum

router = APIRouter()


@router.get("/today", response_model=List[ClusterOut])
async def list_clusters(topic: TopicEnum | None = None, db: Session = Depends(get_db)):
    """
    시스템 클러스터별로 최신순 2개 기사만 묶어서 배열로 반환합니다.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
    base_q = db.query(Cluster).filter(Cluster.created_at >= cutoff)
    # 2) 최신순으로 50개 클러스터만 추출하는 서브쿼리 생성
    subq = (
        base_q
          .order_by(Cluster.created_at.desc())
          .limit(50)
          .subquery()
    )

    # 3) 서브쿼리를 Cluster 엔티티로 다시 매핑(aliased 사용)
    ClusterAlias = aliased(Cluster, subq)

    # 4) 서브쿼리 결과(최신 50개)에 대해 num_articles 기준으로 정렬 후 최종 20개 조회
    top_clusters: List[Cluster] = (
        db.query(ClusterAlias)
          .options(
              joinedload(ClusterAlias.cluster_article).joinedload(ClusterArticle.article),
              joinedload(ClusterAlias.cluster_keyword).joinedload(ClusterKeyword.keyword)
          )
          .order_by(ClusterAlias.num_articles.desc())           # num_articles 내림차순
          .limit(20)
          .all()
    )

    if not top_clusters:
        raise HTTPException(status_code=404, detail="클러스터된 기사가 없습니다")

    result: List[ClusterOut] = []
    for cl in top_clusters:
        # 최신순으로 정렬 후 최대 2개 기사만 선택
        top2 = sorted(
            cl.cluster_article,
            key=lambda ca: ca.article.published or datetime.min,
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
                topic=cl.topic.value if cl.topic else None,
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

@router.get(
    "/keywords/today",response_model=List[KeywordsTodayOut],
    summary="최근 24시간 생성된 클러스터별 대표 키워드와 기사 수"
)

def get_keywords_today(topic: TopicEnum | None = None, db: Session = Depends(get_db)):

    # 1) 시간 필터: 24시간 전
    cutoff = datetime.now(timezone.utc) - timedelta(hours=1)

    # 2) Cluster → ClusterKeyword → Keyword 한 번에 로드
    clusters = (
        db.query(Cluster)
          .options(
              joinedload(Cluster.cluster_keyword).joinedload(ClusterKeyword.keyword)
          )
          .filter(Cluster.created_at >= cutoff)
    )
    if topic is not None:
        clusters = clusters.filter(Cluster.topic == topic)

    clusters = (
        clusters
          .order_by(Cluster.created_at.desc())
          .limit(20)
          .all()
    )

    result: List[KeywordsTodayOut] = []
    for cl in clusters:
        kws: List[KeywordCount] = []
        for ck in cl.cluster_keyword:
            name = ck.keyword.name
            # 3) 각 키워드별로 해당 클러스터에 속한 기사 중 title/summary에 키워드가 포함된 개수 집계
            cnt = (
                db.query(Article.id)
                  .join(ClusterArticle, ClusterArticle.article_id == Article.id)
                  .filter(
                      ClusterArticle.cluster_id == cl.id,
                      (Article.title.contains(name)) |
                      (Article.summary.contains(name))
                  )
                  .distinct()
                  .count()
            )
            kws.append(KeywordCount(keyword=name, article_count=cnt))
        result.append(KeywordsTodayOut(
            cluster_id=cl.id,
            created_at=cl.created_at,
            keywords=kws
        ))

    return result