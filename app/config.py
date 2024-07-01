import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MODEL_DIR: str
    MODEL_PATH: str
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR: str = os.path.join(BASE_DIR, "app")
    LOG_DIR: str = os.path.join(APP_DIR, "logs")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
