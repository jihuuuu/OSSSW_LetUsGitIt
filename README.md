# 📰 뉴스 트렌드 클러스터링 서비스

최신 뉴스 기사를 **주제별로 클러스터링하고**, **키워드 시각화**, **스크랩 기반 개인화 추천** 기능을 제공하는 AI 기반 웹 서비스입니다.

> Semantic Clustering + Trend Visualization + User Scrap-based Note System

---

## ⚙️ 기술 스택

### 🖥️ Frontend
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)

### 🔧 Backend
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---
### 주요 기능
- 🔍 의미 기반 뉴스 클러스터링 (BERT + HDBSCAN)
- 🧠 트렌드 키워드 추출 및 시각화 (D3.js)
- 📚 스크랩과 노트 작성 기능
- 📝 스크랩한 기사 기반 지식맵 생성
- 
### 🚀 설치 및 실행

## 0. 클론

## 🔧 1. 백엔드 실행 (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
localhost:8000 에서 API 서버가 실행됩니다.

API 문서는 http://localhost:8000/docs (Swagger UI)에서 확인 가능합니다.

## 🎨 2. 프론트엔드 실행 (React)
cd frontend
npm install
npm run dev
localhost:5173 에서 웹 애플리케이션이 실행됩니다.

백엔드와 연동이 필요한 경우 .env 파일에서 API URL을 설정해주세요.

---
### ✍️  팀 소개
| 이름 | 역할 | 깃허브 |
|------|------|--------|
| 강성경 | 프론트엔드/디자인/배포/api명세 | [@sunggyeong](https://github.com/sunggyeong) |
| 남지후 | 백엔드/DB설계/ai | [@jihuuuu](https://github.com/jihuuuu) |
| 이채연 | 백엔드/DB설계/배포 | [@chaeyeonlee898](https://github.com/chaeyeonlee898) |
| 조윤경 |  ai/프론트/디자인/api명세 | [@yvngyeong](https://github.com/yvngyeong) |

### 🔐 라이선스

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)  
이 프로젝트는 **MIT 라이선스** 하에 배포됩니다. 자유롭게 사용, 수정, 배포가 가능합니다.

> 자세한 내용은 [`LICENSE`](./LICENSE) 파일을 참고해주세요.
>
> 

프로젝트 구조 설계 및 데이터베이스 연동 (MySQL), RSS 기사 크롤링 진행했습니다.

데이터베이스 연동 순서 및 RSS 기사 크롤링 결과 확인은 노션에 정리했습니다.

### 📁 디렉토리 구조

<details>
<summary> 프로젝트 구조 </summary>

```plaintext
project/
├─ api/                   # api 목록 (필요시 확장)
│   ├─ create_app.py      # FastAPI 앱 팩토리(환경 로드, 라우터 등록) 생성
│   ├─ routes/
│   │   ├─ news.py       
│   │   ├─ cluster.py
│   │   └─ user.py
│   └─ schemas/
│       ├─ news.py
│       └─ user.py
├─ collector/             # rss 기사 크롤링
│   ├─ rss_list.py
│   └─ rss_collector.py
├─ clustering/            # 기사 클러스터링 (AI)
│   ├─ embedder.py
│   ├─ cluster.py
│   └─ pipeline.py
├─ database/
│   ├─ connection.py
│   ├─ mongo_models.py    # 선택 (필요시 확장)
│   └─ sql_models.py
├─ frontend/              # React / Streamlit
├─ data/                  # 선택
│   └─ raw/               # 선택 (RSS로 받은 기사 JSON)
├─ app.py                 # FastAPI 실행 진입점
├─ .env
├─ db_init.py             # DB 초기 생성
├─ requirements.txt       # 패키지 설치 및 의존성 주입
└─ Dockerfile             # 선택 (필요시 확장)
</details>
```

