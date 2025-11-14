from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError

from application.exceptions.handlers import validation_exception_handler
from application.routers.youtube.router import router as youtube_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_exception_handler(ResponseValidationError, validation_exception_handler)

    @app.get("/")
    def read_root():
        return {"Hello": "World!!!!"}

    app.include_router(youtube_router)

    return app


app = create_app()
