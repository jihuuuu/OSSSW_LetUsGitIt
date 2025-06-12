# 🤝 Contributing Guide

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


## 🧑‍💻 개발 환경 설정
자세한 사항은 [README.md](./README.md)를 따라주세요!

```bash
git clone https://github.com/yourname/yourrepo.git
cd yourrepo

# 백엔드 설치
cd backend
pip install -r requirements.txt

# 프론트엔드 설치
cd ../frontend
npm install

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

## 💡 주요 기능

- 🔍 의미 기반 뉴스 클러스터링 (BERT + HDBSCAN)
- 🧠 트렌드 키워드 추출 및 시각화 (D3.js)
- 📚 스크랩과 노트 작성 기능
- 📝 스크랩한 기사 기반 지식맵 생성

---

## 🚀 설치 및 실행

### 🛠️ 0. 클론 및 MySQL 설정

#### 1. MySQL 데이터베이스 생성

```sql
CREATE DATABASE news_app;
root 계정에서 생성해도 되지만, 별도의 사용자 계정을 생성한 뒤 사용하는 것을 권장합니다.

2. 환경 변수 설정 (.env)
프로젝트 루트에 .env 파일을 생성하고 다음 내용을 입력하세요:

env
복사
편집
MYSQL_USER=root
MYSQL_PASSWORD=1569
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=news_app
⚠️ .env 파일에 주석이나 공백 줄이 포함되면 로딩이 실패할 수 있습니다. 반드시 KEY=VALUE 형식으로만 작성하세요.

3. 테이블 Schema 자동 생성 (db_init.py)
bash
복사
편집
python db_init.py
성공 시 출력 메시지:

복사
편집
테이블 생성 완료
MySQL에서 아래 명령으로 테이블 생성 여부를 확인할 수 있습니다:

sql
복사
편집
USE news_app;
SHOW TABLES;
테이블 구조는 database/sql_models.py에 정의되어 있습니다.

🔧 1. 백엔드 실행 (FastAPI)
bash
복사
편집
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
서버 주소: http://localhost:8000

Swagger UI: http://localhost:8000/docs

Swagger UI에서 Try it out → Execute로 API 테스트 가능

🎨 2. 프론트엔드 실행 (React)
bash
복사
편집
cd frontend
npm install
npm run dev
실행 주소: http://localhost:5173

.env에서 백엔드 API 주소를 설정해야 할 수 있습니다.