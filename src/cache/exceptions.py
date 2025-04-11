from fastapi import HTTPException

class CacheConnectionError(HTTPException):
    def __init__(self, detail: str = "Cache connection failed"):
        super().__init__(status_code=503, detail=detail)