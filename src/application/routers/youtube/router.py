from fastapi import APIRouter, Depends, Form, HTTPException
from typing_extensions import Annotated

from application.schemas.youtube_schema import ChannelInsertRequest, ChannelInsertResponse, ChannelListResponse
from application.services.youtube_service import (
    APIKeyService,
    ChannelCreateService,
    ChannelReadService,
    RawDataCrawlService,
)

from .dependencies import (
    get_api_key_service,
    get_channel_create_service,
    get_channel_read_service,
    get_raw_data_crawl_service,
)

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/channels/", response_model=list[ChannelListResponse])
async def list_channels(
    service: ChannelReadService = Depends(get_channel_read_service),
):
    channels = await service.list_channels()
    return channels


@router.post("/channels/insert/")
async def insert_channel(
    request: Annotated[ChannelInsertRequest, Form()],
    service: ChannelCreateService = Depends(get_channel_create_service),
):
    try:
        channel = await service.insert_channel(
            channel_name=request.channel_name,
            channel_handle=request.channel_handle,
            streamer_name=request.streamer_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ChannelInsertResponse(data=channel.to_dict())


@router.post("/videos/raw_data/initialize/")
async def initialize_raw_data(
    service: RawDataCrawlService = Depends(get_raw_data_crawl_service),
):
    await service.initialize_you_tube_video_data()
    return {"status": "Raw data crawling initiated"}


@router.post("/videos/raw_data/fetch/")
async def fetch_raw_data(
    service: RawDataCrawlService = Depends(get_raw_data_crawl_service),
):
    await service.fetch_videos_from_initialized_channels()
    return {"status": "Raw data fetched"}


# @router.get("/api_keys/")
# async def list_api_keys(
#     service: APIKeyService = Depends(get_api_key_service),
# ):
#     api_keys = await service.list_api_keys()
#     return {"api_keys": [api_key.to_dict() for api_key in api_keys]}


@router.get("/api_key/")
async def get_api_key(
    service: APIKeyService = Depends(get_api_key_service),
):
    api_key = await service.get_api_key()
    return {"api_key": api_key.to_dict()}


@router.post("/insert_api_key/")
async def insert_api_key(
    api_key: str = Form(...),
    service: APIKeyService = Depends(get_api_key_service),
):
    await service.insert_api_key(api_key=api_key)
    return {"status": "API key insertion initiated"}
