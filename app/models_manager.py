import pickle
import uuid
from typing import List, Any

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from app.logger import get_logger
from app.config import settings, ensure_model_dir

logger = get_logger()

AVAILABLE_MODELS = {
    "LogisticRegression": LogisticRegression,
    "RandomForestClassifier": RandomForestClassifier,
}

def train_model(train: List[List[float]], target: List[int], model_type: str) -> str:
    ensure_model_dir()

    if model_type not in AVAILABLE_MODELS:
        raise ValueError("Unknown model type")

    model = AVAILABLE_MODELS[model_type]()
    model.fit(train, target)

    model_id = str(uuid.uuid4())
    path = f"{settings.MODELS_DIR}/{model_id}.pkl"

    with open(path, "wb") as f:
        pickle.dump(model, f)

    logger.info(f"Model saved: {model_id}")
    return model_id

def list_trained_models() -> List[str]:
    import os
    ensure_model_dir()
    return [f.split(".")[0] for f in os.listdir(settings.MODELS_DIR) if f.endswith(".pkl")]

def predict(model_id: str, data: List[List[float]]) -> List[Any]:
    ensure_model_dir()
    path = f"{settings.MODELS_DIR}/{model_id}.pkl"

    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
    except FileNotFoundError:
        raise ValueError("Model not found")

    return model.predict(data).tolist()

def delete_model(model_id: str) -> bool:
    import os
    ensure_model_dir()
    path = f"{settings.MODELS_DIR}/{model_id}.pkl"
    try:
        os.remove(path)
        logger.info(f"Model deleted: {model_id}")
        return True
    except FileNotFoundError:
        return False
