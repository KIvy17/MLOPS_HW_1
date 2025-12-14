import os
import uuid

import pytest

from app import models_manager as mm
from app.config import settings


@pytest.mark.filterwarnings("ignore:.*ConvergenceWarning.*")
def test_train_model_uploads_to_s3_when_client_is_mocked(
    temp_models_dir, mock_s3, monkeypatch
):
    """Example unit-test with mocked S3 via fixture."""

    # Make model id deterministic
    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    monkeypatch.setattr(mm.uuid, "uuid4", lambda: fixed_uuid)
    monkeypatch.setattr(settings, "MLFLOW_TRACKING_URI", None, raising=True)

    train = [[0.0, 0.0], [1.0, 1.0], [1.0, 0.0], [0.0, 1.0]]
    target = [0, 1, 1, 0]

    model_id = mm.train_model(
        train=train, target=target, model_type="LogisticRegression"
    )
    assert model_id == str(fixed_uuid)

    local_path = os.path.join(settings.MODELS_DIR, f"{model_id}.pkl")
    assert os.path.exists(local_path)

    # S3 upload is performed through our fake client
    assert mock_s3.upload_calls == [
        (local_path, "test-bucket", f"models/{model_id}.pkl")
    ]


def test_list_trained_models_returns_only_pkl_files(temp_models_dir):
    """Example of a regular unit-test (no S3 involved)."""

    (temp_models_dir / "a.pkl").write_bytes(b"x")
    (temp_models_dir / "b.pkl").write_bytes(b"x")
    (temp_models_dir / "notes.txt").write_text("ignore")

    models = mm.list_trained_models()
    assert set(models) == {"a", "b"}
