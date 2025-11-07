# application/services/crawl_service.py (응용 서비스 계층)
import datetime

from domain.adapter.youtube_api_adapter import YoutubeApiAdapter
from domain.model.youtube import YoutubeChannel, YoutubeVideoRawData
from domain.repository.youtube_repository import (
    YoutubeRepository,
)  # 인터페이스만 임포트


class ChannelInsertService:
    # 생성자는 추상 타입(인터페이스)만 요구함
    def __init__(self, channel_repo: YoutubeRepository, api_client: YoutubeApiAdapter):
        self.channel_repo = channel_repo
        self.api_client = api_client

    def start_crawl(self, channel_name: str, channel_handle: str, streamer_name: str) -> None:
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
        self.channel_repo.save_channel(channel=channel, channel_id=channel_id, streamer_name=streamer_name)


class RawDataCrawlService:
    def __init__(self, youtube_repo: YoutubeRepository, api_client: YoutubeApiAdapter):
        self.youtube_repo = youtube_repo
        self.api_client = api_client

    def crawl_and_save_raw_data(self, youtube_channel: YoutubeChannel) -> None:
        """
        유튜브 원시 데이터를 크롤링하고 저장하는 메서드
        """
        for published_after, published_before in [
            ("2023-01-01T00:00:00Z", "2024-01-01T00:00:00Z"),
            ("2024-01-01T00:01:00Z", "2025-01-01T00:00:00Z"),
            ("2025-01-01T00:01:00Z", "2026-01-01T00:00:00Z"),
        ]:
            page_token = None
            count = 0
            while True:
                response = self.api_client.fetch_channel_videos(
                    channel_id=youtube_channel.channel_id,
                    published_after=published_after,
                    published_before=published_before,
                    page_token=page_token,
                )
                if not response:
                    raise ValueError(f"채널 원시 데이터를 가져올 수 없습니다: {youtube_channel.channel_id}")
                items = response.get("items", [])
                if not items:
                    break
                youtube_raw_data_list = [
                    YoutubeVideoRawData(
                        video_id=item.get("id", {}).get("videoId", ""),
                        channel_id=youtube_channel.channel_id,
                        streamer_name=youtube_channel.streamer_name,
                        raw_data=item,
                        created_at=datetime.datetime.now(datetime.timezone.utc),
                    )
                    for item in items
                    if item.get("id", {}).get("kind") == "youtube#video"  # 동영상 항목만 처리
                ]
                count += len(youtube_raw_data_list)
                print(f"크롤링한 원시 데이터 수: {count}, 페이지 토큰: {page_token}")
                # 2. 로직 수행 및 저장 요청 (인터페이스 메서드 사용)
                self.youtube_repo.bulk_save_raw_data(raw_data_list=youtube_raw_data_list)
                page_token = response.get("nextPageToken")
                if not page_token:
                    print("더 이상 크롤링할 페이지가 없습니다.")
                    break
        # 완료시 채널 초기화 상태 업데이트
        youtube_channel.update_initialized()
        self.youtube_repo.update_channel(channel=youtube_channel)
