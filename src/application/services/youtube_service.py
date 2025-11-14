# application/services/crawl_service.py (응용 서비스 계층)
import datetime

from audit.loggers.log_repository import LogRepository
from audit.loggers.youtube_logger import YoutubeLogEntry
from domain.adapter.youtube_api_adapter import YoutubeApiAdapter
from domain.exceptions.youtube import APIKeyServiceError, YoutubeAPIRequestError
from domain.model.youtube import APIKey, YoutubeChannel, YoutubeVideoRawData
from domain.repository.youtube_repository import (
    APIKeyRepository,
    YoutubeRepository,
)  # 인터페이스만 임포트
from shared.utils import is_quota_reseted


class ChannelReadService:
    def __init__(self, channel_repo: YoutubeRepository):
        self.channel_repo = channel_repo

    async def list_channels(self) -> list[YoutubeChannel]:
        """저장된 모든 채널 정보를 조회하는 메서드

        Returns:
            list[YoutubeChannel]: 저장된 채널 정보 리스트
        """
        try:
            channels = await self.channel_repo.get_channels()
            return channels
        except Exception as e:
            raise Exception(f"채널 조회 중 오류 발생: {e}")


class ChannelCreateService:
    # 생성자는 추상 타입(인터페이스)만 요구함
    def __init__(self, channel_repo: YoutubeRepository, api_key_repo: APIKeyRepository, api_client: YoutubeApiAdapter):
        self.channel_repo = channel_repo
        self.api_key_repo = api_key_repo
        self.api_client = api_client

    async def insert_channel(self, channel_name: str, channel_handle: str, streamer_name: str) -> YoutubeChannel:
        """채널을 삽입하는 메서드

        Args:
            channel_name (str): 유튜브 채널 이름
            channel_handle (str): 유튜브 채널 핸들
            streamer_name (str): 스트리머 이름

        Raises:
            ValueError: 채널 ID를 가져올 수 없는 경우

        Returns:
            YoutubeChannel: 생성된 유튜브 채널 객체
        """
        api_key = await self.api_key_repo.get_api_key()
        channel_id = await self.api_client.fetch_channel_id(channel_handle, api_key.api_key)
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
        return channel


class ChannelUpdateService:
    def __init__(self, channel_repo: YoutubeRepository):
        self.channel_repo = channel_repo

    async def update_channel(self, channel: YoutubeChannel) -> YoutubeChannel:
        """채널 정보를 업데이트하는 메서드

        Args:
            channel (YoutubeChannel): 업데이트할 채널 정보
        """
        await self.channel_repo.update_channel(channel=channel)
        return channel

    async def bulk_update_channels(self, **kwargs) -> list[YoutubeChannel]:
        """여러 채널 정보를 일괄 업데이트하는 메서드

        Args:
            channels (list[YoutubeChannel]): 업데이트할 채널 정보 리스트
        """
        channels = await self.channel_repo.get_channels()
        channel_dicts = []
        for channel in channels:
            channel._update_updated_at()
            channel_dict = channel.to_dict()
            for key, value in kwargs.items():
                if key in channel_dict:
                    setattr(channel, key, value)
            channel_dicts.append(channel_dict)
        new_channels = [YoutubeChannel(**channel_dict) for channel_dict in channel_dicts]
        for channel in new_channels:
            await self.channel_repo.update_channel(channel=channel)
        return new_channels


