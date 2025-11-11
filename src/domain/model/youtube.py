import datetime
import os
from dataclasses import dataclass, field
from typing import Any

import dotenv

from shared.utils import data_class_from_dict

dotenv.load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


@dataclass
class YoutubeChannel:
    channel_name: str
    channel_handle: str
    channel_id: str
    streamer_name: str
    initialized: bool = field(default=False)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    @staticmethod
    def from_dict(data: dict) -> "YoutubeChannel":
        return data_class_from_dict(YoutubeChannel, data)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    def update_initialized(self) -> None:
        self.initialized = True


@dataclass
class YoutubeVideoRawData:
    video_id: str
    channel_id: str
    streamer_name: str
    raw_data: dict
    created_at: datetime.datetime

    @staticmethod
    def from_dict(data: dict) -> "YoutubeVideoRawData":
        return data_class_from_dict(YoutubeVideoRawData, data)


@dataclass
class APIKey:
    api_key: str
    service: str = field(default="youtube")
    quota_used: int = 0
    updated_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    def is_search_quota_available(self) -> bool:
        """검색 쿼터를 사용 가능한지 확인합니다.

        Returns:
            bool: 검색 쿼터 사용 가능 여부
        """
        if self.quota_used <= 8000:
            return True
        return False

    def is_channel_quota_available(self) -> bool:
        """채널 쿼터를 사용 가능한지 확인합니다.

        Returns:
            bool: 채널 쿼터 사용 가능 여부
        """
        if self.quota_used <= 9900:
            return True
        return False

    def use_search_quota(self, amount: int = 100) -> None:
        """검색 쿼터를 사용합니다.

        Args:
            amount (int, optional): 사용할 쿼터 양. Defaults to 100.
        """
        self.quota_used += amount
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    def use_channel_quota(self, amount: int = 1) -> None:
        """채널 쿼터를 사용합니다.

        Args:
            amount (int, optional): 사용할 쿼터 양. Defaults to 1.
        """
        self.quota_used += amount
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_dict(data: dict) -> "APIKey":
        return data_class_from_dict(APIKey, data)
