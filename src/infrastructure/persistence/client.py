# infrastructure/persistence/db_client.py (예시)
from pymongo import AsyncMongoClient

from shared.config.settings import get_settings

# 모듈이 임포트될 때 한 번만 클라이언트 생성
MONGO_CLIENT = AsyncMongoClient(get_settings().MONGO_URI)


def get_mongo_db(db_name: str):
    return MONGO_CLIENT[db_name]
