# api/routes/scrap.py
# 역할: 기사 스크랩랩 관련 엔드포인트 모음

from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
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
    response_model=PagedScraps,
    summary="스크랩 기사 목록 조회 (페이징&검색)"
)
def list_scraps(
    title: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Scrap).join(Article).filter(
        Scrap.user_id==current_user.id, Scrap.state==True
    )
    if title:
        q = q.filter(Article.title.contains(title))

    total = q.count()
    scraps = (
        q.order_by(Scrap.created_at.desc())
         .offset((page-1)*size)
         .limit(size)
         .all()
    )
    articles = [ArticleOut.from_orm(s.article) for s in scraps]
    return PagedScraps(
        articles   = articles,
        totalPages = ceil(total/size),
    )


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
