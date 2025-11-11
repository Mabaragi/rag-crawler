class APIKeyServiceError(Exception):
    """APIKeyService 관련 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"APIKeyServiceError: {self.message}"


class YoutubeAPIRequestError(Exception):
    """Youtube API 요청 관련 예외 클래스

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"YoutubeAPIRequestError: {self.message}"
