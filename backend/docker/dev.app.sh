#!/bin/bash
sleep 2
alembic upgrade head

cd tests

python fill_empty_db.py

cd ../backend

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000