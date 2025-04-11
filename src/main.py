import uvicorn
from src.app import get_app
from src.settings import settings as main_settings

app = get_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host=main_settings.host, port=main_settings.port, reload=main_settings.debug)
