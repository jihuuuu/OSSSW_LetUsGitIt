# database/connection.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["news_db"]  # 사용할 DB 이름