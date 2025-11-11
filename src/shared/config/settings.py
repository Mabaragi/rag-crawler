# infrastructure/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    YOUTUBE_API_KEY: str
    MONGO_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# main.py 또는 앱 초기화 파일
# 1. 설정 객체를 한 번만 생성하여 메모리에 저장
settings = Settings()  # type: ignore


# 2. DI 시스템을 통해 다른 모듈에 전달
def get_settings() -> Settings:
    # 이 함수는 항상 동일한 인스턴스를 반환
    return settings


# 이제 모든 리포지토리나 어댑터는 get_settings() 의존성을 통해 단일 객체에 접근합니다.
