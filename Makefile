.PHONY: install test lint run image up down status smoke stack-test validate

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

test:
	.venv/bin/python -m pytest

lint:
	.venv/bin/ruff check app tests
	.venv/bin/ruff format --check app tests

run:
	.venv/bin/uvicorn app.main:app --reload

image:
	docker build -t factory-api:local .

up:
	docker compose up --build -d

down:
	docker compose down

status:
	docker compose ps

smoke:
	./scripts/smoke-test.sh http://127.0.0.1:8000

stack-test:
	./scripts/stack-test.sh

validate:
	./scripts/validate.sh
