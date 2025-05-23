from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

from database.deps import get_db                             # :contentReference[oaicite:0]{index=0}
from models.article import Article, ClusterArticle,            \
                             ClusterKeyword, Keyword  

class DailyCount(BaseModel):
    date: date
    count: int

class RelatedKeyword(BaseModel):
    cluster_id: int
    created_at: datetime
    co_keywords: List[str]
    frequent_keywords: List[str]

class SearchTrendResponse(BaseModel):
    keyword: str
    trend: List[DailyCount]
    related_keywords: List[RelatedKeyword]

class KeywordTrend(BaseModel):
    keyword: str
    total_counts: int
    daily_counts: List[DailyCount]

class WeeklyTrendResponse(BaseModel):
    start_date: date
    end_date: date
    top_keywords: List[str]
    trend_data: List[KeywordTrend]
