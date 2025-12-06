# HW2 additions

- Added Minio + MLflow + app to docker-compose.yml
- Added S3 (Minio) integration for model storage
- Added MLflow tracking integration in app/models_manager.py
- Added basic DVC config (.dvc/config, data.dvc, data/)

## How to run

1. Build and run all services:

```bash
docker-compose up --build
```

2. Open:
   - Minio console: http://localhost:9001 (login: minio / minio12345)
   - MLflow UI: http://localhost:5000
   - FastAPI docs: http://localhost:8000/docs

3. In Minio console create buckets:
   - mlops-hw2-dvc
   - mlops-hw2-models
   - mlflow-artifacts

4. Put your training data into `data/`, track with DVC if needed:

```bash
dvc add data
dvc push
```

5. Use FastAPI endpoints to train and predict.
