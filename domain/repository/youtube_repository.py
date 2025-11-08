from abc import ABC, abstractmethod

from domain.model.youtube import APIKey, YoutubeChannel, YoutubeVideoRawData


class YoutubeRepository(ABC):
    @abstractmethod
    async def save_channel(self, channel: YoutubeChannel) -> None:
        """채널 정보를 저장합니다.

        Args:
            channel (YoutubeChannel): 채널 정보
            channel_id (str): 채널 ID
            streamer_name (str): 스트리머 이름
        """
        pass

    @abstractmethod
    async def bulk_save_raw_data(self, raw_data_list: list[YoutubeVideoRawData]) -> None:
        """원시 데이터를 일괄 저장합니다.

        Args:
            raw_data (list[YoutubeVideoRawData]): 원시 데이터
        """
        pass

    @abstractmethod
    async def get_channel_by_id(self, channel_id: str) -> YoutubeChannel | None:
        """채널 ID로 채널 정보를 조회합니다.

        Args:
            channel_id (str): 채널 ID

        Returns:
            YoutubeChannel | None: 채널 정보 또는 None
        """
        pass

    @abstractmethod
    async def update_channel(self, channel: YoutubeChannel) -> None:
        """채널 정보를 업데이트합니다.

        Args:
            channel (YoutubeChannel): 업데이트할 채널 정보
        """
        pass


class APIKeyRepository(ABC):
    @abstractmethod
    async def list_api_keys(self) -> list[APIKey]:
        """저장된 모든 API 키를 조회합니다.

        Returns:
            list[APIKey]: 저장된 API
        """
        pass

    @abstractmethod
    async def get_api_key(self) -> APIKey | None:
        """API 키를 조회합니다.

        Returns:
            APIKey | None: API 키 정보 또는 None
        """
        pass

    @abstractmethod
    async def insert_api_key(self, api_key: APIKey) -> None:
        """API 키를 저장합니다.

        Args:
            api_key (APIKey): 저장할 API 키 객체
        """
        pass

    @abstractmethod
    async def update_api_key(self, api_key: APIKey) -> None:
        """API 키를 업데이트합니다.

        Args:
            api_key (APIKey): 업데이트할 API 키 객체
        """
        pass
