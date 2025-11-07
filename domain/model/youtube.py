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
        streamer_name: str = "",
        created_at: datetime.datetime | None = None,
        initialized: bool = False,
    ):
        self.channel_name = channel_name
        self.channel_handle = channel_handle
        self.channel_id = channel_id
        self.streamer_name = streamer_name
        self.initialized = initialized
        self.created_at = created_at

    @staticmethod
    def from_dict(data: dict) -> "YoutubeChannel":
        return YoutubeChannel(
            channel_name=data.get("channel_name", ""),
            channel_handle=data.get("channel_handle", ""),
            channel_id=data.get("channel_id", ""),
            streamer_name=data.get("streamer_name", ""),
            created_at=data.get("created_at"),
        )

    def update_initialized(self) -> None:
        self.initialized = True


class YoutubeVideoRawData:
    def __init__(
        self,
        video_id: str,
        channel_id: str,
        streamer_name: str,
        raw_data: dict,
        created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc),
    ):
        self.video_id = video_id
        self.channel_id = channel_id
        self.streamer_name = streamer_name
        self.raw_data = raw_data
        self.created_at = created_at

    @staticmethod
    def from_dict(data: dict) -> "YoutubeVideoRawData":
        return YoutubeVideoRawData(
            video_id=data["video_id"],
            channel_id=data["channel_id"],
            streamer_name=data["streamer_name"],
            raw_data=data["raw_data"],
            created_at=data["created_at"],
        )
