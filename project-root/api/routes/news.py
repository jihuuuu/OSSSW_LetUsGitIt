# api/routes/news.py

from fastapi import APIRouter
from database.connection import db
from collector.rss_collector import fetch_and_store_titles

router = APIRouter()

# 1. DB에 저장된 기사 목록 조회 - 제목만 (정적)
@router.get("/news/titles")
async def get_news_titles():
    cursor = db["news"].find({}, {"_id": 0, "title": 1})
    titles = await cursor.to_list(100)
    return titles

# 2. RSS에서 기사 크롤링 후 MongoDB에 저장 + 새로 가져오기 (동적)
@router.get("/news")
async def get_news_titles():
    news = await fetch_and_store_titles()
    return news
