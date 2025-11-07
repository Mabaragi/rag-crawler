from fastapi import APIRouter, Depends, Form
from typing_extensions import Annotated

from application.schemas.youtube import ChannelInsertRequest
from application.services.youtube_service import ChannelInsertService

from .dependencies import (
    get_channel_insert_service,
)

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/health")
async def health_check():
    return {"status": "YouTube router is healthy"}


@router.post("/insert_channel/")
async def insert_channel(
    request: Annotated[ChannelInsertRequest, Form()],
    service: ChannelInsertService = Depends(get_channel_insert_service),
):
    service.insert_channel(
        channel_name=request.channel_name,
        channel_handle=request.channel_handle,
        streamer_name=request.streamer_name,
    )
    return {"status": "Channel insertion initiated"}
