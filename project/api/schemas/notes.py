# api/schemas/notes.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

#  1. 노트 생성 요청
class NoteCreateRequest(BaseModel):
    title: str
    text: str
    article_ids: List[int]

#  2. 노트 수정 요청
class NoteUpdateRequest(BaseModel):
    title: str
    text: str
    article_ids: Optional[List[int]] = None

#  3. 요약된 기사 정보 (노트 생성/조회에 사용)
class ArticleOut(BaseModel):
    id: int
    title: str
    link: str

#  4. 노트 생성 응답 구조
class NoteCreateResult(BaseModel):
    userId: int
    noteId: int
    title: str
    text: str
    state: bool
    created_at: datetime
    updated_at: datetime
    articles: List[ArticleOut]

class NoteCreateResponse(BaseModel):
    isSuccess: bool
    code: int
    message: str
    result: NoteCreateResult

#  5. 노트 목록 응답용 요약
class NoteSummary(BaseModel):
    note_id: int
    title: str
    created_at: datetime

#  6. 노트 상세 보기 응답
class ArticleSummary(BaseModel):
    id: int
    title: str
    link: str
    summary: str

class NoteDetail(BaseModel):
    note_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: datetime
    articles: List[ArticleSummary]
