.PHONY: start-local
start-local:
	docker-compose -f docker-compose-prod.yaml -p apigateway-prod down
	docker-compose -f docker-compose-local.yaml -p apigateway-local up --build -d

.PHONY: start-prod
start-prod:
	docker-compose -f docker-compose-local.yaml -p apigateway-local down
	docker-compose -f docker-compose-prod.yaml -p apigateway-prod up --build


.PHONY: down-all
down-all:
	docker-compose -f docker-compose-local.yaml -p apigateway-local down
	docker-compose -f docker-compose-prod.yaml -p apigateway-prod down

.PHONY: tests
test:
	docker build -t docker-apigateway-test .
	docker run --rm docker-apigateway-test python -m pytest
