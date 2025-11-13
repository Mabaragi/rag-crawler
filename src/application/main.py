from fastapi import FastAPI

from application.routers.youtube.router import router as youtube_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World!!"}


app.include_router(youtube_router)
