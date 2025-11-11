from abc import ABC, abstractmethod

from audit.loggers.youtube_logger import YoutubeLogEntry


class LogRepository(ABC):
    @abstractmethod
    async def save_channel_log(self, log: YoutubeLogEntry) -> None:
        """로그를 저장합니다.

        Args:
            log (YoutubeLogEntry): 저장할 로그 데이터
        """
        pass

    @abstractmethod
    async def save_video_raw_data_log(self, log: YoutubeLogEntry) -> None:
        """로그를 저장합니다.

        Args:
            log (YoutubeLogEntry): 저장할 로그 데이터
        """
        pass
