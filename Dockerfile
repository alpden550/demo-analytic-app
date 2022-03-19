FROM python:3-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apk update && apk add gcc python3-dev musl-dev postgresql-dev libffi-dev
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
RUN poetry install

EXPOSE 8000
