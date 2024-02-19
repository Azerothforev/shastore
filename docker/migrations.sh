#!/bin/bash
docker/wait-for-it.sh rabbitmq:5672 -- echo "RabbitMQ is up!"

docker/wait-for-it.sh db:5432 -- echo "Database is up!"

cd src

alembic upgrade head

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000