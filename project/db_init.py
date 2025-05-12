# db_init.py
from database.connection import engine
from database.sql_models import Base

Base.metadata.create_all(bind=engine)
print("✅ articles 테이블 생성 완료")
