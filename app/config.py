import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODELS_DIR: str = "models"

    class Config:
        env_file = ".env"

settings = Settings()

def ensure_model_dir():
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
