from fastapi import FastAPI

from src.cors import init_middleware
from src.routes import router

from src.settings import settings


def get_app() -> FastAPI:
    app = FastAPI(docs_url="/docs" if settings.debug else None,
                  redoc_url="/redoc" if settings.debug else None,
                  openapi_url="/docs/openapi.json" if settings.debug else None)

    init_middleware(app)

    app.include_router(router)
    return app
