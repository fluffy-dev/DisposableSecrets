from fastapi import FastAPI

from src.cors import init_middleware
from src.routes import router


def get_app() -> FastAPI:
    app = FastAPI()

    init_middleware(app)

    app.include_router(router)
    return app
