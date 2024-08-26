DC = docker-compose
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
EXEC = docker exec -it
LOGS = docker logs
ENV_FILE = --env-file .env
APP_CONTAINER = app-drf-authentication
INTO_BASH = /bin/bash
RUN_MIGRATION = poetry run alembic upgrade b85ad2740d7d
ENTER_POSTGRES_CONTAINER = psql -U postgres -d calendar


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: appbash
appbash:
	${EXEC} ${APP_CONTAINER} ${INTO_BASH}
