# 1) 베이스 이미지: 가볍고 최신 파이썬
FROM python:3.12

# JDK 설치 (Debian/Ubuntu 계열 기준)
RUN apt-get update && \
    apt-get install -y default-jdk-headless && \
    rm -rf /var/lib/apt/lists/*

# 2) 앱 실행 디렉터리 설정
WORKDIR /app

# 3) 의존성 파일 먼저 복사 (이후 변경 없으면 캐시 활용)
COPY requirements.txt .

# 4) 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5) 앱 소스 전체 복사
COPY . .

# 6) 컨테이너 기동 시 uvicorn으로 FastAPI 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
