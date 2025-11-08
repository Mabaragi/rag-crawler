from application.services.youtube_service import APIKeyService, ChannelInsertService
from infrastructure.api.youtube_api_client import YoutubeAPIClient
from infrastructure.persistence.mongo_repository import MongoAPIKeyRepository, MongoYoutubeRepository
from shared.config.settings import get_settings


def get_channel_insert_service() -> ChannelInsertService:
    settings = get_settings()
    mongo_repo = MongoYoutubeRepository()
    youtube_client = YoutubeAPIClient(api_key=settings.YOUTUBE_API_KEY)
    return ChannelInsertService(mongo_repo, youtube_client)


def get_api_key_service() -> APIKeyService:
    mongo_repo = MongoAPIKeyRepository()
    return APIKeyService(mongo_repo)
