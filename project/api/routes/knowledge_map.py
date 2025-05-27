# api/routes/knowledge_map.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User, KnowledgeMap
from models.note import Note, NoteArticle
from models.scrap import PCluster, PClusterKeyword, PClusterArticle
from models.article import Article
from api.utils.auth import get_current_user
from database.deps import get_db
from api.schemas.knowledge_map import KnowledgeMapCreateRequest

router = APIRouter()

@router.post("/knowledge-maps")
def create_knowledge_maps(
    request_data: KnowledgeMapCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    created_map_ids = []

    for cluster in request_data.result:
        # 1. KnowledgeMap 생성
        knowledge_map = KnowledgeMap(user_id=current_user.id)
        db.add(knowledge_map)
        db.commit()
        db.refresh(knowledge_map)
        created_map_ids.append(knowledge_map.id)

        # 2. PCluster 생성 (label 단위로)
        pcluster = PCluster(
            label=cluster.label,
            knowledge_map_id=knowledge_map.id
        )
        db.add(pcluster)
        db.commit()
        db.refresh(pcluster)

        # 3. 키워드 등록
        for keyword in cluster.keywords:
            db.add(PClusterKeyword(keyword=keyword, pcluster_id=pcluster.id))

        # 4. 기사 연결
        for article_id in cluster.articleIds:
            article = db.query(Article).filter(Article.id == article_id).first()
            if not article:
                raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
            db.add(PClusterArticle(article_id=article_id, pcluster_id=pcluster.id))

        db.commit()

    return {
        "isSuccess": True,
        "code": "KNOWLEDGE_MAPS_CREATED",
        "message": "지식맵이 성공적으로 생성되었습니다.",
        "result": {
            "knowledgeMapIds": created_map_ids
        }
    }


@router.get("/knowledge_maps/graph")
def get_latest_knowledge_map(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. 가장 최근 지식맵 하나 가져오기
    latest_map = (
        db.query(KnowledgeMap)
        .filter(KnowledgeMap.user_id == current_user.id)
        .order_by(KnowledgeMap.created_at.desc())
        .first()
    )

    if not latest_map:
        raise HTTPException(status_code=404, detail="지식맵이 존재하지 않습니다.")

    nodes = []
    edges = []

    # 2. 지식맵에 속한 클러스터들 가져오기
    clusters = db.query(PCluster).filter(PCluster.knowledge_map_id == latest_map.id).all()

    for cluster in clusters:
        cluster_id = f"cl-{cluster.id}"
        nodes.append({"id": cluster_id, "label": cluster.label, "type": "cluster"})

        # 2-1. 키워드 노드 + 엣지
        keywords = db.query(PClusterKeyword).filter(PClusterKeyword.pcluster_id == cluster.id).all()
        for kw in keywords:
            keyword_id = f"kw-{kw.keyword}"
            nodes.append({"id": keyword_id, "label": kw.keyword, "type": "keyword"})
            edges.append({"source": cluster_id, "target": keyword_id})

        # 2-2. 기사 노드 + 엣지
        article_links = db.query(PClusterArticle).filter(PClusterArticle.pcluster_id == cluster.id).all()
        article_ids = [a.article_id for a in article_links]
        articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

        for article in articles:
            article_id = f"ar-{article.id}"
            nodes.append({"id": article_id, "label": article.title, "type": "article"})
            edges.append({"source": cluster_id, "target": article_id})

    return {
        "isSuccess": True,
        "code": "LATEST_KNOWLEDGE_MAP",
        "message": "최신 지식맵을 불러왔습니다.",
        "result": {
            "nodes": nodes,
            "edges": edges
        }
    }

@router.get("/keywords/{keyword_id}/clusters/notes")
def get_notes_by_keyword(
    keyword_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size

    # 1. keyword_id로 클러스터 id 찾기
    cluster_ids = (
        db.query(PClusterKeyword.pcluster_id)
        .filter(PClusterKeyword.keyword == keyword_id)
        .distinct()
        .all()
    )
    cluster_ids = [cid for (cid,) in cluster_ids]

    if not cluster_ids:
        raise HTTPException(status_code=404, detail="해당 키워드를 가진 클러스터가 없습니다.")

    # 2. 해당 클러스터들이 연결한 기사 ID 수집
    article_ids = (
        db.query(PClusterArticle.article_id)
        .filter(PClusterArticle.pcluster_id.in_(cluster_ids))
        .distinct()
        .all()
    )
    article_ids = [aid for (aid,) in article_ids]

    if not article_ids:
        return {
            "page": page,
            "size": size,
            "keyword": keyword_id,
            "notes": []
        }

    # 3. 해당 기사들과 연결된 노트 ID 수집
    note_ids = (
        db.query(NoteArticle.note_id)
        .filter(NoteArticle.article_id.in_(article_ids))
        .distinct()
        .all()
    )
    note_ids = [nid for (nid,) in note_ids]

    if not note_ids:
        return {
            "page": page,
            "size": size,
            "keyword": keyword_id,
            "notes": []
        }

    # 4. 노트 정보 + 연결된 기사 ID 함께 조회
    notes = (
        db.query(Note)
        .filter(Note.id.in_(note_ids), Note.state == True)
        .order_by(Note.created_at.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    result_notes = []
    for note in notes:
        related_articles = db.query(NoteArticle.article_id).filter(NoteArticle.note_id == note.id).all()
        related_article_ids = [aid for (aid,) in related_articles]

        result_notes.append({
            "note_id": note.id,
            "title": note.title,
            "text": note.text,
            "related_article_ids": related_article_ids,
            "created_at": note.created_at
        })

    return {
        "page": page,
        "size": size,
        "keyword": keyword_id,
        "notes": result_notes
    }


@router.get("/keywords/{keyword}/clusters/articles")
def get_clusters_by_keyword(
    keyword: str,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size

    # 1. 해당 키워드를 가진 클러스터 id들 조회
    cluster_ids = (
        db.query(PClusterKeyword.pcluster_id)
        .filter(PClusterKeyword.keyword == keyword)
        .distinct()
        .all()
    )
    cluster_ids = [cid for (cid,) in cluster_ids]

    if not cluster_ids:
        return {
            "page": page,
            "size": size,
            "keyword": keyword,
            "clusters": []
        }

    # 2. 페이징된 클러스터 조회
    clusters = (
        db.query(PCluster)
        .filter(PCluster.id.in_(cluster_ids))
        .order_by(PCluster.id.desc())
        .offset(offset)
        .limit(size)
        .all()
    )

    # 3. 각 클러스터마다 연결된 기사들 조회
    result_clusters = []
    for cluster in clusters:
        article_ids = (
            db.query(PClusterArticle.article_id)
            .filter(PClusterArticle.pcluster_id == cluster.id)
            .distinct()
            .all()
        )
        article_ids = [aid for (aid,) in article_ids]

        articles = db.query(Article).filter(Article.id.in_(article_ids)).all()

        result_clusters.append({
            "cluster_id": cluster.id,
            "label": cluster.label,
            "articles": [
                {"id": a.id, "title": a.title, "link": a.link}
                for a in articles
            ]
        })

    return {
        "page": page,
        "size": size,
        "keyword": keyword,
        "clusters": result_clusters
    }