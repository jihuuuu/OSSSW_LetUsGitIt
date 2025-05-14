# api/create_app.py
# 역할: FastAPI 앱 인스턴스를 생성·설정하고, 모든 라우터를 등록하는 “팩토리 함수”를 제공

from fastapi import FastAPI
from .routes import news, cluster, user

def create_app():
    app = FastAPI(title="뉴스 클러스터링 API")
    app.include_router(news.router,    prefix="/api/news",    tags=["news"])
    # app.include_router(cluster.router, prefix="/api/cluster", tags=["cluster"])
    app.include_router(user.router,    prefix="/api/user",    tags=["user"])
    return app
