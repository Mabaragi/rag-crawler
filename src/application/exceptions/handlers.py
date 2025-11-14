from fastapi import Request
from fastapi.responses import JSONResponse


def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    print(f"Validation error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error: Response validation failed."})
