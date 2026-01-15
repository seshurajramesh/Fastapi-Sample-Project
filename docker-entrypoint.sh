#!/bin/sh

alembic upgrade head

exec gunicorn --bind 0.0.0.0:8000 main:app --worker-class uvicorn.workers.UvicornWorker