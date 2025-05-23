# api/utils/auth.py

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTErrorq
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from api.config import SECRET_KEY, ALGORITHM
from database.deps import get_db
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


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


def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="refresh_token 없음")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="쿠키 토큰 유효성 실패")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자 없음")

    return user
