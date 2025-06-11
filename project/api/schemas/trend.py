from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from database.deps import get_db                             # :contentReference[oaicite:0]{index=0}
from models.article import Article, ClusterArticle,            \
                             ClusterKeyword, Keyword  

class DailyCount(BaseModel):
    date: date
    count: int

    model_config = ConfigDict(from_attributes=True)

class RelatedKeyword(BaseModel):
    cluster_id: int
    created_at: datetime
    co_keywords: List[str]
    frequent_keywords:  List[str]
    cluster_trend: List[DailyCount]

    model_config = ConfigDict(from_attributes=True)

class SearchTrendResponse(BaseModel):
    keyword: str
    trend: List[DailyCount]
    related_keywords: List[RelatedKeyword]

    model_config = ConfigDict(from_attributes=True)

class KeywordTrend(BaseModel):
    keyword: str
    total_counts: int
    daily_counts: List[DailyCount]

    model_config = ConfigDict(from_attributes=True)

class WeeklyTrendResponse(BaseModel):
    start_date: date
    end_date: date
    top_keywords: List[str]
    trend_data: List[KeywordTrend]

    model_config = ConfigDict(from_attributes=True)


class SuggestedKeywordsResponse(BaseModel):
    keywords: List[str]

    model_config = ConfigDict(from_attributes=True)