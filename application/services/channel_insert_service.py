# application/services/crawl_service.py (응용 서비스 계층)
from domain.adapter.youtube_api_adapter import YoutubeApiAdapter
from domain.model.youtube import YoutubeChannel
from domain.repository.youtube_channel_repository import (
    YoutubeChannelRepository,
)  # 인터페이스만 임포트


class ChannelInsertService:
    # 생성자는 추상 타입(인터페이스)만 요구함
    def __init__(
        self, channel_repo: YoutubeChannelRepository, api_client: YoutubeApiAdapter
    ):
        self.channel_repo = channel_repo
        self.api_client = api_client

    def start_crawl(
        self, channel_name: str, channel_handle: str, streamer_name: str
    ) -> None:
        """
        채널 정보를 크롤링하고 저장하는 메서드
        """
        channel_id = self.api_client.fetch_channel_id(channel_handle)
        if not channel_id:
            raise ValueError(f"채널 ID를 가져올 수 없습니다: {channel_handle}")

        channel = YoutubeChannel(
            channel_name=channel_name,
            channel_handle=channel_handle,
            channel_id=channel_id,
        )
        # 2. 로직 수행 및 저장 요청 (인터페이스 메서드 사용)
        self.channel_repo.save(
            channel=channel, channel_id=channel_id, streamer_name=streamer_name
        )
