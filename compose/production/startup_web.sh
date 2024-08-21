#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input --clear

echo "Starting gunicorn"
gunicorn settings.wsgi:application \
	--bind 0.0.0.0:8000 \
	--access-logfile "-" \
	--error-logfile "-" \
	--forwarded-allow-ips="*" \
	--proxy-allow-from="*" \
	--env "SCRIPT_NAME=/expmotor"

exec "$@"