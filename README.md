# ML Service Homework 1

REST API для управления ML-моделями с JWT аутентификацией.

## Состав группы

* Ковалёнок И.
* Асташкин А.

## Описание

REST API сервис для обучения и использования ML-моделей (LogisticRegression, RandomForestClassifier) с защитой эндпоинтов через JWT токены.

## Требования

- Python 3.10+
- pip

## Установка и запуск

### Шаг 1: Клонирование
```bash
git clone https://github.com/KIvy17/MLOPS_HW_1.git
cd MLOPS_HW_1
git checkout dev
```

### Шаг 2: Установка зависимостей
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install fastapi uvicorn scikit-learn pandas pydantic loguru pyjwt
```

### Шаг 3: Запуск
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Проверка

```bash
curl http://127.0.0.1:8000/health
```

Swagger документация: http://127.0.0.1:8000/docs

## JWT Аутентификация

Все эндпоинты (кроме `/health` и `/token`) требуют JWT токен.

### Получение токена:
```bash
curl -X POST "http://127.0.0.1:8000/token?username=admin&password=password"
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Использование токена:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/models
```

## API Эндпоинты

- `GET /health` - проверка статуса сервиса (без токена)
- `POST /token` - получение JWT токена (без токена)
- `GET /models` - список доступных моделей (требует токен)
- `POST /train` - обучение модели (требует токен)
- `POST /predict/{model_id}` - предсказание (требует токен)
- `DELETE /delete/{model_id}` - удаление модели (требует токен)

## Примеры использования

### 1. Получить токен
```bash
curl -X POST "http://127.0.0.1:8000/token?username=admin&password=password"
```

### 2. Список моделей
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/models
```

### 3. Обучить модель
```bash
curl -X POST http://127.0.0.1:8000/train \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @data_examples/train_example.json
```

### 4. Предсказание
```bash
curl -X POST http://127.0.0.1:8000/predict/MODEL_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @data_examples/predict_example.json
```

## Примеры данных

В папке `data_examples/` находятся примеры JSON для обучения и предсказания.

# Streamlit
streamlit run app/dashboard/app.py
## gRPC
1) Сгенерировать Python-код из .proto (один раз):
python -m grpc_tools.protoc -I app/grpc_service       --python_out=app/grpc_service       --grpc_python_out=app/grpc_service       app/grpc_service/model_service.proto
2) Запустить сервер:
python -m app.grpc_service.server
3) Клиент (пример):
python -m app.grpc_service.client
## Docker
docker-compose up --build
Доступ:
- API: http://localhost:8000/health
- Dashboard: http://localhost:8501


## Структура проекта

```
├── app/
│   ├── main.py              # FastAPI приложение с JWT
│   ├── auth.py              # JWT аутентификация
│   ├── models_manager.py    # Менеджер ML моделей
│   ├── logger.py            # Логирование
│   └── schemas.py           # Pydantic схемы
├── data_examples/           # Примеры данных
└── pyproject.toml           # Зависимости
```

## Примечание

Текущая версия включает базовый REST API и JWT аутентификацию (Ковалёнок И.). 
Дополнительные компоненты (gRPC, Streamlit, Docker) добавлены (Асташикн А.)

