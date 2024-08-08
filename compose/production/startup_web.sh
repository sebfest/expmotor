#!/bin/bash

wait-for-it "$POSTGRES_HOST":"$POSTGRES_PORT"

python manage.py collectstatic --no-input --clear

gunicorn settings.wsgi:application \
  --capture-output \
  --access-logfile /app/logs/access.log \
  --error-logfile /app/logs/error.log \
  --enable-stdio-inheritance \
  --bind 0.0.0.0:8000

exec "$@"
