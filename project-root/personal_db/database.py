from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# .env에서 환경변수 로드
DATABASE_URL = os.getenv("MYSQL_URL")
print(f"Connecting to database at {DATABASE_URL}")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
