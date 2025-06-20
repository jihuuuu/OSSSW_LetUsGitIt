# api/create_app.py
# 역할: FastAPI 앱 인스턴스를 생성·설정하고, 모든 라우터를 등록하는 “팩토리 함수”를 제공

from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routes import cluster, knowledge_map, news, notes, scrap, trend, user
from starlette.concurrency import run_in_threadpool
from clustering.pipeline_by_topic import run_all_topics_pipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
#from tasks.user_scrap_pipeline import generate_user_scrap_knowledge_maps
from database.connection import SessionLocal
from collector.rss_collector import parse_and_store
from tasks.daily_trend import generate_daily_trend
from fastapi_cache import FastAPICache            # 캐시 초기화
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from .config import settings
import traceback
import redis
import asyncio


def hourly_clustering():
    """
    매시 정각에 실행되는 함수:
    1) RSS 파싱 → MySQL 저장 (parse_and_store)
    2) 모든 토픽에 대해 run_all_topics_pipeline 실행 (임베딩→클러스터링→키워드 추출)
    3) 사용자 스크랩 기반 지식맵 생성
    """
    # 1) RSS 크롤링 & DB 저장
    print("⏳ [Pipeline] RSS 크롤링 시작…")
    try:
        parse_and_store()
        print("✅ [Pipeline] RSS 크롤링 완료.")
    except Exception as e:
        print(f"⚠️ [Pipeline] RSS 크롤링 중 에러 발생: {e}")
        traceback.print_exc()

    # 2) 토픽별 전체 파이프라인 실행
    print("⏳ [Pipeline] 토픽별 전체 파이프라인 실행…")
    try:
        # 기본값: kmeans, 클러스터 개수 10, eps=0.5, min_samples=5, since_hours=24, data_dir="data"
        run_all_topics_pipeline(
            clustering_method="kmeans",
            k=10,
            eps=0.5,
            min_samples=5,
            since_hours=24,
            data_dir="data",
            save_db=True
        )
        print("✅ [Pipeline] 토픽별 전체 파이프라인 완료.")
    except Exception as e:
        print(f"⚠️ [Pipeline] 토픽별 파이프라인 중 에러 발생: {e}")
        traceback.print_exc()

    # 사용자별 스크랩 기반 지식맵 추가
    """ 
    db = SessionLocal()
    try:
        generate_user_scrap_knowledge_maps(db)
    finally:
        db.close()"""

def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
    # 매시간 정각에 실행되도록 cron 트리거만 등록 (next_run_time 제거)
    scheduler.add_job(hourly_clustering, trigger="cron", minute=0, coalesce=True, misfire_grace_time=600)
    # 매일 자정에 이전 24시간 트렌드 집계
    scheduler.add_job(generate_daily_trend, trigger='cron', hour=0, minute=0, id='daily_trend_job', replace_existing=True)
    return scheduler

def create_app():
    app = FastAPI(title="뉴스 클러스터링 API")

    # Swagger UI에서 수동 Bearer 토큰 테스트를 위한 securitySchemes 추가
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description="뉴스 클러스터링 및 노트 API",
            routes=app.routes,
        )
        # HTTP Bearer 스킴 등록
        openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
        openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
        # 2) 모든 경로에 보안 요건 추가
        for path in openapi_schema["paths"].values():
            for op in path.values():
                op.setdefault("security", []).append({"bearerAuth": []})
        app.openapi_schema = openapi_schema
        return openapi_schema

    app.openapi = custom_openapi
    
    scheduler = create_scheduler()

    @app.on_event("startup")
    async def startup_event():
        # 1) Redis 연결 및 캐시 초기화
        redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
        # 2) 기존 스케줄러·파이프라인
        # 서버 구동 시 한 번만 스케줄러 시작
        scheduler.start()  
        # 초기 클러스터링 (백그라운드)
        # 초기 트렌드 집계 (백그라운드)
        asyncio.create_task(run_in_threadpool(hourly_clustering))
        asyncio.create_task(run_in_threadpool(generate_daily_trend))


    @app.on_event("shutdown")
    async def shutdown_event():
        scheduler.shutdown()
    
    @app.get("/")
    async def root():
        return {"message": "Hello, world!"}
    

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://3.35.66.161:5173"],  # 프론트 개발 서버 주소
        allow_credentials=True,
        allow_methods=["*"],                      # GET, POST, PUT, OPTIONS 모두 허용
        allow_headers=["*"],                      # 모든 헤더 허용
    )


    # app.include_router(news.router,    prefix="/news",    tags=["news"])
    app.include_router(cluster.router, prefix="/clusters", tags=["cluster"])
    app.include_router(user.router,    prefix="/users",    tags=["user"])
    app.include_router(scrap.router,    prefix="/users",    tags=["scrap"])
    app.include_router(trend.router,    prefix="/trends",    tags=["trend"])
    app.include_router(notes.router, prefix="/users", tags=["notes"])
    app.include_router(knowledge_map.router, prefix="/users", tags=["knowledge_map"])


    return app


