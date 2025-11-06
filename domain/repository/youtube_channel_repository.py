from abc import ABC, abstractmethod

from domain.model.youtube import YoutubeChannel


class YoutubeChannelRepository(ABC):
    @abstractmethod
    def save(
        self, channel: YoutubeChannel, channel_id: str, streamer_name: str
    ) -> None:
        """
        유튜브 채널 저장
        """
        pass

    # @abstractmethod
    # def get(self, video_id: str) -> YoutubeVideo:
    #     pass

    # @abstractmethod
    # def delete(self, video_id: str):
    #     pass
