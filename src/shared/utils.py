import datetime
from dataclasses import fields, is_dataclass
from typing import Any, Type, TypeVar

YOUTUBE_API_RESET_HOUR = 7
YOUTUBE_API_QUOTA_LIMIT = 10000


def is_quota_reseted(updated_at: datetime.datetime) -> bool:
    """API 키의 쿼터가 리셋되었는지 확인하는 유틸리티 함수

    Args:
        updated_at (datetime.datetime): API 키의 마지막 업데이트 시간

    Returns:
        bool: 쿼터가 리셋되었으면 True, 아니면 False
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    if updated_at.hour < YOUTUBE_API_RESET_HOUR:
        if now.hour >= YOUTUBE_API_RESET_HOUR:
            return True
    if updated_at.hour >= YOUTUBE_API_RESET_HOUR:
        if now.hour >= YOUTUBE_API_RESET_HOUR and updated_at.date() < now.date():
            return True
    return False


def is_quota_exceeded(quota_used: int, updated_at: datetime.datetime) -> bool:
    """API 키의 쿼터 사용량이 한도를 초과했는지 확인하는 유틸리티 함수

    Args:
        quota_used (int): 현재 쿼터 사용량
        updated_at (datetime.datetime): API 키의 마지막 업데이트 시간

    Returns:
        bool: 쿼터 사용량이 한도를 초과했으면 True, 아니면 False
    """
    if is_quota_reseted(updated_at):
        return False
    return quota_used >= YOUTUBE_API_QUOTA_LIMIT


T = TypeVar("T")


def data_class_from_dict(cls: Type[T], data: dict[str, Any]) -> T:
    """딕셔너리로 부터 데이터클래스 인스턴스를 생성하는 유틸리티 함수

    Args:
        cls (Type[T]): _description_
        data (dict[str, Any]): _description_

    Raises:
        ValueError: _cls_ 가 데이터클래스가 아닐 경우

    Returns:
        T: _cls_ 타입의 데이터클래스 인스턴스
    """
    if not is_dataclass(cls):
        raise ValueError(f"{cls} is not a dataclass")
    valid_keys = [field.name for field in fields(cls)]
    data = {k: v for k, v in data.items() if k in valid_keys}
    return cls(**data)
