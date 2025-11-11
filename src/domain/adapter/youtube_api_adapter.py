from abc import ABC, abstractmethod


class YoutubeApiAdapter(ABC):
    @abstractmethod
    async def fetch_channel_id(self, handle: str, api_key: str) -> str | None:
        """YouTube 채널 ID를 가져옵니다.

        Args:
            handle (str): YouTube 채널 핸들
            api_key (str): YouTube API 키

        Returns:
            str | None: 채널 ID 또는 None
        """
        pass

    @abstractmethod
    async def fetch_channel_videos(
        self,
        channel_id: str,
        api_key: str,
        page_token: str | None = None,
        published_after: str | None = None,
        published_before: str | None = None,
    ) -> dict | None:
        """특정 채널의 동영상 목록을 가져옵니다.

        Args:
            channel_id (str): YouTube 채널 ID
            api_key (str): YouTube API 키
            page_token (str | None, optional): 다음 페이지 토큰. Defaults to None.
            published_after (str | None, optional): 동영상 게시 이후 시간. Defaults to None.
            published_before (str | None, optional): 동영상 게시 이전 시간. Defaults to None.

        Returns:
            dict | None: 동영상 목록 또는 None
        """
        pass
