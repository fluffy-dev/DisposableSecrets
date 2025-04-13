from fastapi import Depends
from typing import Annotated

from src.secrets.repository import SecretRepository
ISecretRepository = Annotated[SecretRepository, Depends()]


from src.secrets.service import SecretService
ISecretService = Annotated[SecretService, Depends()]
