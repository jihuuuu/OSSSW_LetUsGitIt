# 📰 뉴스 트렌드 클러스터링 서비스 - HOT ISSUE

최신 뉴스 기사를 **주제별로 클러스터링하고**, **트렌드 시각화**, **스크랩 기반 개인화 추천** 기능을 제공하는 AI 기반 웹 서비스입니다.

> Semantic Clustering + Trend Visualization + User Scrap-based Note System


## ⚙️ 기술 스택

### 🖥️ Frontend
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)

### 🔧 Backend
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-764ABC?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

### 🧠 AI/ML
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Transformers](https://img.shields.io/badge/Transformers-FFBF00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/docs/transformers/index)
[![HDBSCAN](https://img.shields.io/badge/HDBSCAN-005571?style=for-the-badge&logo=python&logoColor=white)](https://hdbscan.readthedocs.io/en/latest/)

### 🚀 Deployment / Infra
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)

---
## 주요 기능
- 🔍 의미 기반 뉴스 클러스터링 (SBERT + Kmeans)
- 🧠 이슈 키워드 추출 및 트렌드 시각화 (D3.js)
- 📚 스크랩과 노트 작성 기능
- 📝 스크랩한 기사 기반 지식맵 생성
  


---
## 🚀 설치 및 실행

### 🛠️ 0. 클론 및 MySQL 설정

#### 1. MySQL 데이터베이스 생성

- root 계정에서 생성해도 되지만, 별도의 사용자 계정을 생성한 뒤 사용하는 것을 권장합니다.

```sql
CREATE DATABASE news_app;
```

#### 2. 환경 변수 설정
프로젝트 루트에 .env 파일을 생성하고 다음 내용을 입력하세요:
```
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=news_app

REDIS_HOST=my-redis
REDIS_PORT=6379
REDIS_DB=0
```
⚠️ .env 파일에 주석이나 공백 줄이 포함되면 로딩이 실패할 수 있습니다.
반드시 KEY=VALUE 형식으로만 작성하세요.

#### 3. 테이블 Schema 자동 생성 (db_init.py)
아래 명령어를 터미널에 입력하면 DB에 필요한 테이블들이 생성됩니다:

```bash
python db_init.py
```

성공 시 출력 메시지:
테이블 생성 완료
MySQL에서도 다음 명령으로 테이블 생성 여부를 확인할 수 있습니다:

```sql
USE news_app;
SHOW TABLES;
```
테이블 구조는 database/sql_models.py에 정의되어 있습니다.

#### 4. Docker & Redis 컨테이너 준비
```
cd project
docker-compose up -d --build
```
d 옵션으로 백그라운드 실행이 가능합니다.
```
docker ps
```
를 통해 컨테이너의 준비 상태를 확인할 수 있습니다.

⚠️ Docker 에서 백엔드 서버와 Redis 서버를 제어합니다.


### 🎨 1. 프론트엔드 실행 (React)
```
cd frontend
npm install
npm run dev
```
`localhost:5173` 에서 웹 애플리케이션이 실행됩니다.

백엔드와 연동이 필요한 경우 .env 파일에서 API URL을 설정해주세요.

백엔드 API 문서는 http://localhost:8000/docs (SWAGGER UI) 에서 확인 가능합니다.

원하는 API 항목에서 Try it out -> Execute 클릭

---
## ✍️  팀 소개
| 이름 | 역할 | 깃허브 |
|------|------|--------|
| 강성경 | 프론트/디자인/API명세/배포 | [@sunggyeong](https://github.com/sunggyeong) |
| 남지후 | 백엔드/DB설계/AI/캐싱 | [@jihuuuu](https://github.com/jihuuuu) |
| 이채연 | 백엔드/DB설계/캐싱/배포 | [@chaeyeonlee898](https://github.com/chaeyeonlee898) |
| 조윤경 | 프론트/디자인/API명세/AI | [@yvngyeong](https://github.com/yvngyeong) |

---

## 🔐 라이선스

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)  
이 프로젝트는 **MIT 라이선스** 하에 배포됩니다. 자유롭게 사용, 수정, 배포가 가능합니다.

> 자세한 내용은 [`LICENSE`](./LICENSE) 파일을 참고해주세요.
>
> 

## ⚠️ 뉴스 데이터 및 크롤링 관련 안내

본 프로젝트는 오픈소스 학습용 소프트웨어이며, 실제 뉴스 기사 전문은 포함되어 있지 않습니다.  
크롤링 로직은 학습 및 기술적 데모 목적으로 제공되며, 다음 사항을 반드시 숙지해 주세요:

- 뉴스 데이터는 각 언론사 및 뉴스 제공처의 저작권 보호를 받을 수 있습니다.
- 실제 운영 시, 크롤링 대상 사이트의 `robots.txt` 및 서비스 약관을 반드시 준수해야 합니다.
- 프로젝트에 포함된 크롤링 코드를 상업적으로 사용하거나, 무단 기사 수집에 사용할 경우 책임은 사용자 본인에게 있습니다.
- 샘플 데이터는 테스트 및 시각화 목적이며, 민감한 정보는 포함되어 있지 않습니다.

👉 따라서 본 프로젝트는 **코드만 오픈소스로 제공되며**, 데이터셋은 사용자 환경에 맞춰 별도로 구성해야 합니다.

---

## 📁 디렉토리 구조

### 1. 루트 *(OSSSW_LetUsGitIt/)*

```
OSSSW_LetUsGitIt/
├─ README.md           # 프로젝트 설명서
├─ LICENSE             # 라이선스
├─ .gitignore          # 깃 무시 설정
├─ frontend
├─ project
└─ CONTRIBUTING.md     # 기여 가이드 (옵션)
```

### 2. `project/`  *(백엔드/AI/DB)*

```
project/
├─ api/               # FastAPI 앱, 라우터, 스키마
│  ├─ create_app.py
│  ├─ config.py
│  ├─ routes/
│  ├─ utils/
│  └─ schemas/
├─ collector/         # RSS 크롤러
│  ├─ rss_list.py
│  └─ rss_collector.py
├─ clustering/        # AI 클러스터링/임베딩
│  ├─ cache_redis.py
│  ├─ embedder.py
│  ├─ cluster.py
│  ├─ keyword_extractor.py
│  ├─ running_stage.py
│  └─ pipeline_by_topic.py
├─ database/          # DB 연결, ORM
│  ├─ connection.py
│  └─ deps.py
├─ data/              # 데이터, 원본기사 등
├─ dummy/             # 테스트용/샘플데이터/로직
├─ models/            # SQLAlchemy ORM 모델들
├─ tasks/             # 지식맵 파이프라인, 트렌드 파이프라인
├─ app.py             # FastAPI 앱 실행 진입점
├─ .env               # 환경 변수
├─ db_init.py         # DB 초기화
├─ requirements.txt   # 패키지 명세
├─ docker-compose.yml # 도커 컴포즈 설정   
└─ Dockerfile         # 컨테이너 빌드
```

---

### 3. `frontend/`  *(React/Vite/Tailwind)*

```
frontend/
├─ public/              # 정적 파일 (예: favicon, 이미지 등)
├─ src/                 # 프론트엔드 소스
│  ├─ App.tsx           # 루트 컴포넌트
│  ├─ main.tsx          # 진입점
│  ├─ index.css         # 전역 스타일
│  ├─ vite-env.d.ts     # Vite 환경 타입 정의
│  ├─ assets/           # 이미지, 폰트 등 정적 자산
│  ├─ components/       # 재사용 가능한 UI 컴포넌트
│  ├─ context/          # React context 모음
│  ├─ hooks/            # 커스텀 훅
│  ├─ lib/              # 라이브러리 및 유틸성 코드
│  ├─ pages/            # 페이지 단위 컴포넌트
│  ├─ routes/           # 라우팅 설정
│  ├─ services/         # API 통신 등 외부 서비스 연동
│  └─ types/            # 타입 정의 (TypeScript)
├─ package.json         # 패키지 설정
├─ ...                  # 기타 설정 파일
```

---

> 💡 **프로젝트의 메인 코드는 `project/`(백엔드), `frontend/`(프론트엔드)에 분리되어 있고,
> 공통 문서/설정은 루트(최상위)에 위치합니다.**

--- 

## 🏗️ 시스템 아키텍처

**Browser**, **Frontend**, **Backend**, **Redis**, **MySQL** 5개 컴포넌트 간의 주요 통신 흐름을 보여줍니다.

- **Browser ↔ Frontend (5173)**
  - React/Vite 개발 서버가 호스팅하는 UI
  - 사용자의 인터랙션을 받아 백엔드 API 호출

- **Frontend ↔ Backend (8000)**
  - FastAPI(Uvicorn) 기반 REST API
  - 클러스터링, 트렌드, 키워드 검색 등 주요 비즈니스 로직 제공

- **Backend ↔ Redis (6379)**
  - 임베딩 벡터, 지식맵, API 응답 캐싱
  - `redis.asyncio` + `fastapi-cache2` 비동기 캐시 레이어

- **Backend ↔ MySQL (3306)**
  - SQLAlchemy ORM을 통한 데이터 읽기/쓰기
  - 사용자, 기사, 클러스터, 키워드, 트렌드 등 영속화

---
## 📈 향후 개선 사항
- 클러스터링 성능 향상
- UI 사용성 편의성 향상  
- 사용자별 뉴스 피드 추천
- GPT를 활용한 요약 기능 (노트 내용 자동 요약 후 수정 가능하게)
- 다국어 뉴스 지원

---
## 🤝 기여 방법
기여를 원하시나요? 👉 [CONTRIBUTING.md](./CONTRIBUTING.md)를 확인해주세요!

1. 이 프로젝트에 관심 가져주셔서 감사합니다! 🙌  
2. 이슈를 제기하거나 새로운 기능을 제안하고 싶다면 [Issues](https://github.com/jihuuuu/OSSSW_LetUsGitIt/issues) 탭을 이용해주세요.
3. Pull Request(PR)는 `feat/`, `fix/`, `docs/` 등 [Git 커밋 컨벤션](https://www.conventionalcommits.org/ko/v1.0.0/)을 따릅니다.
4. 코드 변경 전 반드시 아래 과정을 따라주세요:

```bash
# 저장소 포크 및 클론
git clone https://github.com/jihuuuu/OSSSW_LetUsGitIt.git
cd yourrepo

# 브랜치 생성
git checkout -b feat/my-feature

# 작업 후 커밋 및 푸시
git commit -m "feat: add my feature"
git push origin feat/my-feature
```
