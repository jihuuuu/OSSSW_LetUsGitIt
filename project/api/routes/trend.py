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
from fastapi_cache.decorator import cache


router = APIRouter()

# Okt 인스턴스와 불용어는 embedder.py 쪽에 정의돼 있다고 가정
_okt = Okt()

@router.get("/weekly", response_model=WeeklyTrendResponse)
@cache(expire=86400)  # 하루(24시간) 캐싱
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


@router.get("/suggested_keywords", response_model=SuggestedKeywordsResponse,
    summary="일주일간 이슈 키워드 조회", description="일주일(오늘 포함) 동안 trend_keyword 테이블을 집계해서 상위 키워드 리스트를 반환합니다."
)
@cache(expire=86400)  # 하루(24시간) 캐싱
def suggested_keywords(
    db: Session = Depends(get_db),
):
    # 1) 기간 설정: 오늘 포함 최근 7일
    end_date   = date.today()
    start_date = end_date - timedelta(days=7)

    # 2) date 범위 내에서 keyword별 count 합산 후 내림차순 정렬
    rows = (
        db.query(
            Keyword.name.label("keyword"),
            func.sum(TrendKeyword.count).label("total_count")
        )
        .join(ClusterKeyword, ClusterKeyword.id == TrendKeyword.cluster_keyword_id)
        .join(Keyword, Keyword.id == ClusterKeyword.keyword_id)
        .filter(TrendKeyword.date.between(start_date, end_date))
        .group_by(Keyword.name)
        .order_by(desc("total_count"))
        .all()
    )

    # 3) 결과 가공
    keywords: List[str] = [r.keyword for r in rows]
    return {"keywords": keywords}

@router.get("/search", response_model=SearchTrendResponse)
@cache(expire=86400)  # 하루(24시간) 캐싱
def search_trends(
    keyword: str,
    db:      Session = Depends(get_db),
):
    # 1) 날짜 범위: 오늘 포함 최근 7일
    end_date   = date.today() # - timedelta(days=1)
    start_date = end_date - timedelta(days=7)
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
            TrendKeyword.date.between(start_date, end_date)
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

    # 4) 연관 클러스터 + 대표 키워드 + 클러스터별 트렌드
    from sqlalchemy.orm import joinedload

    # 4-1) Cluster, ClusterKeyword, Keyword, TrendKeyword 를 한 번에 당겨오기
    ck_trend_rows = (
        db.query(
            TrendKeyword.cluster_keyword_id.label("ckid"),
            TrendKeyword.date,
            func.sum(TrendKeyword.count).label("cnt")
        )
        .filter(TrendKeyword.date.between(start_date, end_date))
        .group_by(TrendKeyword.cluster_keyword_id, TrendKeyword.date)
        .all()
    )
    # {ckid: {date: cnt}}
    from collections import defaultdict
    trend_by_ck = defaultdict(dict)
    for ckid, d, cnt in ck_trend_rows:
        trend_by_ck[ckid][d] = cnt

    clusters = (
        db.query(Cluster)
          .options(
            joinedload(Cluster.cluster_keyword)
              .joinedload(ClusterKeyword.keyword),
            joinedload(Cluster.cluster_article)
              .joinedload(ClusterArticle.article)
          )
          .join(ClusterKeyword, Cluster.id == ClusterKeyword.cluster_id)
          .filter(ClusterKeyword.keyword_id == kw.id)
          .all()
    )

    related: List[RelatedKeyword] = []
    for cl in clusters:
        # 대표 키워드 리스트
        rep_kwds = [ck.keyword.name for ck in cl.cluster_keyword]
        co       = [w for w in rep_kwds if w != keyword]

        # 클러스터 내 기사 텍스트 모음
        # articles  = (
        #     db.query(Article)
        #       .join(ClusterArticle, ClusterArticle.article_id == Article.id)
        #       .filter(ClusterArticle.cluster_id == cl.id)
        #       .all()
        # )
        # raw_texts = [art.title + " " + (art.summary or "") for art in articles]
        # proc_texts= [preprocess_text(t) for t in raw_texts]

        # # TF-IDF로 비대표 키워드 추출
        # all_freqs = extract_top_keywords(
        #     documents=proc_texts,
        #     cluster_id=cl.id,
        #     top_n=3
        # )
        # nonrep = [w for w in all_freqs if w not in set(co + [keyword])]

        # 클러스터별 날짜 트렌드 채우기
        ckid   = cl.cluster_keyword[0].id   # 이 클러스터의 대표 키워드 ID
        cl_tr  = [
            DailyCount(date=d, count=trend_by_ck[ckid].get(d,0))
            for d in dates
        ]

        related.append(
            RelatedKeyword(
                cluster_id         = cl.id,
                created_at         = cl.created_at,
                co_keywords        = co,
                frequent_keywords  = [],  # 스키마에 추가했다면 OK
                cluster_trend      = cl_tr
            )
        )

    return SearchTrendResponse(
        keyword          = keyword,
        trend            = trend,
        related_keywords = related
    )