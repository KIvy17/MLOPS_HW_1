import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment/.env."""

    # Local storage for models
    MODELS_DIR: str = "models"

    # S3 / Minio config for storing models and datasets
    S3_ENDPOINT_URL: str | None = None
    S3_ACCESS_KEY_ID: str | None = None
    S3_SECRET_ACCESS_KEY: str | None = None
    S3_BUCKET_MODELS: str | None = None

    # MLflow experiment tracking
    MLFLOW_TRACKING_URI: str | None = None
    MLFLOW_EXPERIMENT_NAME: str = "mlops_hw2"

    class Config:
        env_file = ".env"


settings = Settings()


def ensure_model_dir() -> None:
    """Ensure that the local directory for models exists."""
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
