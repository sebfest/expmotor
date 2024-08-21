#!/bin/bash

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
python manage.py generate_fake_data
python manage.py collectstatic --no-input --clear -v 0
gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"
