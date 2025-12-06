# ML Service Homework 1

Сервис для обучения и использования ML‑моделей с REST API, HTTP Basic аутентификацией, gRPC‑сервисом и Streamlit‑дашбордом.

## 📦 Основные компоненты

- **FastAPI** REST API (`app/main.py`, `app/api.py`)
- **HTTP Basic Auth** (`app/auth.py`)
- **Менеджер моделей** с сохранением на диск (`app/models_manager.py`)
- **Конфигурация и логирование** (`app/config.py`, `app/logger.py`)
- **gRPC‑сервис** для работы с моделями (`app/gprc_service/`)
- **Streamlit‑дашборд** для взаимодействия с API (`app/dashboard/app.py`)
- **Docker** + `docker-compose` для развёртывания

Модели: `LogisticRegression`, `RandomForestClassifier` (scikit‑learn).

---

## 🧱 Структура проекта

```text
MLOPS_HW_1-updated_hw1/
├── app/
│   ├── main.py              # Точка входа FastAPI-приложения
│   ├── api.py               # REST эндпоинты для работы с моделями
│   ├── auth.py              # HTTP Basic аутентификация
│   ├── config.py            # Настройки и каталог для моделей
│   ├── logger.py            # Настройка логгера
│   ├── schemas.py           # Pydantic-схемы запросов/ответов
│   ├── models_manager.py    # Обучение, сохранение, загрузка моделей
│   ├── dashboard/
│   │   └── app.py           # Streamlit-дашборд
│   └── gprc_service/
│       ├── server.py        # gRPC сервер
│       ├── client.py        # gRPC клиент-пример
│       ├── model_service.proto
│       ├── model_service_pb2.py
│       └── model_service_pb2_grpc.py
├── data_examples/
│   ├── postman_collection.json  # Коллекция запросов для Postman
│   ├── train_example.json       # Пример данных для обучения
│   └── predict_example.json     # Пример данных для предсказаний
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## ⚙️ Зависимости

Указываются в `pyproject.toml` (Poetry):

- Python 3.10+
- fastapi, uvicorn
- scikit-learn
- pydantic, pydantic-settings
- streamlit, matplotlib
- grpcio, grpcio-tools
- pytest (dev)

---

## 🚀 Запуск сервиса (локально)

### 1. Установка зависимостей

```bash
pip install poetry
poetry install
```

### 2. Запуск REST API (FastAPI)

```bash
poetry run uvicorn app.main:app --reload --port 8000
```

По умолчанию будут доступны:

- Health-check: `GET http://127.0.0.1:8000/health`
- Документация Swagger: `http://127.0.0.1:8000/docs`

### 3. Запуск Streamlit‑дашборда

```bash
poetry run streamlit run app/dashboard/app.py
```

> Базовый URL API в дашборде задаётся константой `API_URL` в `app/dashboard/app.py`
> (по умолчанию `http://127.0.0.1:8001`). При необходимости его можно поменять на `http://127.0.0.1:8000`.

---

## 🔐 Аутентификация

Все основные эндпоинты (`/api/...`) защищены через **HTTP Basic Auth**:

Файл: `app/auth.py`

```python
from fastapi.security import HTTPBasic, HTTPBasicCredentials

def authenticate(creds: HTTPBasicCredentials = Depends(security)):
    if creds.username == "admin" and creds.password == "admin":
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")
```

По умолчанию:
- **username**: `admin`
- **password**: `admin`

Эти значения можно поменять в `auth.py`.

---

## 🌐 REST API

Базовый префикс: `/api` (см. `app/main.py` и `app/api.py`).

### 1. Health-check

```http
GET /health
```

**Ответ:**

```json
{
  "message": "OK"
}
```

### 2. Список обученных моделей

```http
GET /api/models
```

Требует Basic Auth.

**Ответ:**

```json
{
  "models": [
    "e7f1a9a2-...",
    "b3c5d8e1-..."
  ]
}
```

---

### 3. Обучение модели

Эндпоинт:  