class RawDataCrawlService:
    def __init__(
        self,
        youtube_repo: YoutubeRepository,
        api_key_repo: APIKeyRepository,
        api_client: YoutubeApiAdapter,
        log_repo: LogRepository,
    ):
        self.youtube_repo = youtube_repo
        self.api_key_repo = api_key_repo
        self.api_client = api_client
        self.log_repo = log_repo

    async def initialize_you_tube_video_data(self) -> None:
        """유튜브 채널의 원시 비디오 데이터를 초기화합니다.

        Raises:
            ValueError: 응답이 없는 경우
            YoutubeAPIRequestError: 유튜브 API 요청 중 오류가 발생한 경우
        """
        youtube_channels = await self.youtube_repo.get_uninitialized_channels()

        for youtube_channel in youtube_channels:
            try:
                api_key = await self.api_key_repo.get_api_key()
                previously_used = api_key.quota_used

                if not api_key.is_search_quota_available():
                    await self.log_repo.save_channel_log(
                        YoutubeLogEntry(
                            domain_id=youtube_channel.channel_id,
                            level="INFO",
                            message="API 키 쿼터 초과",
                            details={"quota_used": api_key.quota_used, "channel": youtube_channel.to_dict()},
                        )
                    )
                    break
                for published_after, published_before in [
                    ("2023-01-01T00:00:00Z", "2024-01-01T00:00:00Z"),
                    ("2024-01-01T00:01:00Z", "2025-01-01T00:00:00Z"),
                    ("2025-01-01T00:01:00Z", "2026-01-01T00:00:00Z"),
                ]:
                    page_token = None
                    count = 0
                    while True:
                        response = await self._fetch_channel_videos(
                            channel_id=youtube_channel.channel_id,
                            api_key=api_key,
                            page_token=page_token,
                            published_after=published_after,
                            published_before=published_before,
                        )
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
                        await self.log_repo.save_video_raw_data_log(
                            YoutubeLogEntry(
                                domain_id=youtube_channel.channel_id,
                                level="INFO",
                                message="비디오 원시 데이터 수집 성공",
                                details={"collected_count": len(youtube_raw_data_list)},
                            )
                        )
                        # 2. 로직 수행 및 저장 요청 (인터페이스 메서드 사용)
                        await self.youtube_repo.bulk_save_raw_data(raw_data_list=youtube_raw_data_list)
                        page_token = response.get("nextPageToken")
                        if not page_token:
                            # print("더 이상 크롤링할 페이지가 없습니다.")
                            break
            # 수집중 에러 발생시에 수집하던 채널 데이터 모두 삭제
            except Exception as e:
                await self.log_repo.save_channel_log(
                    YoutubeLogEntry(
                        domain_id=youtube_channel.channel_id,
                        level="ERROR",
                        message="채널 크롤링 중 오류 발생",
                        details={"quota_used": api_key.quota_used - previously_used, "error": str(e)},
                    )
                )

                await self.youtube_repo.clear_raw_data_for_channel(channel=youtube_channel)
            # 정상 완료시 채널 초기화 상태 업데이트
            else:
                await self.log_repo.save_channel_log(
                    YoutubeLogEntry(
                        domain_id=youtube_channel.channel_id,
                        level="INFO",
                        message="채널 크롤링 성공",
                        details={"quota_used": api_key.quota_used - previously_used},
                    )
                )

                youtube_channel.update_initialized()
                await self.youtube_repo.update_channel(channel=youtube_channel)
            # 어떤 경우에도 사용한 쿼터는 업데이트
            finally:
                await self.api_key_repo.update_api_key(api_key=api_key)

    async def fetch_videos_from_initialized_channels(self) -> None:
        """초기화된 유튜브 채널을 가져오는 메서드"""
        youtube_channels = await self.youtube_repo.get_initialized_channels()
        for youtube_channel in youtube_channels:
            api_key = await self.api_key_repo.get_api_key()
            if not api_key.is_search_quota_available():
                await self.log_repo.save_channel_log(
                    YoutubeLogEntry(
                        domain_id=youtube_channel.channel_id,
                        level="INFO",
                        message="초기화 이후 비디오 수집 도중 API 키 쿼터 초과",
                        details={"quota_used": api_key.quota_used, "channel": youtube_channel.to_dict()},
                    )
                )
                break

            page_token = None
            count = 0
            videos_for_save = []
            while True:
                response = await self._fetch_channel_videos(
                    channel_id=youtube_channel.channel_id,
                    api_key=api_key,
                    page_token=page_token,
                )
                if not response:
                    raise ValueError("응답 데이터를 가져올 수 없습니다")
                items = response.get("items", [])
                video_items = [item for item in items if item.get("id", {}).get("kind") == "youtube#video"]

                crawl_finished = False
                for item in video_items:
                    video_id = item.get("id", {}).get("videoId", "")
                    existing_video = await self.youtube_repo.get_video_by_id(video_id=video_id)
                    if existing_video:
                        crawl_finished = True
                        break  # 이미 저장된 비디오인 경우 데이터 수집 완료
                    youtube_raw_data = YoutubeVideoRawData(
                        video_id=item.get("id", {}).get("videoId", ""),
                        channel_id=youtube_channel.channel_id,
                        streamer_name=youtube_channel.streamer_name,
                        raw_data=item,
                        created_at=datetime.datetime.now(datetime.timezone.utc),
                    )
                    await self.log_repo.save_video_raw_data_log(
                        YoutubeLogEntry(
                            domain_id=video_id,
                            level="INFO",
                            message="초기화 이후 비디오 원시 데이터 수집 성공",
                            details={"video_id": video_id, "channel": youtube_channel.to_dict()},
                        )
                    )
                    count += 1
                    videos_for_save.append(youtube_raw_data)
                if crawl_finished:
                    break
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
            if videos_for_save:
                await self.youtube_repo.bulk_save_raw_data(raw_data_list=videos_for_save)
            await self.api_key_repo.update_api_key(api_key=api_key)
            await self.log_repo.save_channel_log(
                YoutubeLogEntry(
                    domain_id=youtube_channel.channel_id,
                    level="INFO",
                    message="초기화 이후 비디오 수집 완료",
                    details={"collected_count": count, "quota_used": api_key.quota_used},
                )
            )

    async def crawl_transcripts(self) -> None:
        """유튜브 채널의 비디오 자막 데이터를 크롤링하는 메서드"""

        pass

    async def _fetch_channel_videos(
        self,
        channel_id: str,
        api_key: APIKey,
        page_token: str | None = None,
        published_after: str | None = None,
        published_before: str | None = None,
    ) -> dict:
        """특정 채널의 동영상 목록을 가져오는 내부 헬퍼 메서드

        Args:
            channel_id (str): YouTube 채널 ID
            api_key (str): YouTube API 키
            page_token (str | None, optional): 다음 페이지 토큰. Defaults to None.
            published_after (str | None, optional): 동영상 게시 이후 시간. Defaults to None.
            published_before (str | None, optional): 동영상 게시 이전 시간. Defaults to None.

        Returns:
            dict | None: 동영상 목록 또는 None
        """
        try:
            response = await self.api_client.fetch_channel_videos(
                api_key=api_key.api_key,
                channel_id=channel_id,
                published_after=published_after,
                published_before=published_before,
                page_token=page_token,
            )
            if not response:
                raise ValueError("응답 데이터를 가져올 수 없습니다")
        except Exception as e:
            raise YoutubeAPIRequestError(f"유튜브 API 요청 중 오류 발생: {e}")
        api_key.use_search_quota()
        return response


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

    async def get_api_key(self) -> APIKey:
        """저장된 API 키를 조회하는 메서드

        Returns:
            APIKey | None: 저장된 API 키 객체 또는 None
        """
        try:
            api_key = await self.api_key_repo.get_api_key()
            return api_key
        except Exception as e:
            raise APIKeyServiceError(f"API 키 조회 중 오류 발생: {e}")

    async def insert_api_key(self, api_key: str) -> None:
        """API 키를 저장하는 메서드

        Args:
            api_key (str): 저장할 API 키
        """

        api_key_obj = APIKey(api_key=api_key)
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
