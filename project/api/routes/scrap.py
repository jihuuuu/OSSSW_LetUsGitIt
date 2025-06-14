# api/routes/scrap.py
# 역할: 기사 스크랩 관련 엔드포인트 모음

from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from tasks.user_scrap_pipeline import build_knowledge_map
from database.deps import get_db
from api.schemas.scrap import *

from models.scrap import Scrap, PKeyword, PKeywordArticle        # 스크랩 모델
from models.user import KnowledgeMap
from models.article import Article    # 기사 모델
from models.note import NoteArticle, Note  # 노트-기사 매핑 및 노트 모델

# 인증 유저를 가져오는 의존성 (실제 구현에 따라 변경)
from api.utils.auth import get_current_user_flexible as get_current_user
from models.user import User

# 스크랩 시 pkeyword, knowledgemap db 업데이트
from clustering.keyword_extractor import extract_keywords_per_article, get_top_keywords
from clustering.embedder import preprocess_text
from api.utils.cache import delete_cache
from redis import Redis

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
    
    cache_key = f"user:{current_user.id}:knowledge_map"
    delete_cache(cache_key)
    
    # 기존 유효한 지식맵 비활성화
    db.query(KnowledgeMap).filter_by(user_id=current_user.id, is_valid=True).update({"is_valid": False})
    
    # 1. 기사 존재 확인
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(404, "Article not found")

    # 2. 기존 스크랩 확인 및 상태 변경
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

    # 3. 키워드 추출
    preprocessed = preprocess_text(article.title + " " + (article.summary or ""))
    keywords_list = extract_keywords_per_article([preprocessed])
    keywords = keywords_list[0]
    # 디버깅용 출력
    print(f"Extracted keywords: {keywords}")

     # 4. 기존 PKeyword 불러오기
    pkeyword_dict = {pk.name: pk for pk in db.query(PKeyword).filter_by(user_id=current_user.id).all()}

    for keyword in keywords:
        if keyword in pkeyword_dict:
            pk = pkeyword_dict[keyword]
            pk.count += 1
        else:
            pk = PKeyword(user_id=current_user.id, name=keyword, count=1)
            db.add(pk)
            db.flush()
            pkeyword_dict[keyword] = pk

        # 중간테이블 연결
        existing_link = db.query(PKeywordArticle).filter_by(pkeyword_id=pk.id, article_id=article.id).first()
        if not existing_link:
            db.add(PKeywordArticle(pkeyword_id=pk.id, article_id=article.id))

    # 5. 커밋
    db.commit()
    db.refresh(scrap)

    # 6. 지식맵 생성(celery task 실행)
    build_knowledge_map(current_user.id)
    
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
