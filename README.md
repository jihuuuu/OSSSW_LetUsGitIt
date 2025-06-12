# 📰 뉴스 트렌드 클러스터링 서비스

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

프로젝트 구조 설계 및 데이터베이스 연동 (MySQL), RSS 기사 크롤링 진행했습니다.

데이터베이스 연동 순서 및 RSS 기사 크롤링 결과 확인은 노션에 정리했습니다.

프로젝트 구조는 다음과 같습니다.

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

