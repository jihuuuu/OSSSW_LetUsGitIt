# utils/token.py
# 확장성, 재사용성을 위해 token 관련 기능을 utils로 분리
# JWT 토큰 생성 및 검증을 위한 유틸리티 함수들

from datetime import datetime, timezone, timedelta
from jose import jwt
from api.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE

# 인증된 사용자 정보 기반으로 JWT 액세스 토큰 생성
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 인증된 사용자 정보 기반으로 JWT 리프레시 토큰 생성
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
