# database/connection.py
# 역할: 각 데이터 저장소(몽고DB, RDBMS)에 연결할 수 있는 “세션·클라이언트”를 한 곳에서 생성·내보냅니다.

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# ────────────────────────────────────────────────────────────────────
# 1) .env 파일 로드
# 프로젝트 루트의 .env 파일을 읽어서 os.environ에 등록합니다.
# 프로젝트 루트 기준으로 .env를 찾도록
env_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=env_path) 
# ────────────────────────────────────────────────────────────────────

print("▶︎ ❄️ .env 경로:", env_path)
print("MYSQL_USER env:", os.getenv("MYSQL_USER"))
print("MYSQL_DB   env:", os.getenv("MYSQL_DB"))

# 2) 환경변수에서 접속 정보 읽기
# api/config.py에서 설정한 DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME을 가져옴

if not all([DB_USER, DB_PASS, DB_NAME]):
    raise RuntimeError("🚨 .env에서 MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB가 설정되어 있는지 확인하세요.")

# 3) SQLAlchemy 접속 URL 구성 (PyMySQL 드라이버 사용 예)
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

# **디버깅**: 실제 URL을 터미널에 찍어 보고 싶다면 아래 프린트 활성화
print("▶︎ Connecting to DB:", SQLALCHEMY_DATABASE_URL)

# 4) Engine 생성 (echo=True로 SQL 로그를 볼 수도 있습니다)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,       # True로 하면 CREATE TABLE 같은 SQL을 콘솔에 보여 줌
    pool_pre_ping=True,
)

# 5) 세션 팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
