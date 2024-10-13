FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 as builder

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  POETRY_NO_INTERACTION=1 \
  POETRY_HOME="/opt/poetry" \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/app/.venv" \
  POETRY_VERSION=1.8.3 \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  PYTHONPATH=/app \
  PIP_PREFER_BINARY=1 \
  LC_ALL=C.UTF-8 \
  PYTHONIOENCODING=utf-8

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
# ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

# Update system and install wget
# RUN apt update && \
#     DEBIAN_FRONTEND="noninteractive" apt install --no-install-suggests --no-install-recommends -y \
#     curl pipx && \
#     apt clean && \
#     rm -rf /var/lib/apt/lists/*
# ENV PATH="/root/.local/bin:${PATH}"
# RUN pipx install poetry
# RUN pipx inject poetry poetry-plugin-bundle
# RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root --no-ansi --no-interaction --only main


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim as final
# FROM python:3.11-slim
# FROM python:3.11-alpine

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app/

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./scripts/ /app/

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./tests-start.sh /app/

COPY ./app /app/app
