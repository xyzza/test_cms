.PHONY: run migrate db build lint test
.DEFAULT_GOAL := test_compose


run:
	@echo "running..."
	@uvicorn app:server --reload --port 8080

migrate:
	@yoyo apply -d ${DB_DSN}

db:
	@docker-compose up -d db

build:
	@echo "building..."
	@docker-compose build app

test_compose:
	@docker-compose up --build

test_local: lint
	@echo "testing..."
	@pytest -sv

sort:
	@isort .

lint:
	@echo "checking linters..."
	@flake8