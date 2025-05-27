# api/create_app.py
# 역할: FastAPI 앱 인스턴스를 생성·설정하고, 모든 라우터를 등록하는 “팩토리 함수”를 제공

from fastapi import FastAPI
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routes import cluster, knowledge_map, news, notes, scrap, trend, user

from starlette.concurrency import run_in_threadpool
from clustering.pipeline import run_embedding_stage, run_clustering_stage
from models.user import User
from fastapi.middleware.cors import CORSMiddleware
from api.routes.scrap import router as scrap_router
from api.utils.auth import get_current_user
from tasks.user_scrap_pipeline import generate_user_scrap_knowledge_maps
from database.connection import SessionLocal

def hourly_clustering():
    """
    지난 24시간 기사로 임베딩 생성 → 클러스터링 수행 및 DB 저장
    매시 정각마다 실행됩니다.
    """
    # 임베딩 생성 (지난 24시간)
    embs = run_embedding_stage(batch_size=32, since_hours=24)
    if embs is None:
        print("⚠️ 지난 24시간 내 임베딩할 기사가 없습니다.")
        return

    # 클러스터링 수행 및 DB 저장
    run_clustering_stage(
        emb_path="data/article_embeddings.npy",
        method="kmeans",
        n_clusters=10,
        eps=None,
        min_samples=None,
        limit=None,
        save_db=True
    )
    print("✅ 한 시간 단위 클러스터링 완료")
    # 사용자별 스크랩 기반 지식맵 추가
    db = SessionLocal()
    try:
        generate_user_scrap_knowledge_maps(db)
    finally:
        db.close()

def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    # 매시간 정각에 실행되도록 cron 트리거만 등록 (next_run_time 제거)
    scheduler.add_job(hourly_clustering, trigger="cron", minute=0)
    return scheduler

# 더미 유저 반환 함수 (test용)
def fake_current_user():
    # DB에 id=1 유저가 있어야 합니다
    return User(id=1)


def create_app():
    app = FastAPI(title="뉴스 클러스터링 API")

    scheduler = create_scheduler()

    @app.on_event("startup")
    async def startup_event():
        # 서버 구동 시 한 번만 스케줄러 시작
        scheduler.start()  
        # 앱 띄울 때 초기 한 번 실행을 원하면 직접 호출
        await run_in_threadpool(hourly_clustering) 

    @app.on_event("shutdown")
    async def shutdown_event():
        scheduler.shutdown()
    
    # 루트 엔드포인트 없으면 중간에 404 떠서 추가
    @app.get("/")
    async def root():
        return {"message": "Hello, world!"}
    
    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # 프론트 개발 서버 주소
        allow_credentials=True,
        allow_methods=["*"],                      # GET, POST, PUT, OPTIONS 모두 허용
        allow_headers=["*"],                      # 모든 헤더 허용
    )

    # 2) 원래 인증 의존성을 가짜 함수로 교체
    app.dependency_overrides[get_current_user] = fake_current_user

    app.include_router(news.router,    prefix="/news",    tags=["news"])
    app.include_router(cluster.router, prefix="/clusters", tags=["cluster"])
    app.include_router(user.router,    prefix="/users",    tags=["user"])
    app.include_router(scrap.router,    prefix="/users",    tags=["scrap"])
    app.include_router(trend.router,    prefix="/trends",    tags=["trend"])
    app.include_router(notes.router, prefix="/users", tags=["notes"])
    app.include_router(knowledge_map.router, prefix="/users", tags=["knowledge-map"])

    return app

