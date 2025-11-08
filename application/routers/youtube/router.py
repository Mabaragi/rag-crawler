from fastapi import APIRouter, Depends, Form
from typing_extensions import Annotated

from application.schemas.youtube import ChannelInsertRequest
from application.services.youtube_service import APIKeyService, ChannelInsertService

from .dependencies import (
    get_api_key_service,
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
    await service.insert_channel(
        channel_name=request.channel_name,
        channel_handle=request.channel_handle,
        streamer_name=request.streamer_name,
    )
    return {"status": "Channel insertion initiated"}


@router.get("/api_keys/")
async def list_api_keys(
    service: APIKeyService = Depends(get_api_key_service),
):
    api_keys = await service.list_api_keys()
    return {"api_keys": [api_key.to_dict() for api_key in api_keys]}


@router.post("/insert_api_key/")
async def insert_api_key(
    api_key: str = Form(...),
    service: APIKeyService = Depends(get_api_key_service),
):
    await service.insert_api_key(api_key=api_key)
    return {"status": "API key insertion initiated"}
