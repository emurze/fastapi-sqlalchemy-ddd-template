FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /service/

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install --no-root --no-interaction --no-ansi -vvv && \
    rm -rf $POETRY_CACHE_DIR

COPY alembic.ini .

COPY src src
COPY tests tests

RUN poetry install --no-interaction --no-ansi -vvv

EXPOSE 8080

CMD poetry run bash -c " \
    poe row-migrate && \
    cd src && \
    poe run_server main:app \
"