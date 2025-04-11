from fastapi import Depends, Request
from typing import Annotated

from src.secrets.repository import SecretRepository
from src.secrets.service import SecretService

ISecretRepository = Annotated[SecretRepository, Depends()]
ISecretService = Annotated[SecretService, Depends()]
