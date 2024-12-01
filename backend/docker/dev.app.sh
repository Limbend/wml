#!/bin/bash

sleep 2

cd /app
alembic upgrade head

cd tests

python fill_empty_db.py

cd ../api

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000