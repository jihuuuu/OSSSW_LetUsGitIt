from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List
from pydantic import ConfigDict

class KeywordCount(BaseModel):
    keyword: str
    article_count: int

    model_config = ConfigDict(from_attributes=True)

class KeywordsTodayOut(BaseModel):
    cluster_id: int
    created_at: datetime
    keywords: List[KeywordCount]

    model_config = ConfigDict(from_attributes=True)

class ArticleOut(BaseModel):
    article_id: int
    title: str
    summary: str
    link: HttpUrl
    published: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ClusterOut(BaseModel):
    cluster_id: int
    created_at: datetime
    label: int
    num_articles: int
    keywords: List[str]
    articles: List[ArticleOut]

    model_config = ConfigDict(from_attributes=True)