```http
POST /api/train
```

Требует Basic Auth.

Схема запроса (`TrainRequest` из `schemas.py`):

```json
{
  "train": [
    [1.0, 2.0],
    [2.0, 3.0],
    [3.0, 4.0]
  ],
  "target": [0, 1, 0],
  "model_type": "LogisticRegression"
}
```

`model_type` — один из:

- `"LogisticRegression"`
- `"RandomForestClassifier"`

**Успешный ответ:**

```json
{
  "model_id": "e7f1a9a2-1234-5678-90ab-abcdefabcdef"
}
```

ID модели используется дальше для предсказаний и удаления.

---

### 4. Предсказание

```http
POST /api/predict/{model_id}
```

Требует Basic Auth.

Схема запроса (`PredictRequest`):

```json
{
  "data": [
    [2.0, 3.0],
    [3.0, 5.0]
  ]
}
```

**Ответ:**

```json
{
  "predictions": [0, 1]
}
```

---

### 5. Удаление модели

```http
DELETE /api/delete/{model_id}
```

Требует Basic Auth.

**Успешный ответ:**

```json
{
  "message": "deleted"
}
```

При отсутствии модели: `404 Model not found`.

---

## 🧠 Менеджер моделей

Файл: `app/models_manager.py`

Основные функции:

- `list_available_models()` — возвращает список доступных типов моделей (`AVAILABLE_MODELS`)
- `train_model(train, target, model_type)` — обучает модель и сохраняет её на диск в каталог `settings.MODELS_DIR`
- `load_model(model_id)` — загружает модель по ID
- `predict(model_id, data)` — делает предсказание и возвращает список значений
- `delete_model(model_id)` — удаляет сохранённую модель по ID

Каталог для моделей задаётся в `app/config.py`:

```python
class Settings(BaseSettings):
    MODELS_DIR: str = "models"
```

При необходимости можно переопределить через переменные окружения или `.env`.

---

## 🛰 gRPC‑сервис

Директория: `app/gprc_service/`

Файлы:

- `model_service.proto` — описание сервиса
- `model_service_pb2.py`, `model_service_pb2_grpc.py` — сгенерированный код
- `server.py` — gRPC‑сервер
- `client.py` — пример клиента

Основной сервис: `ModelService` с методами:

- `ListModels(Empty) -> ModelList`
- `TrainModel(TrainRequest) -> TrainResponse`
- `Predict(PredictRequest) -> PredictResponse`
- `DeleteModel(DeleteRequest) -> DeleteResponse`

### Запуск gRPC‑сервера

```bash
python app/gprc_service/server.py
```

По умолчанию сервер слушает порт `50051`.

### Пример клиента

```bash
python app/gprc_service/client.py
```

Клиент подключается к `localhost:50051` и запрашивает список доступных типов моделей.

---

## 📊 Streamlit‑дашборд

Файл: `app/dashboard/app.py`

Функциональность:

- форма авторизации (HTTP Basic)
- проверка `/health`
- обучение модели через `/api/train`
- просмотр списка моделей `/api/models`
- получение предсказаний `/api/predict/{model_id}`
- удаление модели `/api/delete/{model_id}`
- вывод таблиц и простых графиков (matplotlib)

Запуск:

```bash
poetry run streamlit run app/dashboard/app.py
```

---

## 🐳 Запуск через Docker

### 1. Сборка и запуск всех сервисов

```bash
docker-compose up --build
```

Файл `docker-compose.yml` поднимает:

- `api` — FastAPI на порту `8000`
- `dashboard` — Streamlit на порту `8501`

Каталог `./models` монтируется внутрь контейнера как `/app/models` для сохранения обученных моделей.

---

## 📎 Полезное

- Примеры запросов лежат в `data_examples/`:
  - `train_example.json`
  - `predict_example.json`
  - `postman_collection.json` — готовая коллекция для Postman
- Конфигурация пути к моделям — в `app/config.py`
- Логи пишутся через `app/logger.py` в стандартный вывод (StreamHandler)
