FROM python:3.9 AS builder

RUN mkdir /app
WORKDIR /app

RUN pip install --no-cache-dir uv
ADD pyproject.toml ./
ADD uv.lock ./

RUN uv sync --no-dev

FROM python:3.9-slim AS dev
LABEL version="0.1"

RUN mkdir /app
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ADD ./ ./

WORKDIR /app/api/
CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]