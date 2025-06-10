from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from api.schemas.trend import *
from models.article import Cluster
from database.deps import get_db                             # :contentReference[oaicite:0]{index=0}
from models.article import Article, ClusterArticle, ClusterKeyword, Keyword, TrendKeyword
from clustering.keyword_extractor import extract_top_keywords
from clustering.embedder import preprocess_text
from konlpy.tag import Okt

router = APIRouter()

# Okt 인스턴스와 불용어는 embedder.py 쪽에 정의돼 있다고 가정
_okt = Okt()

@router.get("/weekly", response_model=WeeklyTrendResponse)
def get_weekly_trends(db: Session = Depends(get_db)):
    today = date.today() # - timedelta(days=1)
    start = today - timedelta(days=7)
    
    # 1) 지난 7일간 cluster_keyword별 합계 집계 → keyword_id로 매핑
    rows = (
        db.query(
            ClusterKeyword.keyword_id.label("keyword_id"),
            func.sum(TrendKeyword.count).label("total")
        )
        .join(TrendKeyword, TrendKeyword.cluster_keyword_id == ClusterKeyword.id)
        .filter(TrendKeyword.date >= start, TrendKeyword.date <= today)
        .group_by(ClusterKeyword.keyword_id)
        .order_by(desc("total"))
        .limit(5)
        .all()
    )

    # 2) id → name 매핑
    kw_ids = [r.keyword_id for r in rows]
    kw_map = {
        k.id: k.name
        for k in db.query(Keyword).filter(Keyword.id.in_(kw_ids)).all()
    }

    # 3) 응답 객체 생성
    top_keywords = [kw_map[r.keyword_id] for r in rows]
    trend_data = []
    for r in rows:
        # 하루 단위 상세 집계
        daily_counts = []
        for i in range(7):
            d = start + timedelta(days=i)
            cnt = (
                db.query(func.sum(TrendKeyword.count))
                  .join(ClusterKeyword, ClusterKeyword.id == TrendKeyword.cluster_keyword_id)
                  .filter(
                      ClusterKeyword.keyword_id == r.keyword_id,
                      TrendKeyword.date == d
                  )
                  .scalar()
            ) or 0
            daily_counts.append(DailyCount(date=d, count=cnt))

        trend_data.append(
            KeywordTrend(
                keyword=kw_map[r.keyword_id],
                total_counts=r.total,
                daily_counts=daily_counts
            )
        )

    return WeeklyTrendResponse(
        start_date=start,
        end_date=today - timedelta(days=1),
        top_keywords=top_keywords,
        trend_data=trend_data
    )



@router.get("/search", response_model=SearchTrendResponse)
def search_trends(
    keyword: str,
    db:      Session = Depends(get_db),
):
    # 1) 날짜 범위: 오늘 포함 최근 7일
    end_date   = date.today() # - timedelta(days=1)
    start_date = end_date - timedelta(days=6)
    dates      = [start_date + timedelta(days=i) for i in range(7)]

    # 2) 키워드 유효성 검사
    kw = db.query(Keyword).filter(Keyword.name == keyword).first()
    if not kw:
        raise HTTPException(404, f"키워드 '{keyword}'를 찾을 수 없습니다.")

    # 3) 일별 전역 트렌드: cluster_keyword → keyword_id로 집계
    rows = (
        db.query(
            TrendKeyword.date.label("date"),
            func.sum(TrendKeyword.count).label("count")
        )
        .join(ClusterKeyword, ClusterKeyword.id == TrendKeyword.cluster_keyword_id)
        .filter(
            ClusterKeyword.keyword_id == kw.id,
            TrendKeyword.date >= start_date,
            TrendKeyword.date <= end_date
        )
        .group_by(TrendKeyword.date)
        .order_by(TrendKeyword.date)
        .all()
    )
    # 누락된 날짜는 0으로 채워줌
    trend_map = {r.date: r.count for r in rows}
    trend = [
        DailyCount(date=d, count=trend_map.get(d, 0))
        for d in dates
    ]

    # 4) 연관 클러스터 및 키워드 구성 (기존 로직 유지)
    related: List[RelatedKeyword] = []
    clusters = (
        db.query(Cluster)
          .join(ClusterKeyword, Cluster.id == ClusterKeyword.cluster_id)
          .filter(ClusterKeyword.keyword_id == kw.id)
          .all()
    )
    for cl in clusters:
        # 같은 클러스터의 다른 대표 키워드
        rep_kwds = [ck.keyword.name for ck in cl.cluster_keyword]
        co       = [w for w in rep_kwds if w != keyword]

        # 클러스터 내 기사 텍스트 모음
        articles  = (
            db.query(Article)
              .join(ClusterArticle, ClusterArticle.article_id == Article.id)
              .filter(ClusterArticle.cluster_id == cl.id)
              .all()
        )
        raw_texts = [art.title + " " + (art.summary or "") for art in articles]
        proc_texts= [preprocess_text(t) for t in raw_texts]

        # TF-IDF로 비대표 키워드 추출
        all_freqs = extract_top_keywords(
            documents=proc_texts,
            db=db,
            cluster_id=cl.id,
            top_n=3
        )
        nonrep = [w for w in all_freqs if w not in set(co + [keyword])]

        # 4-1) 클러스터별 일별 트렌드
        cl_rows = (
            db.query(
                TrendKeyword.date.label("date"),
                func.sum(TrendKeyword.count).label("count")
            )
            .filter(
                TrendKeyword.cluster_keyword_id == cl.id,
                TrendKeyword.date >= start_date,
                TrendKeyword.date <= end_date
            )
            .group_by(TrendKeyword.date)
            .order_by(TrendKeyword.date)
            .all()
        )
        cl_map   = {r.date: r.count for r in cl_rows}
        cl_trend = [
            DailyCount(date=d, count=cl_map.get(d, 0))
            for d in dates
        ]

        related.append(
            RelatedKeyword(
                cluster_id         = cl.id,
                created_at         = cl.created_at,
                co_keywords        = co,
                frequent_keywords  = nonrep,  # 스키마에 추가했다면 OK
                cluster_trend      = cl_trend
            )
        )

    return SearchTrendResponse(
        keyword          = keyword,
        trend            = trend,
        related_keywords = related
    )