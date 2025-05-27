# dummy/seed_dummy_data.py

from sqlalchemy.orm import Session
from datetime import datetime
from faker import Faker
from passlib.hash import bcrypt

from models.user import User, KnowledgeMap
from models.note import Note, NoteArticle
from models.article import Article
from models.scrap import Scrap
from database.connection import engine, SessionLocal  # ✅ 기존 설정 가져오기
from models.base import Base

# DB 테이블 생성 (없으면)
Base.metadata.create_all(bind=engine)

# 세션 시작
db: Session = SessionLocal()
fake = Faker("ko_KR")

# ──────────────────────────────
# 1. 유저 생성
user = User(
    user_name="테스터",
    email = fake.unique.email(),
    password=bcrypt.hash("test12345")
)
db.add(user)
db.commit()
db.refresh(user)

# 2. 기사 생성
articles = []
for _ in range(100):
    a = Article(
        title=fake.sentence(),
        link=fake.url(),
        summary=fake.text(),
        published=datetime.now()  # 👈 중요

    )
    db.add(a)
    articles.append(a)
db.commit()

# 3. 노트 + 연결
note = Note(
    user_id=user.id,
    title="AI 뉴스 요약",
    text="오늘의 뉴스 핵심 요약입니다.",
    state=True,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
db.add(note)
db.commit()
db.refresh(note)

for article in articles[:3]:
    db.add(NoteArticle(note_id=note.id, article_id=article.id))
db.commit()

# 4. KnowledgeMap 생성
km = KnowledgeMap(user_id=user.id)
db.add(km)
db.commit()

# 5. Scrap 연결
for article in articles:
    db.add(Scrap(user_id=user.id, article_id=article.id, created_at=datetime.utcnow()))
db.commit()

print("✅ 더미 데이터 삽입 완료")

