# 📰 뉴스 트렌드 클러스터링 서비스 - HOT ISUUE

최신 뉴스 기사를 **주제별로 클러스터링하고**, **키워드 시각화**, **스크랩 기반 개인화 추천** 기능을 제공하는 AI 기반 웹 서비스입니다.

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
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---
## 주요 기능
- 🔍 의미 기반 뉴스 클러스터링 (BERT + HDBSCAN)
- 🧠 트렌드 키워드 추출 및 시각화 (D3.js)
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
MYSQL_USER=root
MYSQL_PASSWORD=1569
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=news_app
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

### 🔧 1. 백엔드 실행 (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
${import.meta.env.VITE_API_URL}:8000 에서 API 서버가 실행됩니다.

API 문서는 http://${import.meta.env.VITE_API_URL}:8000/docs (Swagger UI)에서 확인 가능합니다.
원하는 API 항목에서 Try it out → Execute 클릭

### 🎨 2. 프론트엔드 실행 (React)
cd frontend
npm install
npm run dev
${import.meta.env.VITE_API_URL}:5173 에서 웹 애플리케이션이 실행됩니다.

백엔드와 연동이 필요한 경우 .env 파일에서 API URL을 설정해주세요.

---
## ✍️  팀 소개
| 이름 | 역할 | 깃허브 |
|------|------|--------|
| 강성경 | 프론트엔드/디자인/배포/api명세 | [@sunggyeong](https://github.com/sunggyeong) |
| 남지후 | 백엔드/DB설계/ai | [@jihuuuu](https://github.com/jihuuuu) |
| 이채연 | 백엔드/DB설계/배포 | [@chaeyeonlee898](https://github.com/chaeyeonlee898) |
| 조윤경 |  ai/프론트/디자인/api명세 | [@yvngyeong](https://github.com/yvngyeong) |

## 🔐 라이선스

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)  
이 프로젝트는 **MIT 라이선스** 하에 배포됩니다. 자유롭게 사용, 수정, 배포가 가능합니다.

> 자세한 내용은 [`LICENSE`](./LICENSE) 파일을 참고해주세요.
>
> 

---

## 📁 디렉토리 구조

<details>
<summary> 프로젝트 구조 </summary>

<pre>
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
</pre>
<br>

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
