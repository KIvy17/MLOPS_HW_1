import pickle
import os
import uuid
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from app.logger import get_logger

logger = get_logger()

AVAILABLE_MODELS = {
    "LogisticRegression": LogisticRegression,
    "RandomForestClassifier": RandomForestClassifier,
}

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def list_available_models():
    """Возвращает названия моделей, которые можно обучить."""
    return list(AVAILABLE_MODELS.keys())

def train_model(model_type, X, y, params):
    """Обучает модель и сохраняет в файл. Возвращает UUID модели."""
    if model_type not in AVAILABLE_MODELS:
        raise ValueError("Неизвестный тип модели")
    model = AVAILABLE_MODELS[model_type](**params)
    model.fit(X, y)
    model_id = str(uuid.uuid4())
    with open(f"{MODEL_DIR}/{model_id}.pkl", "wb") as f:
        pickle.dump(model, f)
    logger.info(f"Модель {model_type} обучена и сохранена, id={model_id}")
    return model_id

def predict(model_id, X):
    """Загружает модель и делает предсказания."""
    path = f"{MODEL_DIR}/{model_id}.pkl"
    if not os.path.exists(path):
        raise ValueError("Модель не найдена")
    with open(path, "rb") as f:
        model = pickle.load(f)
    preds = model.predict(X)
    return preds.tolist()

def delete_model(model_id):
    """Удаляет файл модели. Возвращает True если удалено, False если не найдено."""
    path = f"{MODEL_DIR}/{model_id}.pkl"
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Модель {model_id} удалена")
        return True
    return False
