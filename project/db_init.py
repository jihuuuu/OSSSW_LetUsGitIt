# db_init.py
from database.connection import engine
from models.base import Base

Base.metadata.create_all(bind=engine)
print("테이블 생성 완료")
