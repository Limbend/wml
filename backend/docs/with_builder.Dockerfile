FROM python:3.9 AS builder

RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r ./requirements.txt

FROM python:3.9-slim
LABEL version="0.1"

WORKDIR /app
COPY --from=builder /app/wheels ./wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache ./wheels/*

ADD . .

WORKDIR /app/api/
CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]