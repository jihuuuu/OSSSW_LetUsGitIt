# api/utils/auth.py

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from api.config import SECRET_KEY, ALGORITHM
from database.deps import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰 payload 오류")
    except JWTError:
        raise HTTPException(status_code=401, detail="토큰 인증 실패")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자 없음")

    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def get_current_user_flexible(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # 1. 우선 access token 헤더 확인
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="access token payload 오류")
            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                raise HTTPException(status_code=401, detail="사용자 없음")
            return user
        except JWTError:
            pass

    # 2. access 실패 → refresh token fallback
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="refresh token 없음")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="refresh token 타입 오류")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="refresh token payload 오류")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="사용자 없음")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="refresh token 디코딩 오류")
