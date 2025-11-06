import requests
from domain.model.url import YOUTUBE_DATA_API_CHANNELS_URL
import os, dotenv

dotenv.load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YoutubeChannel:
    def __init__(self, channel_name: str, channel_handle: str, channel_id: str):
        self.channel_name = channel_name
        self.channel_handle = channel_handle
        self.channel_id = channel_id
