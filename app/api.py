
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TrainRequest, PredictRequest, Message
from app.models_manager import train_model, predict, delete_model, list_trained_models
from app.auth import authenticate

router = APIRouter()

@router.get("/models", dependencies=[Depends(authenticate)])
async def models_list():
    return {"models": list_trained_models()}

@router.post("/train", dependencies=[Depends(authenticate)])
async def train(req: TrainRequest):
    try:
        model_id = train_model(req.train, req.target, req.model_type)
        return {"model_id": model_id}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/predict/{model_id}", dependencies=[Depends(authenticate)])
async def do_predict(model_id: str, req: PredictRequest):
    try:
        preds = predict(model_id, req.data)
        return {"predictions": preds}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.delete("/delete/{model_id}", dependencies=[Depends(authenticate)])
async def delete(model_id: str):
    if delete_model(model_id):
        return {"message": "deleted"}
    raise HTTPException(404, "Model not found")
