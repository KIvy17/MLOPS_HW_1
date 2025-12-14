# HW3
# Usage examples:
#   make test
#   make lint
#   make docker-push DOCKERHUB_USER=myname IMAGE_NAME=mlops-hw TAG=v1

DOCKERHUB_USER ?= your_dockerhub_username
IMAGE_NAME ?= mlops_hw
TAG ?= latest

FULL_IMAGE := $(DOCKERHUB_USER)/$(IMAGE_NAME):$(TAG)

.PHONY: test lint docker-push

docker-push:
	@echo "Building: $(FULL_IMAGE)"
	docker build -t $(FULL_IMAGE) .
	@echo "Pushing: $(FULL_IMAGE)"
	docker push $(FULL_IMAGE)

test:
	poetry run pytest -q

lint:
	# Install ruff into the current poetry venv if missing
	poetry run python -c "import ruff" 2>/dev/null || poetry run python -m pip install -q ruff==0.9.2
	poetry run ruff check .
	poetry run ruff format --check .
