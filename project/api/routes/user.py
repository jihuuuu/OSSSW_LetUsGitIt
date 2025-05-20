# api/routes/user.py
# 역할: 회원가입, 로그인, 토큰 갱신 등 사용자 인증 관련 엔드포인트 모음

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jose import jwt, JWTError, ExpiredSignatureError
from api.schemas.user import UserCreate, UserOut, UserLogin
from database.deps import get_db
from models.user import User
from api.config import SECRET_KEY, ALGORITHM
from api.utils.token import create_access_token, create_refresh_token

router = APIRouter()

# 1. 회원가입
@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 사용자 이름, 이메일 중복 검사
    # 중복 시 400 에러
    if db.query(User).filter((User.user_name == user.user_name) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    
    # 사용자 객체 생성
    # 요청 본문에 사용자 이름, 이메일, 비밀번호
    new_user = User(
        user_name=user.user_name,
        email=user.email,
        password_hash=bcrypt.hash(user.password) # 비밀번호 해싱
    )

    # DB에 사용자 추가
    db.add(new_user) # 세션에 객체 추가
    db.commit() # 세션에 추가된 객체를 DB에 반영
    db.refresh(new_user) # DB에서 새로 생성된 객체를 가져옴
    
    # UserOut 모델에 맞춰 반환
    return new_user

# 2. 로그인
@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    # 사용자명으로 유저 조회
    user_db = db.query(User).filter(User.username == user.username).first()
    
    # 사용자 정보가 없거나 비밀번호가 일치하지 않으면 401 에러
    if not user_db or not bcrypt.verify(user.password, user_db.password_hash):
        raise HTTPException(status_code=401, detail="로그인 정보가 일치하지 않습니다.")
    
    user_id = str(user_db.id)
    # JWT 액세스 토큰과 리프레시 토큰 생성
    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})

    # Refresh Token은 HTTPOnly 쿠키에 저장
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,       # HTTPS 환경에서만 전송됨
        samesite="strict", # CSRF 공격 방지
        path="/api/user/refresh" # 리프레시 토큰을 사용할 경로(API 엔드포인트)
    )

    # 액세스 토큰은 클라이언트에 반환(JS에서 저장하여 API 호출 시 사용)
    return {"access_token": access_token, "token_type": "bearer"}

# 3. 액세스 토큰 재발급 라우터
@router.post("/refresh")
def refresh_token(request: Request):
    # 쿠키에서 refresh_token 가져오기
    token = request.cookies.get("refresh_token")
    # 없으면 401 에러
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token이 없습니다.")

    # JWT 검증
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    # 유효하지 않거나 만료된 토큰이면 401 에러
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token이 만료되었습니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 refresh token입니다.")

    # 새로운 액세스 토큰 생성 후 반환
    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}

# 4. 로그아웃
@router.post("/logout")
def logout(response: Response):
    # 쿠키에서 refresh_token 삭제
    response.delete_cookie(key="refresh_token", path="/api/user/refresh")

    return {"message": "로그아웃 되었습니다."}
