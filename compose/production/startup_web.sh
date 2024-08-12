#!/bin/bash

wait-for-it "$POSTGRES_HOST":"$POSTGRES_PORT"

#python manage.py collectstatic --no-input --clear

gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --forwarded-allow-ips="*" --proxy-allow-from="*"

exec "$@"
