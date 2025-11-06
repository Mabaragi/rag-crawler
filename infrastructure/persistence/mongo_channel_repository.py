import os, dotenv
import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

from domain.repository.youtube_channel_repository import YoutubeChannelRepository

dotenv.load_dotenv()


class MongoChannelRepository(YoutubeChannelRepository):
    """
    MongoDB를 사용한 채널 저장소 구현체입니다.

    """

    def __init__(
        self,
        uri: str | None = None,
    ):
        self._client = MongoClient(uri or os.getenv("MONGO_URI"))
        self._db: Database = self._client["youtube_db"]
        self._collection: Collection = self._db["channels"]

    def save(self, channel, channel_id) -> None:
        try:
            self._collection.update_one(
                filter={"channel_id": channel_id},
                update={
                    "$set": {
                        "channel_name": channel.channel_name,
                        "channel_handle": channel.channel_handle,
                        "channel_id": channel_id,
                        "created_at": datetime.datetime.now(datetime.timezone.utc),
                    }
                },
                upsert=True,
            )
        except PyMongoError as e:
            print(f"Error saving channel to MongoDB: {e}")
