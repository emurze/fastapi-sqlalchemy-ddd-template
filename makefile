# Run | Clean

run-backend:
	poe --root backend run

clean-backend:
	poe --root backend clean


# Total checking and testing

check-backend:
	poe --root backend check_all


# Testing

test-backend:
	poe --root backend test

test_unit-backend:
	poe --root backend test_unit

test_integration-backend:
	poe --root backend test_integration

test_e2e-backend:
	poe --root backend test_e2e

test_coverage-backend:
	poe --root backend test_coverage

# Linting, Formatting, and Type Checking

format-backend:
	poe --root backend format

lint-backend:
	poe --root backend lint

check_types-backend:
	poe --root backend lint


# # Migrations

migrations-backend:
	poe --root backend makemigrations

migrate-backend:
	poe --root backend migrate
