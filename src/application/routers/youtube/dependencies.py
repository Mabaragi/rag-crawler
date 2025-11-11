from application.services.youtube_service import (
    APIKeyService,
    ChannelCreateService,
    ChannelReadService,
    RawDataCrawlService,
)
from infrastructure.api.youtube_api_client import YoutubeAPIClient
from infrastructure.persistence.mongo_repository import (
    MongoAPIKeyRepository,
    MongoLogRepository,
    MongoYoutubeRepository,
)


def get_channel_read_service() -> ChannelReadService:
    youtube_repo = MongoYoutubeRepository()
    return ChannelReadService(youtube_repo)


def get_channel_create_service() -> ChannelCreateService:
    youtube_repo = MongoYoutubeRepository()
    api_key_repo = MongoAPIKeyRepository()
    youtube_client = YoutubeAPIClient()
    return ChannelCreateService(youtube_repo, api_key_repo, youtube_client)


def get_api_key_service() -> APIKeyService:
    api_key_repo = MongoAPIKeyRepository()
    return APIKeyService(api_key_repo)


def get_raw_data_crawl_service() -> RawDataCrawlService:
    youtube_repo = MongoYoutubeRepository()
    api_key_repo = MongoAPIKeyRepository()
    youtube_client = YoutubeAPIClient()
    log_repo = MongoLogRepository()
    return RawDataCrawlService(youtube_repo, api_key_repo, youtube_client, log_repo)
