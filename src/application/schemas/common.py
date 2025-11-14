from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    status: str = Field(default="success", description="요청 처리 상태")
    message: str = Field(default="OK", description="추가 메시지")
    data: dict | None = Field(default=None, description="API 데이터 페이로드")
