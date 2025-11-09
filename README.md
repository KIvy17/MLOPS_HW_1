# ML Service Homework 1

REST API for ML models management with JWT authentication.

## Team Members

* Kovalenok I.
* Astashkin A.

## Description

REST API service for training and using ML models (LogisticRegression, RandomForestClassifier) with JWT token authentication.

## Requirements

- Python 3.10+
- pip

## Installation

```bash
git clone https://github.com/KIvy17/MLOPS_HW_1.git
cd MLOPS_HW_1
git checkout dev

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install fastapi uvicorn scikit-learn pandas pydantic loguru pyjwt
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Check

```bash
curl http://127.0.0.1:8000/health
```

Swagger docs: http://127.0.0.1:8000/docs

## JWT Authentication

All endpoints (except `/health` and `/token`) require JWT token.

### Get token:
```bash
curl -X POST "http://127.0.0.1:8000/token?username=admin&password=password"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Use token:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/models
```

## API Endpoints

- `GET /health` - check service status (no token required)
- `POST /token` - get JWT token (no token required)
- `GET /models` - list available models (token required)
- `POST /train` - train model (token required)
- `POST /predict/{model_id}` - make prediction (token required)
- `DELETE /delete/{model_id}` - delete model (token required)

## Usage Examples

### 1. Get token
```bash
curl -X POST "http://127.0.0.1:8000/token?username=admin&password=password"
```

### 2. List models
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/models
```

### 3. Train model
```bash
curl -X POST http://127.0.0.1:8000/train \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @data_examples/train_example.json
```

### 4. Predict
```bash
curl -X POST http://127.0.0.1:8000/predict/MODEL_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @data_examples/predict_example.json
```

## Data Examples

Example JSON files for training and prediction are in `data_examples/` folder.

## Project Structure

```
├── app/
│   ├── main.py              # FastAPI application with JWT
│   ├── auth.py              # JWT authentication
│   ├── models_manager.py    # ML models manager
│   ├── logger.py            # Logging
│   └── schemas.py           # Pydantic schemas
├── data_examples/           # Example data
└── pyproject.toml           # Dependencies
```

## Note

Current version includes basic REST API and JWT authentication (Kovalenok I.). 
Additional components (gRPC, Streamlit, Docker) will be added in next commits.
