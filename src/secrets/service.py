from uuid import uuid4
from src.cache.client import IClient
from src.secrets.entities import SecretEntity, SecretLogEntity
from src.secrets.dependencies import ISecretRepository
from src.secrets.settings import secrets_settings
from src.secrets.exceptions import SecretNotFound, InvalidPassphrase
from src.secrets.dto import SecretCreateDTO, SecretDeleteDTO
from src.secrets.security import get_fernet

class SecretService:
    def __init__(self, cache_client: IClient, repository: ISecretRepository):
        self.cache_client = cache_client
        self.repository = repository

    async def create_secret(self, secret_data: SecretCreateDTO, ip_address: str) -> SecretEntity:
        """Create a new secret and log the action."""
        fernet = get_fernet()
        encrypted_secret = fernet.encrypt(secret_data.secret.encode()).decode()
        secret_key = uuid4()
        ttl = max(secret_data.ttl_seconds, secrets_settings.MIN_TTL_SECONDS)

        secret = SecretEntity(
            key=secret_key,
            value=encrypted_secret,
            passphrase=secret_data.passphrase,
            ttl_seconds=ttl
        )
        await self.cache_client.set(str(secret.key), secret.value, expire=ttl)

        log = SecretLogEntity(
            secret_key=str(secret.key),
            action="create",
            ip_address=ip_address,
            ttl_seconds=ttl,
            passphrase_used=secret.passphrase
        )
        await self.repository.log_action(log)
        return secret

    async def get_secret(self, secret_key: str, ip_address: str) -> str:
        """Retrieve and delete a secret, logging the action."""
        encrypted_secret = await self.cache_client.get_and_delete(secret_key)
        if not encrypted_secret:
            raise SecretNotFound()

        fernet = get_fernet()
        secret_value = fernet.decrypt(encrypted_secret.encode()).decode()

        log = SecretLogEntity(
            secret_key=secret_key,
            action="read",
            ip_address=ip_address,
            ttl_seconds=None,
            passphrase_used=None
        )
        await self.repository.log_action(log)
        return secret_value

    async def delete_secret(self, secret_key: str, delete_data: SecretDeleteDTO, ip_address: str) -> None:
        """Delete a secret with passphrase validation, logging the action."""
        encrypted_secret = await self.cache_client.get_and_delete(secret_key)
        if not encrypted_secret:
            raise SecretNotFound()

        create_log = await self.repository.get_create_log(secret_key)
        if create_log and create_log.passphrase_used and create_log.passphrase_used != delete_data.passphrase:
            raise InvalidPassphrase()

        log = SecretLogEntity(
            secret_key=secret_key,
            action="delete",
            ip_address=ip_address,
            passphrase_used=delete_data.passphrase,
            ttl_seconds=None,
        )
        await self.repository.log_action(log)