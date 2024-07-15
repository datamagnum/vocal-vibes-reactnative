l.DEFAULT_GOAL=help
COMPOSE_DEPS_FILES = -f infra/local/docker-compose.yaml

start-deps: # Starts dependencies
	docker-compose $(COMPOSE_DEPS_FILES) up -d

stop-deps: # Stops dependencies
	@docker-compose $(COMPOSE_DEPS_FILES) stop


create-database: # Create Database
	python ./migrations/create_database.py

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'