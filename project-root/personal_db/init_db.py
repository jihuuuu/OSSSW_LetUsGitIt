from sqlalchemy import create_engine
from personal_db.database import Base
from personal_db.models.user import User
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
DATABASE_URL = os.getenv("MYSQL_URL")

# SQLAlchemy 엔진으로 테이블 생성
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

print("원격 DB에 users 테이블 생성 완료")
