# application/services/crawl_service.py (응용 서비스 계층)
import datetime

from application.exceptions import APIKeyServiceError
from domain.adapter.youtube_api_adapter import YoutubeApiAdapter
from domain.model.youtube import APIKey, YoutubeChannel, YoutubeVideoRawData
from domain.repository.youtube_repository import (
    APIKeyRepository,
    YoutubeRepository,
)  # 인터페이스만 임포트
from shared.utils import is_quota_reseted


class ChannelInsertService:
    # 생성자는 추상 타입(인터페이스)만 요구함
    def __init__(self, channel_repo: YoutubeRepository, api_client: YoutubeApiAdapter):
        self.channel_repo = channel_repo
        self.api_client = api_client

    async def insert_channel(self, channel_name: str, channel_handle: str, streamer_name: str) -> None:
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
            streamer_name=streamer_name,
        )
        # 2. 로직 수행 및 저장 요청 (인터페이스 메서드 사용)
        await self.channel_repo.save_channel(channel=channel)


class RawDataCrawlService:
    def __init__(self, youtube_repo: YoutubeRepository, api_client: YoutubeApiAdapter):
        self.youtube_repo = youtube_repo
        self.api_client = api_client

    async def crawl_and_save_raw_data(self, youtube_channel: YoutubeChannel) -> None:
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
                await self.youtube_repo.bulk_save_raw_data(raw_data_list=youtube_raw_data_list)
                page_token = response.get("nextPageToken")
                if not page_token:
                    print("더 이상 크롤링할 페이지가 없습니다.")
                    break
        # 완료시 채널 초기화 상태 업데이트
        youtube_channel.update_initialized()
        await self.youtube_repo.update_channel(channel=youtube_channel)


class APIKeyService:
    def __init__(self, api_key_repo: APIKeyRepository):
        self.api_key_repo = api_key_repo

    async def list_api_keys(self) -> list[APIKey]:
        """저장된 모든 API 키를 조회하는 메서드

        Returns:
            list[APIKey]: 저장된 API 키 목록
        """
        try:
            api_keys = await self.api_key_repo.list_api_keys()
            return api_keys
        except Exception as e:
            raise APIKeyServiceError(f"API 키 조회 중 오류 발생: {e}")

    async def insert_api_key(self, api_key: str) -> None:
        """API 키를 저장하는 메서드

        Args:
            api_key (str): 저장할 API 키
        """

        api_key_obj = APIKey(key=api_key)
        try:
            await self.api_key_repo.insert_api_key(api_key=api_key_obj)
        except Exception as e:
            raise APIKeyServiceError(f"API 키 저장 중 오류 발생: {e}")

    async def update_quota_used(self, quota_used: int) -> None:
        """API 키의 사용량을 업데이트하는 메서드

        Args:
            api_key (str): 업데이트할 API 키
            quota_used (int): 사용량
        """
        try:
            existing_key = await self.api_key_repo.get_api_key()
            if not existing_key:
                raise APIKeyServiceError("존재하지 않는 API 키입니다.")
            # 만약 updated_at이 전날의 07시 이전이라면 quota_used를 초기화
            if is_quota_reseted(existing_key.updated_at):
                existing_key.quota_used = 0
            existing_key.quota_used += quota_used
            await self.api_key_repo.update_api_key(api_key=existing_key)
        except Exception as e:
            raise APIKeyServiceError(f"API 키 사용량 업데이트 중 오류 발생: {e}")
