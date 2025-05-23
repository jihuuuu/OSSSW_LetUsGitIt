# api/routes/user.py
# 역할: 회원가입, 로그인, 토큰 갱신 등 사용자 인증 관련 엔드포인트 모음

from datetime import datetime, timedelta
from passlib.hash import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from jose import jwt
from database.deps import get_db
from models.user import User
from api.schemas.user import UserCreate, UserLogin
from api.utils.auth import verify_password
from api.config import SECRET_KEY, ALGORITHM
import re

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 1. 비밀번호 불일치 확인
    if user.password != user.password_chk:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errorCode": "PASSWORD_MISMATCH", "message": "비밀번호가 일치하지 않습니다."}
        )

    # 2. 이메일 형식 검증
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errorCode": "INVALID_EMAIL_FORMAT", "message": "이메일 형식이 올바르지 않습니다."}
        )

    # 3. 이메일 중복 검사
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"errorCode": "EMAIL_ALREADY_EXISTS", "message": "이미 가입된 이메일입니다."}
        )

    # 4. 사용자 생성
    new_user = User(
        user_name=user.user_name,
        email=user.email,
        password=bcrypt.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "회원가입이 완료되었습니다.",
        "user": {
            "id": new_user.id,
            "user_name": new_user.user_name,
            "email": new_user.email,
            "created_at": new_user.created_at,
            "updated_at": new_user.updated_at
        }
    }

def create_access_token(user_id: int, expires_delta: timedelta):
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    # username 기준으로 사용자 조회
    db_user = db.query(User).filter(User.user_name == user.user_name).first()

    # 로그인 실패
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "errorCode": "INVALID_CREDENTIALS",
                "message": "아이디 또는 비밀번호가 올바르지 않습니다."
            }
        )

    # 로그인 성공 → 토큰 생성
    access_token = create_access_token(user_id=db_user.id, expires_delta=timedelta(minutes=15))
    refresh_token = create_refresh_token(user_id=db_user.id)

    # refresh_token을 httpOnly 쿠키로 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 3600  # 7일
    )

    return {
        "message": "로그인에 성공했습니다.",
        "access_token": access_token
    }

# 로그아웃
@router.post("/logout")
def logout(response: Response):
    # 쿠키 삭제: refresh_token
    response.delete_cookie(key="refresh_token")
    return {
        "message": "로그아웃이 완료되었습니다."
    }