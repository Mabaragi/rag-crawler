import datetime

# from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError

from audit.loggers.log_repository import LogRepository
from audit.loggers.youtube_logger import YoutubeLogEntry
from domain.model.youtube import APIKey, YoutubeChannel, YoutubeVideoRawData
from domain.repository.youtube_repository import APIKeyRepository, YoutubeRepository
from infrastructure.persistence.client import get_mongo_db


class MongoYoutubeRepository(YoutubeRepository):
    """
    MongoDB를 사용한 유튜브 저장소 구현체입니다.

    """

    def __init__(self, db_name: str = "youtube_db"):
        # 환경 변수나 기본값으로 클라이언트 초기화
        # 데이터베이스는 생성자에서 전달받은 이름으로 설정
        self._db = get_mongo_db(db_name)

    async def _get_channels(self, filter: dict | None = None) -> list[YoutubeChannel]:
        try:
            if filter is None:
                filter = {}
            cursor = self._db["channels"].find(filter)
            channels = []
            async for document in cursor:
                channels.append(YoutubeChannel.from_dict(document))
            return channels
        except PyMongoError as e:
            raise e

    async def get_channels(self) -> list[YoutubeChannel]:
        return await self._get_channels()

    async def get_initialized_channels(self) -> list[YoutubeChannel]:
        return await self._get_channels(filter={"initialized": True})

    async def get_uninitialized_channels(self) -> list[YoutubeChannel]:
        return await self._get_channels(filter={"initialized": False})

    async def get_video_by_id(self, video_id: str) -> YoutubeVideoRawData | None:
        try:
            data = await self._db["raw_data"].find_one(filter={"video_id": video_id})
            if data:
                return YoutubeVideoRawData.from_dict(data)
            return None
        except PyMongoError as e:
            raise e

    async def save_channel(self, channel: YoutubeChannel) -> None:
        try:
            youtube_channel_data = channel.to_dict()
            youtube_channel_data["created_at"] = datetime.datetime.now(datetime.timezone.utc)

            await self._db["channels"].update_one(
                filter={"channel_id": channel.channel_id},
                update={"$set": youtube_channel_data},
                upsert=True,
            )
        except PyMongoError as e:
            raise e

    async def update_channel(self, channel: YoutubeChannel) -> None:
        try:
            await self._db["channels"].update_one(
                filter={"channel_id": channel.channel_id},
                update={
                    "$set": {
                        "channel_name": channel.channel_name,
                        "channel_handle": channel.channel_handle,
                        "streamer_name": channel.streamer_name,
                        "initialized": channel.initialized,
                    }
                },
            )
        except PyMongoError as e:
            print(f"Error updating channel in MongoDB: {e}")

    async def get_channel_by_id(self, channel_id: str) -> YoutubeChannel | None:
        try:
            data = await self._db["channels"].find_one(filter={"channel_id": channel_id})
            if data:
                return YoutubeChannel.from_dict(data)
            return None
        except PyMongoError as e:
            raise e

    async def bulk_save_raw_data(self, raw_data_list: list[YoutubeVideoRawData]) -> None:
        try:
            await self._db["raw_data"].insert_many([data.__dict__ for data in raw_data_list])
        except PyMongoError as e:
            raise e

    async def clear_raw_data_for_channel(self, channel: YoutubeChannel) -> None:
        try:
            await self._db["raw_data"].delete_many({"channel_id": channel.channel_id})
        except PyMongoError as e:
            raise e

    async def check_saved(self, raw_data: YoutubeVideoRawData) -> bool | None:
        """
        원시 데이터의 저장 여부를 확인합니다.
        """
        video_id = raw_data.video_id
        try:
            existing = await self._db["raw_data"].find_one({"video_id": video_id})
            return existing is not None
        except PyMongoError as e:
            raise e


class MongoAPIKeyRepository(APIKeyRepository):
    def __init__(self, db_name: str = "youtube_db"):
        self._db = get_mongo_db(db_name)

    async def list_api_keys(self) -> list[APIKey]:
        try:
            cursor = self._db["api_keys"].find({})
            api_keys = []
            async for document in cursor:
                api_keys.append(APIKey.from_dict(document))
            return api_keys
        except PyMongoError as e:
            raise e

    async def get_api_key(self) -> APIKey:
        try:
            data = await self._db["api_keys"].find_one(filter={"service": "youtube"})
            if data:
                return APIKey.from_dict(data)
            else:
                raise ValueError("No API key found for YouTube service")
        except PyMongoError as e:
            raise e

    async def insert_api_key(self, api_key: APIKey) -> None:
        try:
            await self._db["api_keys"].update_one(
                filter={"service": "youtube"},
                update={"$set": api_key.to_dict()},
                upsert=True,
            )
        except PyMongoError as e:
            raise e

    async def update_api_key(self, api_key: APIKey) -> None:
        try:
            api_key_data = api_key.to_dict()
            api_key_data["updated_at"] = datetime.datetime.now(datetime.timezone.utc)
            await self._db["api_keys"].update_one(
                filter={"service": "youtube"},
                update={"$set": api_key_data},
            )
        except PyMongoError as e:
            raise e


class MongoLogRepository(LogRepository):
    def __init__(self, db_name: str = "log_db"):
        self._db = get_mongo_db(db_name)

    async def _save_log(self, log: YoutubeLogEntry, collection_name: str) -> None:
        try:
            await self._db[collection_name].insert_one(log.to_dict())
        except PyMongoError as e:
            raise e

    async def save_channel_log(self, log: YoutubeLogEntry) -> None:
        await self._save_log(log, "channel_crawl_logs")

    async def save_video_raw_data_log(self, log: YoutubeLogEntry) -> None:
        await self._save_log(log, "video_raw_data_logs")
