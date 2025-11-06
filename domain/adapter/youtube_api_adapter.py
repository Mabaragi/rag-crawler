from abc import ABC, abstractmethod


class YoutubeApiAdapter(ABC):

    @abstractmethod
    def fetch_channel_id(self, handle: str):
        pass
