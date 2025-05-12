# api/routes/news.py
# 기사 관련 API를 구현하는 FastAPI 라우터입니다.
from fastapi import APIRouter
from mongodb.connection import db
from collector.rss_collector import fetch_and_store_titles

router = APIRouter()

# 1. DB에 저장된 기사 목록 조회 - 제목만 (정적)
@router.get("/news/titles")
async def get_news_titles_only():
    cursor = db["news"].find({}, {"_id": 0, "title": 1})
    titles = await cursor.to_list(100)
    return titles

# 2. RSS에서 기사 크롤링 후 MongoDB에 저장 + 새로 가져오기 (동적)
@router.get("/news")
async def get_and_save_news():
    raw_news = await fetch_and_store_titles()
    
    # ObjectId 문제 해결: _id 제거 or 문자열 변환
    clean_news = []
    for doc in raw_news:
        doc.pop("_id", None)  # 안전하게 _id 제거
        clean_news.append(doc)

    return clean_news
