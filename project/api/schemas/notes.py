# api/schemas/notes.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .common import StandardResponse
from pydantic import ConfigDict

# 1. 노트 생성 요청
class NoteCreateRequest(BaseModel):
    title: str
    text: str
    article_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


# 2. 노트 수정 요청
class NoteUpdateRequest(BaseModel):
    title: str
    text: str
    article_ids: Optional[List[int]] = None

    model_config = ConfigDict(from_attributes=True)


# 3. 요약된 기사 정보 (노트 생성/조회에 사용)
class ArticleOut(BaseModel):
    id: int
    title: str
    link: str

    model_config = ConfigDict(from_attributes=True)


# 4. 노트 생성/수정 응답의 result 부분
class NoteCreateResult(BaseModel):
    userId: int
    noteId: int
    title: str
    text: str
    state: bool
    created_at: datetime
    updated_at: datetime
    articles: List[ArticleOut]

    model_config = ConfigDict(from_attributes=True)

NoteCreateResponse = StandardResponse[NoteCreateResult]


# 5. 노트 목록 아이템
class NoteListItem(BaseModel):
    note_id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 6. 노트 목록 조회 결과 (페이징)
class NoteListResult(BaseModel):
    page: int
    size: int
    total: int
    totalPages: int
    notes: List[NoteListItem]

    model_config = ConfigDict(from_attributes=True)

NoteListResponse = StandardResponse[NoteListResult]


# 7. 기사 상세 정보
class ArticleSummary(BaseModel):
    id: int
    title: str
    link: str
    summary: str

    model_config = ConfigDict(from_attributes=True)


# 8. 노트 상세 정보 result
class NoteDetail(BaseModel):
    note_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: datetime
    articles: List[ArticleSummary]

    model_config = ConfigDict(from_attributes=True)

NoteDetailResponse = StandardResponse[NoteDetail]