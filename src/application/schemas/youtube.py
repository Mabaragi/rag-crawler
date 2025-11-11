# # app/schemas/channel.py (가정)

from pydantic import BaseModel, Field


class ChannelInsertRequest(BaseModel):
    """채널 삽입 요청 스키마"""

    channel_name: str = Field(default=..., description="유튜브 채널 이름", examples=["시부키 다시보기"])
    channel_handle: str = Field(default=..., description="유튜브 채널 핸들", examples=["@shibuki"])
    streamer_name: str = Field(default=..., description="스트리머 이름", examples=["시부키"])
