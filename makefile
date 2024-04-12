# Run | Clean

run:
	poe --root backend run

clean:
	poe --root backend clean


# Total checking and testing

check:
	poe --root backend check_all


# Testing

test:
	poe --root backend test

test_unit:
	poe --root backend test_unit

test_integration:
	poe --root backend test_integration

test_e2e:
	poe --root backend test_e2e

test_domain:
	poe --root backend test_domain

test_application:
	poe --root backend test_application

test_infra:
	poe --root backend test_infra

test_coverage:
	poe --root backend test_coverage

# Linting, Formatting, and Type Checking

format:
	poe --root backend format

lint:
	poe --root backend lint

check_types:
	poe --root backend check_types


# # Migrations

migrations:
	poe --root backend makemigrations

migrate:
	poe --root backend migrate
