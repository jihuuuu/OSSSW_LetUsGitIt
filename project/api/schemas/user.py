#api/schemas/user.py
from pydantic import BaseModel, EmailStr

# 회원가입 요청 시 사용할 모델
class UserCreate(BaseModel):
    user_name: str
    email: EmailStr # 유효한 이메일 형식 검증
    password: str # 평문으로 받아 해싱

# 회원정보 응답 시 사용할 모델
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True # SQLAlchemy 모델을 자동으로 Pydantic 모델로 변환

# 로그인 요청 시 사용할 모델델
class UserLogin(BaseModel):
    username: str
    password: str
