from abc import ABC, abstractmethod

from domain.model.youtube import YoutubeChannel, YoutubeVideoRawData


class YoutubeRepository(ABC):
    @abstractmethod
    def save_channel(self, channel: YoutubeChannel, channel_id: str, streamer_name: str) -> None:
        """채널 정보를 저장합니다.

        Args:
            channel (YoutubeChannel): 채널 정보
            channel_id (str): 채널 ID
            streamer_name (str): 스트리머 이름
        """
        pass

    @abstractmethod
    def bulk_save_raw_data(self, raw_data_list: list[YoutubeVideoRawData]) -> None:
        """원시 데이터를 일괄 저장합니다.

        Args:
            raw_data (list[YoutubeVideoRawData]): 원시 데이터
        """
        pass

    @abstractmethod
    def get_channel_by_id(self, channel_id: str) -> YoutubeChannel | None:
        """채널 ID로 채널 정보를 조회합니다.

        Args:
            channel_id (str): 채널 ID

        Returns:
            YoutubeChannel | None: 채널 정보 또는 None
        """
        pass

    @abstractmethod
    def update_channel(self, channel: YoutubeChannel) -> None:
        """채널 정보를 업데이트합니다.

        Args:
            channel (YoutubeChannel): 업데이트할 채널 정보
        """
        pass
