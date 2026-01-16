#!/bin/sh


echo "Running migrations..."
alembic upgrade head

sleep 10



echo "Starting server..."
exec gunicorn --bind 0.0.0.0:8000 main:app --worker-class uvicorn.workers.UvicornWorker