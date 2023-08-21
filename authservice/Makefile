.PHONY: start-local
start-local:
	docker-compose -f docker-compose-local.yaml -p auth-service-local up --build -d

.PHONY: start-prod
start-prod:
	docker-compose -f docker-compose-prod.yaml -p auth-service-prod up --build -d


.PHONY: down-all
down-all:
	docker-compose -f docker-compose-local.yaml -p auth-service-local down
	docker-compose -f docker-compose-prod.yaml -p auth-service-prod down

