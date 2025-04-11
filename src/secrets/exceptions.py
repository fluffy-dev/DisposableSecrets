from fastapi import HTTPException

class SecretNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Secret not found")

class InvalidPassphrase(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Invalid passphrase")