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

    def fetch_channel_videos(
        self,
        channel_id: str,
        page_token: str | None = None,
        published_after: str | None = None,
        published_before: str | None = None,
    ):
        """
        특정 채널의 동영상 목록을 가져옵니다.
        """
        params = {
            "key": self.api_key,
            "channelId": channel_id,
            "part": "snippet",
            "maxResults": "50",
            "order": "date",
            "publishedAfter": published_after,
            "publishedBefore": published_before,
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(f"{self.base_url}/search", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching videos: {response.status_code, response.text}")
        return None
