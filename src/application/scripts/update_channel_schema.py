import asyncio

from application.services.youtube_service import ChannelUpdateService
from infrastructure.persistence.mongo_repository import MongoYoutubeRepository


async def main():
    channel_service = ChannelUpdateService(MongoYoutubeRepository())
    await channel_service.bulk_update_channels()


if __name__ == "__main__":
    asyncio.run(main())
