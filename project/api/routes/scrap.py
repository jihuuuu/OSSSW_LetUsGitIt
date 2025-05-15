# api/routes/scrap.py
# 역할: 기사 스크랩랩 관련 엔드포인트 모음

# 기사 스크랩 삭제 delete
# 기사 스크랩 목록 조회 get
# 기사 스크랩 상세 조회...? get

from database.sql_models import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.deps import get_db


router = APIRouter()

