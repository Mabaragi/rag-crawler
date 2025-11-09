import httpx

from domain.adapter.youtube_api_adapter import YoutubeApiAdapter


class YoutubeAPIClient(YoutubeApiAdapter):
    def __init__(self):
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def fetch_channel_id(self, handle: str, api_key: str) -> str | None:
        """Fetch YouTube channel ID by handle.

        Args:
            handle (str): The YouTube channel handle.
            api_key (str): The API key for authentication.

        Returns:
            str | None: The YouTube channel ID or None if not found.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/channels",
                params={"key": api_key, "forHandle": handle},
            )
        if response.status_code == 200:
            return response.json().get("items", [])[0].get("id")
        else:
            print(f"Error fetching channel data: {response.status_code, response.text}")
        return None

    async def fetch_channel_videos(
        self,
        api_key: str,
        channel_id: str,
        page_token: str | None = None,
        published_after: str | None = None,
        published_before: str | None = None,
    ):
        """Fetch YouTube channel videos.

        Args:
            api_key (str):  API key for authentication.
            channel_id (str): YouTube channel ID for which to fetch videos.
            page_token (str | None, optional): page token for pagination. Defaults to None.
            published_after (str | None, optional): terms to filter videos. Defaults to None.
            published_before (str | None, optional): terms to filter videos. Defaults to None.

        Returns:
            _type_: _description_
        """
        params = {
            "key": api_key,
            "channelId": channel_id,
            "part": "snippet",
            "maxResults": "50",
            "order": "date",
        }
        if published_after:
            params["publishedAfter"] = published_after
        if published_before:
            params["publishedBefore"] = published_before
        if page_token:
            params["pageToken"] = page_token

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/search", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching videos: {response.status_code, response.text}")
        return None
