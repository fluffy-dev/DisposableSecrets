from fastapi import APIRouter
from src.secrets.router import router as secrets_router

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(secrets_router)