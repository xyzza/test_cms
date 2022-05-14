.PHONY: run migrate db build lint test
.DEFAULT_GOAL := build


run:
	@echo "running..."
	@uvicorn app:server --reload --port 8080

migrate:
	@yoyo apply -d ${DB_DSN}

db:
	@docker-compose -f ci-cd/docker-compose.yml up -d db

build:
	@echo "building..."
	@docker-compose -f ci-cd/docker-compose.yml build app

test:
	@echo "testing..."


# TODO: isort, flake
