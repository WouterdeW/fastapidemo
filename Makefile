SHELL = /bin/bash

all: up init-db init-schema

build:
	docker build -t fastapidemo:latest .

up: ## Starts docker-compose setup
	docker-compose up -d

down: ## Stops docker-compose setup
	docker-compose down

clean: ## Stop docker-compose setup and delete all volumes
	docker-compose down --volumes --remove-orphans

init-db: up ## Initialize database
	@while ! docker ps --no-trunc --filter "label=com.docker.compose.service=db" | grep -q 'healthy'; do echo "initializing PostgreSQL.."; sleep 15; done
	docker-compose exec -T db psql -h localhost -U postgres -f /tmp/sql/init-db.sql

init-schema: up init-db
	docker-compose exec -T db psql --dbname=demo --username=demo -f /tmp/sql/init-schema.sql

test:
	pytest -s -v tests