from pydantic import BaseModel
from typing import List, Any, Dict

class TrainRequest(BaseModel):
    model_type: str
    X: List[List[float]]
    y: List[int]
    params: Dict[str, Any] = {}

class PredictRequest(BaseModel):
    X: List[List[float]]

class Message(BaseModel):
    message: str
