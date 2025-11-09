from fastapi import FastAPI, HTTPException
from app.schemas import TrainRequest, PredictRequest, Message
from app.models_manager import list_available_models, train_model, predict, delete_model
from app.logger import get_logger

logger = get_logger()

app = FastAPI(title="ML Service API", description="REST API for ML model management")

@app.get("/health", response_model=Message)
def health():
    """Проверяет, что сервис работает."""
    return {"message": "Сервис работает"}

@app.get("/models")
def get_models():
    """Возвращает список типов моделей, которые можно обучить."""
    return {"available_models": list_available_models()}

@app.post("/train")
def train(req: TrainRequest):
    """Обучает модель на переданных данных и сохраняет ее. Возвращает ID модели."""
    try:
        model_id = train_model(req.model_type, req.X, req.y, req.params)
        return {"message": "Модель обучена", "model_id": model_id}
    except Exception as e:
        logger.error(f"Ошибка при обучении: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/{model_id}")
def make_prediction(model_id: str, req: PredictRequest):
    """Делает предсказания с помощью обученной модели по ее ID."""
    try:
        preds = predict(model_id, req.X)
        return {"predictions": preds}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete/{model_id}")
def remove_model(model_id: str):
    """Удаляет модель с диска по ее ID."""
    if delete_model(model_id):
        return {"message": "Модель удалена"}
    raise HTTPException(status_code=404, detail="Модель не найдена")
