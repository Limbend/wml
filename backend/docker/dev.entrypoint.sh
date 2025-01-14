#!/bin/bash

# You must use line breaks in LF format!
# Otherwise the container sends non-obvious errors. As if such a file does not exist.

sleep 2

echo "dev.entrypoint.sh -- Start alembic upgrade"
cd /app
alembic upgrade head

echo "dev.entrypoint.sh -- Run fill_empty_db.py"
cd tests
python fill_empty_db.py

echo "dev.entrypoint.sh -- Start app"
cd ../api
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000