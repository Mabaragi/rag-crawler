# main.py 또는 commands/cli.py (조립 계층)
import os
import sys

from dotenv import load_dotenv

# 환경 변수 로드 (예: MONGO_URI)
from application.services.youtube_service import ChannelInsertService, RawDataCrawlService
from domain.model.youtube import YoutubeChannel
from infrastructure.api.youtube_api_client import YoutubeAPIClient
from infrastructure.persistence.mongo_repository import MongoYoutubeRepository

load_dotenv()


# --- 3. 실행 함수 ---
def run_channel_insert_command(channel_name: str, channel_handle: str, streamer_name: str) -> None:
    """채널 정보를 수집하고 데이터베이스에 저장합니다.

    Args:
        channel_name (str): 채널 이름
        channel_handle (str): 채널 핸들
        streamer_name (str): 스트리머 이름
    """

    # [A] 리포지토리 구현체 객체 생성 (인프라스트럭처)
    # 실제 MongoDB 연결 설정이 여기서 이루어집니다.
    mongo_repo = MongoYoutubeRepository()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("❌ YOUTUBE_API_KEY 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)
    api_client = YoutubeAPIClient(api_key=api_key)
    # [B] 응용 서비스 객체 생성 및 의존성 주입 (DIP)
    # 서비스는 인터페이스(YoutubeChannelRepository)를 통해 구현체를 전달받습니다.
    crawl_service = ChannelInsertService(channel_repo=mongo_repo, api_client=api_client)

    # [C] 서비스 메서드 실행
    print(f"\n🚀 크롤링을 시작합니다: {channel_name} ({channel_handle})")
    try:
        crawl_service.start_crawl(
            channel_name=channel_name,
            channel_handle=channel_handle,
            streamer_name=streamer_name,
        )
        print("🎉 크롤링 및 저장이 성공적으로 완료되었습니다.")

    except Exception as e:
        print(f"❌ 크롤링 중 오류가 발생했습니다: {e}")
        # 실제 환경에서는 로깅 처리
        sys.exit(1)


def run_video_rawdata_crawl_command() -> None:
    """유튜브 원시 데이터를 수집하고 데이터베이스에 저장합니다.

    Args:
        youtube_channel (YoutubeChannel): 유튜브 채널 객체
    """

    # [A] 리포지토리 구현체 객체 생성 (인프라스트럭처)
    # 실제 MongoDB 연결 설정이 여기서 이루어집니다.
    mongo_repo = MongoYoutubeRepository()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("❌ YOUTUBE_API_KEY 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)
    api_client = YoutubeAPIClient(api_key=api_key)

    # youtube_channel = mongo_repo.get_channel_by_id("UCZznqq0-ZBvtel1ieA8f35g")  # 예시 채널 ID
    youtube_channels = mongo_repo._db["channels"].find({"initialized": False})
    for channel_data in youtube_channels:
        channel_data.pop("_id", None)  # MongoDB의 _id 필드 제거
        youtube_channel = YoutubeChannel(**channel_data)

        raw_data_crawl_service = RawDataCrawlService(
            youtube_repo=mongo_repo,
            api_client=api_client,
        )
        raw_data_crawl_service.crawl_and_save_raw_data(youtube_channel=youtube_channel)


# --- 4. CLI 진입점 ---
if __name__ == "__main__":
    # 커맨드라인 인수로 채널 정보를 받는다고 가정
    command = input("커맨드를 선택해주세요. '채널' 저장 또는 '비디오' 수집: ")
    if command == "채널":
        while True:
            print("유튜브 채널 아이디를 수집합니다. Ctrl+C로 종료할 수 있습니다.")
            input_name = input("채널 이름을 입력하세요: ")
            input_handle = input("채널 핸들을 입력하세요: ")
            input_streamer = input("스트리머 이름을 입력하세요: ")
            try:
                run_channel_insert_command(
                    channel_name=input_name,
                    channel_handle=input_handle,
                    streamer_name=input_streamer,
                )
            except Exception as e:
                print(f"❌ 크롤링 중 오류가 발생했습니다: {e}")
    elif command == "비디오":
        run_video_rawdata_crawl_command()
        print("비디오 원시 데이터 수집이 완료되었습니다.")
