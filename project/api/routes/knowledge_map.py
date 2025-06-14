# api/routes/knowledge_map.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity

from models.article import Article
from models.user import User
from models.scrap import PKeyword, PKeywordArticle
from api.utils.auth import get_current_user_flexible as get_current_user
from api.utils.cache import get_cache
from tasks.user_scrap_pipeline import build_knowledge_map
from database.deps import get_db
from clustering.embedder import make_embeddings
from clustering.keyword_extractor import get_top_keywords
from api.schemas.knowledge_map import KnowledgeMapOut, Message
from api.schemas.cluster import ArticleOut
from tasks.user_scrap_pipeline import build_knowledge_map
from redis import Redis
router = APIRouter()

@router.post("/knowledge_map/update", response_model=Message)
def update_knowledge_map(current_user: User = Depends(get_current_user)):
    result = build_knowledge_map(current_user.id)
    if result == "SUCCESS":
        return {"message": "Knowledge map updated and cached in Redis"}
    else:
        raise HTTPException(status_code=500, detail="Knowledge map update failed")

# GET: 캐시된 지식맵 조회 or Celery 생성 요청
@router.get("/knowledge_map/graph", response_model=KnowledgeMapOut)
def get_or_create_knowledge_map_graph(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
   
    cache_key = f"user:{current_user.id}:knowledge_map"
    cached = get_cache(cache_key)
    
    if cached:
        try:
            # 검증된 모델로 감싸서 리턴
            return KnowledgeMapOut(**cached)
        except Exception as e:
            print(f"[Cache parsing error] {e}")
            redis_client.delete(cache_key)  # 캐시 삭제 (오류난 구조니까)
            return JSONResponse(
                status_code=500,
                content={"message": "캐시된 지식맵 데이터에 오류가 있습니다."}
            )

    # 없으면 생성 요청
    return JSONResponse(
        status_code=202,
        content={"message": "지식맵을 생성 중입니다. 잠시 후 다시 시도해주세요."}
    )

@router.get("/keywords/{keyword_id}/articles", response_model=list[ArticleOut])
def get_articles_by_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. 유저가 스크랩한 기사들 중에서
    # 2. keyword_id와 연결된 PKeywordArticle이 있는 것만 필터링
    results = (
        db.query(Article)
        .join(PKeywordArticle, PKeywordArticle.article_id == Article.id)
        .filter(PKeywordArticle.pkeyword_id == keyword_id)
        .all()
    )

    # ✅ FastAPI가 기대하는 스키마 형태에 맞게 매핑
    return [
        ArticleOut(
            article_id=article.id,  # ✅ 여기서 명시적으로 지정
            title=article.title,
            summary=article.summary,
            link=article.link,
            published=article.published,
        )
        for article in results
    ]