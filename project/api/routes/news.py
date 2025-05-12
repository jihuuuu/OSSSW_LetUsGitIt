# api/routes/news.py
# 역할: 기사 조회·검색·필터링용 엔드포인트 모음

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from collector.rss_collector import parse_and_store
from database.sql_models import Article
from api.schemas.news import NewsOut

router = APIRouter()

# 의존성: 요청마다 DB 세션을 열고 닫아 줍니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. MySQL에 저장된 기사 목록 조회 (제목만)
@router.get("/titles", response_model=list[NewsOut], summary="DB에 저장된 기사 제목만 조회")
def get_news_titles_only(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = (
        db.query(Article.id, Article.title)
          .order_by(Article.fetched_at.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )
    # Pydantic NewsOut 모델에 맞춰 dict로 반환
    return [{"id": a.id, "title": a.title, "link": None, "summary": None, "published": None} 
            for a in articles]

# 2. RSS 크롤링 → MySQL 저장 → 방금 저장된 기사 목록 반환
@router.post("/refresh", response_model=list[NewsOut], summary="RSS를 새로 크롤링해서 DB에 저장 후 반환")
def refresh_and_get_news(db: Session = Depends(get_db)):
    # 1) RSS → MySQL
    parse_and_store()

    # 2) 방금 저장된 기사 100건 조회 (가장 최근 저장순)
    recent = (
        db.query(Article)
          .order_by(Article.fetched_at.desc())
          .limit(100)
          .all()
    )
    # 3) Pydantic에 맞게 변환
    return [
        {
            "id": art.id,
            "title": art.title,
            "link": art.link,
            "summary": art.summary,
            "published": art.published,
        }
        for art in recent
    ]