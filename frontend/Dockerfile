# 1단계: 빌드 단계
FROM node:18 as build

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 lock 파일 복사
COPY package*.json ./

# 의존성 설치
RUN npm install

# 전체 소스 복사
COPY . .

# React 앱 빌드 (Vite든 CRA든 빌드 결과물이 나옴)
RUN npm run build

# ----------------------------------------------------

# 2단계: 정적 파일 서빙용 Nginx
FROM nginx:stable-alpine

# 빌드된 파일을 Nginx HTML 디렉토리로 복사
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx 설정 파일 덮어쓰기 (원하면 따로 커스터마이징 가능)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
