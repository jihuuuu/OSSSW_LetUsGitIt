# models/base.py
# 역할: 공통 모델 정의
# db 테이블을 관계에 따라 나누어 정의

from sqlalchemy.orm import declarative_base

Base = declarative_base()