# main.py 또는 commands/cli.py (조립 계층)
import os
import sys

from dotenv import load_dotenv

# 환경 변수 로드 (예: MONGO_URI)
from application.services.channel_insert_service import ChannelInsertService
from infrastructure.api.youtube_api_client import YoutubeAPIClient
from infrastructure.persistence.mongo_repository import MongoChannelRepository

load_dotenv()


# --- 3. 실행 함수 ---
def run_channel_insert_command(
    channel_name: str, channel_handle: str, streamer_name: str
) -> None:
    """
    크롤링 서비스의 의존성을 주입하고 실행하는 메인 함수
    """

    # [A] 리포지토리 구현체 객체 생성 (인프라스트럭처)
    # 실제 MongoDB 연결 설정이 여기서 이루어집니다.
    mongo_repo = MongoChannelRepository()
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


# --- 4. CLI 진입점 ---
if __name__ == "__main__":
    # 커맨드라인 인수로 채널 정보를 받는다고 가정
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
