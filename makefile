# Variables

DEFAULT_COLOR = \e[0m

BLUE = \e[34m

YELLOW = \033[33m

DOCKER_CONTAINER_NAME = api


# Functions

define docker_exec
	docker exec -it ${DOCKER_CONTAINER_NAME} bash -c "$(1)"
endef

define docker_row_exec
	docker exec ${DOCKER_CONTAINER_NAME} bash -c "$(1)"
endef


# Run

run:
	docker compose up --build

restart:
	docker compose down
	docker compose up --build -d

down:
	docker compose down

clean:
	docker compose down -v


# Migrations

migrations:
	$(call docker_exec,poetry run alembic revision --autogenerate)

migrate:
	$(call docker_exec,poetry run alembic upgrade head)

migrate-in-container:
	poetry run alembic upgrade head


# Formatting | Lint | Typing

black:
	poetry run black . -l 79 tests src

lint:
	poetry run flake8 --config setup.cfg src tests

typechecks:
	poetry run mypy --config setup.cfg src tests


# Unit Tests

unittests-auth:
	poetry run pytest -s -v tests/auth/domain tests/auth/application

unittests-shared:
	poetry run pytest -s -v tests/shared/domain tests/shared/application

unittests: unittests-shared unittests-auth

# Integration Tests

integration_tests-auth:
	$(call docker_exec,cd tests/auth/infra && poetry run pytest -s -vv .)

integration_tests-shared:
	$(call docker_exec,cd tests/shared/infra && poetry run pytest -s -vv .)

integration_tests:
	$(call docker_exec,\
	    cd tests/shared/infra && poetry run pytest -s -vv . && \
	    cd ../../../ && \
	    cd tests/auth/infra && poetry run pytest -s -vv .\
	)


# End To End Tests

e2e_tests-auth:
	$(call docker_exec,cd tests/auth/presentation && poetry run pytest -s -vv .)

e2e_tests: e2e_tests-auth


test: lint typechecks unittests integration_tests e2e_tests
