from cryptography.fernet import Fernet
from src.secrets.settings import secrets_settings

def get_fernet() -> Fernet:
    return Fernet(secrets_settings.ENCRYPTION_KEY.encode())