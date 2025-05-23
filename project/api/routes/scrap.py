# api/routes/scrap.py
# 역할: 기사 스크랩랩 관련 엔드포인트 모음

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database.deps import get_db
from api.schemas.scrap import *

from models.scrap import Scrap        # 스크랩 모델
from models.article import Article    # 기사 모델
from models.note import NoteArticle, Note  # 노트-기사 매핑 및 노트 모델

# 인증 유저를 가져오는 의존성 (실제 구현에 따라 변경)
from api.utils.auth import get_current_user
from models.user import User

router = APIRouter()


# --- 1) 기사 스크랩 ---
@router.post(
    "/articles/{article_id}/scrap",
    response_model=ScrapCreateResponse,
    summary="기사 스크랩"
)
def scrap_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1) 기사 존재 확인
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(404, "Article not found")

    # 2) 기존 스크랩 조회
    scrap = (
        db.query(Scrap)
          .filter_by(article_id=article_id, user_id=current_user.id)
          .first()
    )
    if scrap:
        if scrap.state:
            raise HTTPException(400, "Already scrapped")
        scrap.state = True
        scrap.updated_at = datetime.utcnow()
    else:
        scrap = Scrap(article_id=article_id, user_id=current_user.id)
        db.add(scrap)

    db.commit()
    db.refresh(scrap)

    # 2) wrapper 객체로 리턴
    return ScrapCreateResponse(
        isSuccess=True,
        code="SCRAP_CREATED",
        message="스크랩이 성공적으로 등록되었습니다.",
        result=ScrapCreateResult(
            scrapId    = scrap.id,
            userId     = scrap.user_id,
            articleId  = scrap.article_id,
            state      = scrap.state,
            created_at = scrap.created_at,
            updated_at = scrap.updated_at,
        )
    )


# --- 2) 스크랩 기사 전체 조회 / 제목 검색 ---
@router.get(
    "/scraps",
    response_model=List[ScrapWithArticle],
    summary="스크랩 기사 목록 조회 (최신순 & 제목 검색 가능)"
)
def list_scraps(
    title: Optional[str] = Query(None, description="검색할 기사 제목 키워드"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Scrap)
          .join(Article)
          .filter(Scrap.user_id == current_user.id, Scrap.state == True)
    )
    if title:
        query = query.filter(Article.title.contains(title))
    scraps = query.order_by(Scrap.created_at.desc()).all()

    return [
        ScrapWithArticle(
            scrap_id   = s.id,
            article    = ArticleOut.from_orm(s.article),
            created_at = s.created_at
        )
        for s in scraps
    ]


# --- 3) 스크랩 취소 ---
@router.put(
    "/articles/{article_id}/unscrap",
    response_model=ScrapCancelResponse,
    summary="스크랩 취소"
)
def unscrap_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scrap = (
        db.query(Scrap)
          .filter_by(article_id=article_id, user_id=current_user.id, state=True)
          .first()
    )
    if not scrap:
        raise HTTPException(404, "No active scrap found")
    
    scrap.state = False
    scrap.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(scrap)

    # 3) wrapper 씌워서 반환
    return ScrapCancelResponse(
        isSuccess=True,
        code="SCRAP_CANCELLED",
        message="스크랩이 성공적으로 취소되었습니다.",
        result=ScrapCreateResult(
            scrapId    = scrap.id,
            userId     = scrap.user_id,
            articleId  = scrap.article_id,
            state      = scrap.state,
            created_at = scrap.created_at,
            updated_at = scrap.updated_at,
        )
    )


# --- 4) 스크랩된 기사에 달린 노트 조회 ---
@router.get(
    "/scraps/{scrap_id}/notes",
    response_model=List[NoteOut],
    summary="스크랩 기사별 관련 노트 조회"
)
def get_notes_for_scrap(
    scrap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1) 스크랩 존재 및 소유권 확인
    scrap = (
        db.query(Scrap)
          .filter_by(id=scrap_id, user_id=current_user.id)
          .first()
    )
    if not scrap:
        raise HTTPException(404, "Scrap not found")

    # 2) 해당 기사(article_id)에 연결된 NoteArticle 조회
    note_articles = (
        db.query(NoteArticle)
          .join(Note)
          .filter(
              NoteArticle.article_id == scrap.article_id,
              Note.user_id == current_user.id,
              Note.state == True
          )
          .all()
    )
    return [na.note for na in note_articles]

