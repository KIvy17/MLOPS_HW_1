import os
import pickle
import uuid
from typing import List, Any, Optional

import boto3
import mlflow
from mlflow import sklearn as mlflow_sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from app.logger import get_logger
from app.config import settings, ensure_model_dir

logger = get_logger()

AVAILABLE_MODELS = {
    "LogisticRegression": LogisticRegression,
    "RandomForestClassifier": RandomForestClassifier,
}


def _get_s3_client() -> Optional["boto3.client"]:
    """Create S3/Minio client if configuration is provided."""
    if (
        not settings.S3_ENDPOINT_URL
        or not settings.S3_ACCESS_KEY_ID
        or not settings.S3_SECRET_ACCESS_KEY
    ):
        return None

    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
    )


def _upload_model_to_s3(local_path: str, model_id: str) -> None:
    client = _get_s3_client()
    bucket = settings.S3_BUCKET_MODELS
    if not client or not bucket:
        return

    key = f"models/{model_id}.pkl"
    try:
        client.upload_file(local_path, bucket, key)
        logger.info(f"Model {model_id} uploaded to S3 bucket '{bucket}' as '{key}'")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Failed to upload model {model_id} to S3: {exc}")


def _download_model_from_s3(local_path: str, model_id: str) -> bool:
    client = _get_s3_client()
    bucket = settings.S3_BUCKET_MODELS
    if not client or not bucket:
        return False

    key = f"models/{model_id}.pkl"
    try:
        client.download_file(bucket, key, local_path)
        logger.info(f"Model {model_id} downloaded from S3 bucket '{bucket}'")
        return True
    except Exception:
        return False


def _setup_mlflow() -> None:
    """Configure MLflow tracking if URI is provided."""
    if not settings.MLFLOW_TRACKING_URI:
        return

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)


def train_model(train: List[List[float]], target: List[int], model_type: str) -> str:
    """Train model of given type, save locally and (optionally) to S3 & MLflow."""
    ensure_model_dir()

    if model_type not in AVAILABLE_MODELS:
        raise ValueError("Unknown model type")

    ModelCls = AVAILABLE_MODELS[model_type]

    _setup_mlflow()

    if settings.MLFLOW_TRACKING_URI:
        with mlflow.start_run(run_name=f"train_{model_type}"):
            model = ModelCls()
            model.fit(train, target)

            mlflow.log_param("model_type", model_type)
            mlflow.log_param("n_samples", len(train))

            # Log model to MLflow
            mlflow_sklearn.log_model(model, artifact_path="model")

            model_id = str(uuid.uuid4())
            path = os.path.join(settings.MODELS_DIR, f"{model_id}.pkl")
            with open(path, "wb") as f:
                pickle.dump(model, f)

            _upload_model_to_s3(path, model_id)

            logger.info(f"Model trained and saved: {model_id}")
            return model_id
    else:
        # No MLflow configured – just train and save
        model = ModelCls()
        model.fit(train, target)

        model_id = str(uuid.uuid4())
        path = os.path.join(settings.MODELS_DIR, f"{model_id}.pkl")
        with open(path, "wb") as f:
            pickle.dump(model, f)

        _upload_model_to_s3(path, model_id)

        logger.info(f"Model trained and saved: {model_id}")
        return model_id


def list_trained_models() -> List[str]:
    """List locally stored models by ID."""
    ensure_model_dir()
    return [
        f.split(".")[0] for f in os.listdir(settings.MODELS_DIR) if f.endswith(".pkl")
    ]


def predict(model_id: str, data: List[List[float]]) -> List[Any]:
    """Load model (locally or from S3) and get predictions."""
    ensure_model_dir()
    path = os.path.join(settings.MODELS_DIR, f"{model_id}.pkl")

    if not os.path.exists(path):
        downloaded = _download_model_from_s3(path, model_id)
        if not downloaded:
            raise ValueError("Model not found")

    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        raise ValueError("Model not found")

    return model.predict(data).tolist()


def delete_model(model_id: str) -> bool:
    """Delete local model file. S3 cleanup is optional and not required for HW2."""
    ensure_model_dir()
    path = os.path.join(settings.MODELS_DIR, f"{model_id}.pkl")
    try:
        os.remove(path)
        logger.info(f"Model deleted: {model_id}")
        return True
    except FileNotFoundError:
        return False
