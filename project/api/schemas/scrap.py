from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ScrapCreateResult(BaseModel):
    scrapId: int
    userId: int
    articleId: int
    state: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScrapCreateResponse(BaseModel):
    isSuccess: bool
    code: str
    message: str
    result: ScrapCreateResult

    model_config = ConfigDict(from_attributes=True)


class ScrapCancelResponse(BaseModel):
    isSuccess: bool
    code: str
    message: str
    result: ScrapCreateResult

    model_config = ConfigDict(from_attributes=True)


class ArticleOut(BaseModel):
    id: int
    title: str
    link: str
    summary: str | None
    published: datetime

    model_config = ConfigDict(from_attributes=True)


class ScrapWithArticle(BaseModel):
    scrap_id: int
    article: ArticleOut
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteOut(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime

    class Config:
        orm_mode = True