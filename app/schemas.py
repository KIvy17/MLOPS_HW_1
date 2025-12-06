from pydantic import BaseModel
from typing import List

class TrainRequest(BaseModel):
    train: List[List[float]]
    target: List[int]
    model_type: str

class PredictRequest(BaseModel):
    data: List[List[float]]

class Message(BaseModel):
    message: str
