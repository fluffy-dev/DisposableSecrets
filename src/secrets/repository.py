from typing import Optional

from sqlalchemy import select
from src.secrets.entities import SecretLogEntity
from src.secrets.models import SecretLogModel
from src.secrets.dto import SecretLogDTO

from src.database.session import ISession


class SecretRepository:
    def __init__(self, session: ISession):
        self.session = session

    async def log_action(self, log: SecretLogEntity) -> SecretLogDTO:
        """Log an action to the database."""
        instance = SecretLogModel(**log.__dict__)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return await self._get_dto(instance)

    async def get_create_log(self, secret_key: str) -> Optional[SecretLogDTO]:
        """Retrieve the creation log for a secret."""
        query = select(SecretLogModel).where(
            SecretLogModel.secret_key == secret_key,
            SecretLogModel.action == "create"
        )
        result = await self.session.execute(query)
        instance = result.scalar_one_or_none()
        return await self._get_dto(instance)

    async def _get_dto(self, row: SecretLogModel) -> SecretLogDTO:
        return SecretLogDTO(
            id=row.id,
            secret_key=row.secret_key,
            action=row.action,
            ip_address=row.ip_address,
            ttl_seconds=row.ttl_seconds,
            passphrase_used=row.passphrase_used
        )