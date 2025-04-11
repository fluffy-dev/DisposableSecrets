from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional

from src.database.base_model import Base

class SecretLogModel(Base):
    __tablename__ = "secret_logs"

    secret_key: Mapped[str] = mapped_column(String, index=True)
    action: Mapped[str] = mapped_column(String)
    ip_address: Mapped[str] = mapped_column(String)
    ttl_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passphrase_used: Mapped[Optional[str]] = mapped_column(String, nullable=True)