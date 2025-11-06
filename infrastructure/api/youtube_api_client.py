import os
import requests
from domain.adapter.youtube_api_adapter import YoutubeApiAdapter


class YoutubeAPIClient(YoutubeApiAdapter):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def fetch_channel_id(self, handle: str):
        """
        YouTube 채널 ID를 가져옵니다.
        """
        response = requests.get(
            f"{self.base_url}/channels",
            params={"key": self.api_key, "forHandle": handle},
        )
        if response.status_code == 200:
            return response.json().get("items", [])[0].get("id")
        else:
            print(f"Error fetching channel data: {response.status_code, response.text}")
        return None
