# # app/schemas/channel.py (가정)

from datetime import datetime

from pydantic import BaseModel, Field

from application.schemas.common import SuccessResponse
from domain.model.youtube import ChannelCrawlSchedule


class ChannelBaseSchema(BaseModel):
    """채널 기본 스키마"""

    channel_name: str = Field(default=..., description="유튜브 채널 이름", examples=["시부키 다시보기"])
    channel_handle: str = Field(default=..., description="유튜브 채널 핸들", examples=["@shibukireplay"])
    streamer_name: str = Field(default=..., description="스트리머 이름", examples=["시부키"])


class ChannelInsertRequest(ChannelBaseSchema):
    """채널 삽입 요청 스키마"""

    pass


class ChannelListResponse(ChannelBaseSchema):
    """채널 목록 응답 스키마"""

    channel_id: str
    initialized: bool
    created_at: datetime
    updated_at: datetime
    schedule: ChannelCrawlSchedule


class ChannelInsertResponse(SuccessResponse):
    """채널 삽입 응답 스키마"""

    data: dict = Field(default_factory=lambda: {}, description="생성된 채널 메타 정보")


__all__ = [
    "ChannelInsertRequest",
    "ChannelInsertResponse",
]
