# MLOps Homework 3 (HW3)

Branch: `hw3`

This repository contains **Homework 3** for the MLOps course.  
It is based on the application from **Homework 2** and adds:

- Unit tests (pytest)
- Mocked S3 interactions (via pytest fixture)
- Makefile with required commands:
  - build + push Docker image to DockerHub
  - run tests
  - run linters

---

## Unit tests

Tests are located in `tests/`:

- `tests/conftest.py`
  - adds project root to `PYTHONPATH` for imports
  - provides S3 mock fixture (FakeS3Client)
  - provides temp models directory fixture
- `tests/test_models_manager.py`
  - test with mocked S3 upload
  - regular unit test (no S3)

Run tests:
```bash
make test
```

Or directly:
```bash
poetry run pytest
```

---

## Linters

Project uses **ruff** for linting and formatting checks.

Run linters:
```bash
make lint
```

If formatting is required, run:
```bash
poetry run ruff format .
```
and then re-check:
```bash
make lint
```

---

## Makefile

`Makefile` is located in the repository root and provides:

- `make test` — run unit tests
- `make lint` — run linters (ruff)
- `make docker-push` — build Docker image and push it to DockerHub

---

## Docker (build + push)

Docker image is built locally and pushed to DockerHub.

DockerHub username used:
```
astrifrf
```

Image and tag:
```
astrifrf/mlops-hw:hw3
```

Login (one time):
```bash
docker login
```

Build + push (command used):
```bash
make docker-push DOCKERHUB_USER=astrifrf IMAGE_NAME=mlops-hw TAG=hw3
```

After push the image should appear in DockerHub as:
```
astrifrf/mlops-hw:hw3
```

---

## Full verification checklist

From repository root:
```bash
poetry install --with dev
make test
make lint
make docker-push DOCKERHUB_USER=astrifrf(ваш юзернейм) IMAGE_NAME=mlops-hw(ваш) TAG=hw3(ваш)
```

---

## Project structure

```
.
├── app/
├── tests/
│   ├── conftest.py
│   └── test_models_manager.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

