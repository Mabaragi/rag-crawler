import datetime
import os

import dotenv

dotenv.load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YoutubeChannel:
    def __init__(
        self,
        channel_name: str,
        channel_handle: str,
        channel_id: str,
        streamer_name: str,
        created_at: datetime.datetime | None = None,
        initialized: bool = False,
    ):
        self.channel_name = channel_name
        self.channel_handle = channel_handle
        self.channel_id = channel_id
        self.streamer_name = streamer_name
        self.initialized = initialized
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def from_dict(data: dict) -> "YoutubeChannel":
        return YoutubeChannel(
            channel_name=data["channel_name"],
            channel_handle=data["channel_handle"],
            channel_id=data["channel_id"],
            streamer_name=data["streamer_name"],
            created_at=data["created_at"],
        )

    def to_dict(self) -> dict:
        return {
            "channel_name": self.channel_name,
            "channel_handle": self.channel_handle,
            "channel_id": self.channel_id,
            "streamer_name": self.streamer_name,
            "initialized": self.initialized,
            "created_at": self.created_at,
        }

    def update_initialized(self) -> None:
        self.initialized = True


class YoutubeVideoRawData:
    def __init__(
        self,
        video_id: str,
        channel_id: str,
        streamer_name: str,
        raw_data: dict,
        created_at: datetime.datetime | None = None,
    ):
        self.video_id = video_id
        self.channel_id = channel_id
        self.streamer_name = streamer_name
        self.raw_data = raw_data
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def from_dict(data: dict) -> "YoutubeVideoRawData":
        return YoutubeVideoRawData(
            video_id=data["video_id"],
            channel_id=data["channel_id"],
            streamer_name=data["streamer_name"],
            raw_data=data["raw_data"],
            created_at=data["created_at"],
        )


class APIKey:
    def __init__(
        self,
        key: str,
        quota_used: int = 0,
        updated_at: datetime.datetime | None = None,
        created_at: datetime.datetime | None = None,
    ):
        self.service = "youtube"
        self.key = key
        self.quota_used = quota_used
        self.updated_at = updated_at or datetime.datetime.now(datetime.timezone.utc)
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self) -> dict:
        return {
            "service": self.service,
            "api_key": self.key,
            "quota_used": self.quota_used,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "APIKey":
        return APIKey(
            key=data["api_key"],
            quota_used=data["quota_used"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
