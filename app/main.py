from fastapi import FastAPI
from app.api import router as api_router
from app.schemas import Message

app = FastAPI(title="Fixed ML API")


@app.get("/health", response_model=Message)
async def health():
    return {"message": "OK"}


app.include_router(api_router, prefix="/api")
