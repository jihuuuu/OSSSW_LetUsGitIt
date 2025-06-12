# api/config.py
# 배포/보안 설정 모델

import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Extra

# .env 파일 로딩
env_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# JWT 설정
SECRET_KEY = os.getenv("JWT_SECRET", "fallback-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

# DB 설정 (연결 URL은 connection.py에서 사용)
DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DB")

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        extra = Extra.ignore

# 싱글턴으로 쓰기
settings = Settings()