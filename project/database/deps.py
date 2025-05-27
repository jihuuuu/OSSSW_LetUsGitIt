# database/deps.py
# 역할: DB 세션을 관리하는 의존성 주입 모듈

from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
