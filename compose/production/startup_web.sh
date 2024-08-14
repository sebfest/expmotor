#!/bin/bash

wait-for-it "$POSTGRES_HOST":"$POSTGRES_PORT"

python manage.py collectstatic --no-input --clear
python manage.py flush --no-input
python manage.py migrate

gunicorn settings.wsgi:application \
	--bind 0.0.0.0:8000 \
	--access-logfile "-" \
	--error-logfile "-" \
	--forwarded-allow-ips="*" \
	--proxy-allow-from="*" \
	--env "SCRIPT_NAME=/app"

exec "$@"
