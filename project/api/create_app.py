# api/create_app.py
# 역할: FastAPI 앱 인스턴스를 생성·설정하고, 모든 라우터를 등록하는 “팩토리 함수”를 제공

from fastapi import FastAPI

from .routes import news, cluster, user, scrap, article_notes, user_notes, knowledge_map

def create_app():
    app = FastAPI(title="뉴스 클러스터링 API")
    
    # 루트 엔드포인트 없으면 중간에 404 떠서 추가
    @app.get("/")
    async def root():
        return {"message": "Hello, world!"}
    
    app.include_router(news.router,    prefix="/api/news",    tags=["news"])
    app.include_router(cluster.router, prefix="/api/cluster", tags=["cluster"])
    app.include_router(user.router,    prefix="/user",    tags=["user"])
    app.include_router(user_notes.router, tags=["user-notes"])
    app.include_router(article_notes.router, tags=["article-notes"])
    app.include_router(scrap.router,   prefix="/api/scrap",   tags=["scrap"])
    app.include_router(knowledge_map.router, prefix="/api/knowledge-map", tags=["knowledge-map"])
    return app
