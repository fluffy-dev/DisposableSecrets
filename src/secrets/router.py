from fastapi import APIRouter, Response, Request
from src.secrets.dependencies import ISecretService
from src.secrets.dto import (
    SecretCreateDTO, SecretResponseDTO, SecretRetrieveDTO,
    SecretDeleteDTO, DeleteResponseDTO
)

router = APIRouter(prefix="/secrets", tags=["secrets"])

@router.post("/secret", response_model=SecretResponseDTO, status_code=201)
async def create_secret(secret_data: SecretCreateDTO, service: ISecretService, response: Response, request: Request):
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    ip_address = request.client.host
    secret = await service.create_secret(secret_data, ip_address)
    return {"secret_key": secret.key}

@router.get("/secret/{secret_key}", response_model=SecretRetrieveDTO)
async def get_secret(
    secret_key: str,
    service: ISecretService,
    response: Response,
    request: Request
):
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    ip_address = request.client.host
    secret_value = await service.get_secret(secret_key, ip_address)
    return {"secret": secret_value}

@router.delete("/secret/{secret_key}", response_model=DeleteResponseDTO)
async def delete_secret(
    secret_key: str,
    delete_data: SecretDeleteDTO,
    service: ISecretService,
    response: Response,
    request: Request,
):

    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    ip_address = request.client.host
    await service.delete_secret(secret_key, delete_data, ip_address)
    return {"status": "secret_deleted"}