# ML Service Homework 1

REST API for ML models management.

## Team Members

* Kovalenok I.
* Astashkin A.

## Description

Basic REST API service for training and using ML models (LogisticRegression, RandomForestClassifier).

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

pip install fastapi uvicorn scikit-learn pandas pydantic loguru
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

## API Endpoints

- `GET /health` - check service status
- `GET /models` - list available models
- `POST /train` - train model
- `POST /predict/{model_id}` - make prediction
- `DELETE /delete/{model_id}` - delete model

## Examples

Example data for training and prediction are in `data_examples/` folder.

## Project Structure

```
├── app/
│   ├── main.py              # FastAPI application
│   ├── models_manager.py    # ML models manager
│   ├── logger.py            # Logging
│   └── schemas.py           # Pydantic schemas
├── data_examples/           # Example data
└── pyproject.toml           # Dependencies
```
