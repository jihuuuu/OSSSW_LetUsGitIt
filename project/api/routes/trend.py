from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from api.schemas.trend import *

from database.deps import get_db                             # :contentReference[oaicite:0]{index=0}
from models.article import Article, ClusterArticle,            \
                             ClusterKeyword, Keyword
from clustering.keyword_extractor import extract_top_keywords

router = APIRouter()

@router.get("/weekly", response_model=WeeklyTrendResponse)
def get_weekly_trends(
    start_date: Optional[date] = None,
    end_date:   Optional[date] = None,
    db:         Session = Depends(get_db),
):
    # 1) 날짜 계산: 기본은 최근 7일
    end_date   = date.today()
    start_date = end_date - timedelta(days=6)

    # 2) 기간별 일자 리스트
    num_days = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    # 3) 키워드별 누적 기사 수 계산 (클러스터 구분 없이 키워드 단위로 한 번만)
    from sqlalchemy import func

    keyword_counts = (
        db.query(
            Keyword.id.label("kw_id"),
            Keyword.name.label("kw_name"),
            func.count(func.distinct(Article.id)).label("total")
        )
        .join(ClusterKeyword, ClusterKeyword.keyword_id == Keyword.id)
        .join(ClusterArticle, ClusterArticle.cluster_id == ClusterKeyword.cluster_id)
        .join(Article, Article.id == ClusterArticle.article_id)
        .filter(Article.published >= datetime.combine(start_date, datetime.min.time()))
        .filter(Article.published <  datetime.combine(end_date + timedelta(days=1), datetime.min.time()))
        .filter(
            or_(
                Article.title.contains(Keyword.name),
                Article.summary.contains(Keyword.name)
            )
        )
        .group_by(Keyword.id, Keyword.name)
        .order_by(func.count(Article.id).desc())
        .limit(5)
        .all()
    )
    # 이제 중복 없이 상위 5개 키워드만 남음
    top5 = [(row.kw_name, row.kw_id, row.total) for row in keyword_counts]
    top_keywords = [name for name, _, _ in top5]

    # 5) 일별 변화 구하기
    trend_data: List[KeywordTrend] = []
    for kw_name, kw_id, total in top5:
        daily = []
        for d in dates:
            d_start = datetime.combine(d, datetime.min.time())
            d_end   = d_start + timedelta(days=1)
            cnt = (
                db.query(Article.id)
                  .join(ClusterArticle, ClusterArticle.article_id == Article.id)
                  .join(ClusterKeyword, ClusterKeyword.cluster_id == ClusterArticle.cluster_id)
                  .filter(ClusterKeyword.keyword_id == kw_id)
                  .filter(Article.published >= d_start, Article.published < d_end)
                  .filter(
                      or_(
                          Article.title.contains(kw_name),
                          Article.summary.contains(kw_name)
                      )
                  )
                  .distinct()
                  .count()
            )
            daily.append(DailyCount(date=d, count=cnt))
        trend_data.append(KeywordTrend(
            keyword=kw_name,
            total_counts=total,
            daily_counts=daily
        ))

    return WeeklyTrendResponse(
        start_date=start_date,
        end_date=end_date,
        top_keywords=top_keywords,
        trend_data=trend_data
    )

@router.get("/search", response_model=SearchTrendResponse)
def search_trends(
    keyword: str,
    db:      Session = Depends(get_db),
):
    # 1) 날짜 범위: 오늘 포함 최근 7일
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    dates = [start_date + timedelta(days=i) for i in range(7)]

    # 2) 키워드 유효성 검사
    kw = db.query(Keyword).filter(Keyword.name == keyword).first()
    if not kw:
        raise HTTPException(404, f"키워드 '{keyword}'를 찾을 수 없습니다.")

    # 3) 일별 기사 수 집계
    trend: List[DailyCount] = []
    for d in dates:
        d_start = datetime.combine(d, datetime.min.time())
        d_end   = d_start + timedelta(days=1)
        cnt = (
            db.query(Article.id)
              .filter(Article.published >= d_start, Article.published < d_end)
              .filter(
                  (Article.title.contains(keyword)) |
                  (Article.summary.contains(keyword))
              )
              .distinct()
              .count()
        )
        trend.append(DailyCount(date=d, count=cnt))

    # 4) 연관 키워드 구성
    related: List[RelatedKeyword] = []
    clusters = (
        db.query(Cluster)
          .join(ClusterKeyword, Cluster.id == ClusterKeyword.cluster_id)
          .filter(ClusterKeyword.keyword_id == kw.id)
          .all()
    )
    for cl in clusters:
        # 같은 클러스터의 다른 대표 키워드
        co = [ck.keyword.name for ck in cl.cluster_keyword if ck.keyword.name != keyword]

        # 클러스터 내 기사 텍스트 모음
        texts = [
            art.title + " " + (art.summary or "")
            for art in (
                db.query(Article)
                  .join(ClusterArticle, ClusterArticle.article_id == Article.id)
                  .filter(ClusterArticle.cluster_id == cl.id)
                  .all()
            )
        ]
        # TF-IDF 기반 비대표 키워드 추출 후 대표 키워드·검색 키워드 제외
        freqs = extract_top_keywords(texts, top_n=5)
        exclude = set(co + [keyword])
        freq_kws = [w for w in freqs if w not in exclude][:2]

        related.append(RelatedKeyword(
            cluster_id=cl.id,
            created_at=cl.created_at,
            co_keywords=co,
            frequent_keywords=freq_kws
        ))

    return SearchTrendResponse(
        keyword=keyword,
        trend=trend,
        related_keywords=related
    )