import datetime
import os

import dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from domain.model.youtube import YoutubeChannel
from domain.repository.youtube_channel_repository import YoutubeChannelRepository

dotenv.load_dotenv()


class MongoBaseRepository:
    """MongoDB 클라이언트 연결 및 기본 데이터베이스 설정을 관리하는 기반 클래스."""

    def __init__(self, db_name: str = "youtube_db"):
        # 환경 변수나 기본값으로 클라이언트 초기화
        self._client: MongoClient = MongoClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017")
        )
        # 데이터베이스는 생성자에서 전달받은 이름으로 설정
        self._db: Database = self._client[db_name]

    def get_db(self) -> Database:
        """MongoDB 데이터베이스 인스턴스를 반환합니다."""
        return self._db


class MongoChannelRepository(MongoBaseRepository, YoutubeChannelRepository):
    """
    MongoDB를 사용한 채널 저장소 구현체입니다.

    """

    def __init__(
        self,
        db_name: str = "youtube_db",
    ):
        super().__init__(db_name=db_name)
        self._collection: Collection = self.get_db()["channels"]

    def save(
        self, channel: YoutubeChannel, channel_id: str, streamer_name: str
    ) -> None:
        try:
            self._collection.update_one(
                filter={"channel_id": channel_id},
                update={
                    "$set": {
                        "channel_name": channel.channel_name,
                        "channel_handle": channel.channel_handle,
                        "channel_id": channel_id,
                        "streamer_name": streamer_name,
                        "created_at": datetime.datetime.now(datetime.timezone.utc),
                    }
                },
                upsert=True,
            )
        except PyMongoError as e:
            print(f"Error saving channel to MongoDB: {e}")


class MongoRawDataRepository(MongoBaseRepository):
    """
    MongoDB를 사용한 유튜브 원시 데이터 저장소 구현체입니다.
    """

    def __init__(
        self,
        db_name: str = "youtube_db",
    ):
        super().__init__(db_name=db_name)
        self._collection: Collection = self.get_db()["raw_data"]

    def bulk_save_raw_data(self, raw_data_list: list[dict]) -> None:
        try:
            self._collection.insert_many(raw_data_list)
        except PyMongoError as e:
            print(f"Error saving raw data to MongoDB: {e}")

    def check_saved(self, raw_data_list: list[dict]) -> bool | None:
        """
        원시 데이터 리스트의 첫번째 요소로 저장 여부를 확인합니다.
        """
        video_id = raw_data_list[0].get("video_id")
        try:
            existing = self._collection.find_one({"video_id": video_id})
            return existing is not None
        except PyMongoError as e:
            print(f"Error checking raw data in MongoDB: {e}")
            return None
