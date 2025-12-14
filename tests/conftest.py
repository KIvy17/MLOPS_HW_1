# ruff: noqa: E402


import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pytest

from app.config import settings


class FakeS3Client:
    """Very small fake S3 client for unit tests."""

    def __init__(self) -> None:
        self.upload_calls: list[tuple[str, str, str]] = []
        self.download_calls: list[tuple[str, str, str]] = []

    def upload_file(self, filename: str, bucket: str, key: str) -> None:
        self.upload_calls.append((filename, bucket, key))

    def download_file(self, bucket: str, key: str, filename: str) -> None:
        self.download_calls.append((bucket, key, filename))


@pytest.fixture()
def temp_models_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Put models into a temp directory so tests don't touch real FS."""
    models_dir = tmp_path / "models"
    monkeypatch.setattr(settings, "MODELS_DIR", str(models_dir), raising=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    return models_dir


@pytest.fixture()
def mock_s3(monkeypatch: pytest.MonkeyPatch) -> FakeS3Client:
    """Mock S3 client via fixture (HW3 requirement)."""
    from app import models_manager as mm

    fake = FakeS3Client()
    monkeypatch.setattr(mm, "_get_s3_client", lambda: fake)
    monkeypatch.setattr(settings, "S3_BUCKET_MODELS", "test-bucket", raising=True)
    return fake
