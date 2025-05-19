# models/__init__.py
# 역할: SQLAlchemy ORM 모델을 정의하고, 데이터베이스와의 상호작용을 위한 세션을 관리
# 모든 모델 import 해서 Base metadata 구성

from .user import User, KnowledgeMap
from .article import Article, Cluster, ClusterKeyword
from .note import Note, NoteArticle
from .scrap import Scrap
from .base import Base