class DomainError(Exception):
    """도메인 관련 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ChannelIdDuplicateError(DomainError):
    """채널 ID 중복 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str):
        super().__init__(message)


class APIKeyServiceError(DomainError):
    """APIKeyService 관련 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str):
        super().__init__(message)


class YoutubeAPIRequestError(DomainError):
    """Youtube API 요청 관련 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str):
        super().__init__(message)
