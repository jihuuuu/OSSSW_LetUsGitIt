# api/routes/user.py
# 역할: 회원가입, 로그인, 토큰 갱신 등 사용자 인증 관련 엔드포인트 모음

from datetime import datetime, timedelta
from passlib.hash import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from database.deps import get_db
from models.user import User
from api.schemas.user import UserCreate, UserLogin
from api.utils.auth import verify_password, get_current_user
from api.utils.token import create_access_token, create_refresh_token
from api.config import SECRET_KEY, ALGORITHM, COOKIE_SECURE, COOKIE_PATH, COOKIE_SAMESITE
import re
from uuid import uuid4
from api.utils.logger import logger

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

@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    # username 기준으로 사용자 조회
    db_user = db.query(User).filter(User.email == user.email).first()

    # 로그인 실패
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "errorCode": "INVALID_CREDENTIALS",
                "message": "이메일 또는 비밀번호가 올바르지 않습니다."
            }
        )

    # 로그인 성공 → 토큰 생성
    access_token = create_access_token({"sub": str(db_user.id), "type": "access"})
    # refrest token rotation을 위한 jti 활용
    jti = str(uuid4())
    refresh_token = create_refresh_token({"sub": str(db_user.id), "type": "refresh"}, jti=jti)
    # DB에 refresh token 저장 (선택적, 보안 고려)
    db_user.refresh_token_id = jti
    db.commit()

    # refresh_token을 httpOnly 쿠키로 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 3600,  # 7일
        secure=COOKIE_SECURE,  # HTTPS 환경에서만 쿠키 전송
        path=COOKIE_PATH,  
        samesite=COOKIE_SAMESITE  # CSRF 공격 방지 설정
    )

    return {
        "message": "로그인에 성공했습니다.",
        "access_token": access_token,
        "user_id": db_user.id   
    }

# 로그아웃
@router.post("/logout")
def logout(response: Response):
    # 쿠키 삭제: refresh_token
    response.delete_cookie(key="refresh_token")
    return {
        "message": "로그아웃이 완료되었습니다."
    }

# 토큰 유효성 검사 API
@router.get("/me")
def read_current_user(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}

# 토큰 만료 시 새 access token 발급
@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="refresh_token 없음")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰 타입입니다")
        user_id = payload.get("sub")
        jti = payload.get("jti")  # ✅ 기존 토큰의 고유 ID
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰 유효하지 않음")

    # 사용자 조회
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자 없음")

    # jti 재사용 탐지 로깅
    if user.refresh_token_id != jti:
        logger.warning(
            f"[REUSE ATTEMPT] user_id={user_id}, ip={request.client.host}, jti={jti}, expected={user.refresh_token_id}"
        )
        raise HTTPException(status_code=401, detail="이미 사용된 refresh token입니다")

    # 짧은 주기 요청 감지 로깅 (현재 기준: 10초 미만)
    if user.last_token_used_at and datetime.now() - user.last_token_used_at < timedelta(seconds=10):
        logger.warning(
            f"[SUSPICIOUS REFRESH] user_id={user_id}, ip={request.client.host}, now={datetime.now().isoformat()}, last={user.last_token_used_at.isoformat()}"
        )
        raise HTTPException(status_code=429, detail="refresh 요청이 너무 자주 발생합니다")

    # 새 토큰 발급
    new_jti = str(uuid4())
    new_refresh_token = create_refresh_token({"sub": user_id, "type": "refresh"}, jti=new_jti)
    user.refresh_token_id = new_jti
    user.last_token_used_at = datetime.now()
    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=7 * 24 * 3600,
        secure=COOKIE_SECURE,
        path=COOKIE_PATH,
        samesite=COOKIE_SAMESITE
    )

    new_access_token = create_access_token({
        "sub": str(user_id),
        "type": "access"
    })
    return {"access_token": new_access_token}
