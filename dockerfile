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

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY alembic.ini .
COPY setup.cfg .
COPY makefile .

COPY src src
COPY tests tests

RUN poetry install

EXPOSE 8080

CMD bash -c "\
    make migrate-in-container && \
    cd src && \
    poetry run uvicorn --host 0.0.0.0 --port 8080 main:app --reload \
"