from abc import ABC, abstractmethod


class YoutubeApiAdapter(ABC):

    @abstractmethod
    def fetch_channel_id(self, handle: str):
        pass

    @abstractmethod
    def fetch_channel_videos(
        self,
        channel_id: str,
        page_token: str | None = None,
        published_after: str | None = None,
        published_before: str | None = None,
    ):
        pass
