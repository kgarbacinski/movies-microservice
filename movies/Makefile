.PHONY: start-local
start-local:
	docker-compose -f docker-compose-local.yaml -p movies-local up --build -d

.PHONY: start-prod
start-prod:
	docker-compose -f docker-compose-prod.yaml -p movies-prod up --build -d


.PHONY: down-all
down-all:
	docker-compose -f docker-compose-local.yaml -p movies-local down
	docker-compose -f docker-compose-prod.yaml -p movies-prod down

.PHONY: tests
test:
	docker build -t docker-movies-test .
	docker run --rm docker-movies-test python -m pytest
