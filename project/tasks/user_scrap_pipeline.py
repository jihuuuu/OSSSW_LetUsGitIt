# tasks/user_scrap_pipeline.py
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.user import KnowledgeMap, User
from models.scrap import PKeyword, PKeywordArticle
from clustering.embedder import make_embeddings
from clustering.keyword_extractor import get_top_keywords
from sklearn.metrics.pairwise import cosine_similarity
from redis import Redis
import json

def build_knowledge_map(user_id: int):
    db: Session = SessionLocal()

    try:
        print(f"🧠 Task called with user_id={user_id}")
        # 1. 유저의 모든 PKeyword 가져오기
        print("📍 Step 1: 유저 PKeyword 조회 시작")
        pkeywords = db.query(PKeyword).filter_by(user_id=user_id).all()
        if not pkeywords:
            return "NO_PKEYWORDS"

        # 2. 연결 정보 설정
        print("📍 Step 2: connections 설정")
        for pk in pkeywords:
            pk.connections = db.query(PKeywordArticle).filter_by(pkeyword_id=pk.id).all()

        # 3. 상위 20개 키워드 선정
        print("📍 Step 3: top_keywords 계산")
        top_keywords = get_top_keywords(pkeywords, alpha=0.75, limit=20)
        if not top_keywords:
            print("⚠️ top_keywords가 비어 있어 knowledge_map을 생성하지 않습니다.")
            return "NO_TOP_KEYWORDS"
        print(f"📍 top_keywords 개수: {len(top_keywords)}")

        # 4. KnowledgeMap 생성 및 연결
        print("📍 Step 4: KnowledgeMap 생성")
        knowledge_map = KnowledgeMap(user_id=user_id, is_valid=True)
        db.add(knowledge_map)
        db.flush()  # knowledge_map.id 확보
        created_at = knowledge_map.created_at

        for pk in top_keywords:
            pk.knowledge_map_id = knowledge_map.id

        # 5. 임베딩 및 유사도 계산
        print("📍 Step 5: 임베딩 및 유사도 계산")
        keyword_texts = [kw.name for kw in top_keywords]
        embeddings = make_embeddings(keyword_texts)
        sim_matrix = cosine_similarity(embeddings)

        # 6. 간선 생성 (dict로)
        print("📍 Step 6: 간선 생성")
        edges = []
        threshold = 0.60
        top_k = 3
        for i in range(len(top_keywords)):
            similarities = [(j, sim_matrix[i][j]) for j in range(len(top_keywords)) if i != j]
            top_similar = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
            for j, sim in top_similar:
                if sim >= threshold:
                    edges.append({
                        "source": top_keywords[i].id,
                        "target": top_keywords[j].id,
                        "weight": round(float(sim), 4)
                    })

        # 7. 노드 생성 (dict로)
        print("📍 Step 7: 노드 생성")
        nodes = [
            {"id": kw.id, "name": kw.name, "count": kw.count}
            for kw in top_keywords
        ]

        # ✅ 디버깅 출력
        print("\n🧠 [지식맵 노드 목록]")
        for node in nodes:
            print(f" - {node['name']} (count: {node['count']})")

        print("\n🔗 [지식맵 간선 목록]")
        for edge in edges:
            print(f" - {edge['source']} -> {edge['target']} (weight: {edge['weight']})")

        # 8. Redis에 캐싱
        redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
        cache_key = f"user:{user_id}:knowledge_map"
        cache_value = {"id": knowledge_map.id,
                       "created_at": created_at.isoformat(),  # datetime은 문자열로
                       "nodes": nodes,
                       "edges": edges}
        redis_client.set(cache_key, json.dumps(cache_value, ensure_ascii=False))  # 문자열로 저장
        
        db.commit()
        return "SUCCESS"

    except Exception as e:
        print(f"\n🔥 Knowledge Map Task 실패: {e.__class__.__name__} - {e}")
        import traceback
        traceback.print_exc()
        return "ERROR"
        
    finally:
        db.close()
