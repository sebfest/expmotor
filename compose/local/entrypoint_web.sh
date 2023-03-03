#!/bin/bash

wait-for-it $POSTGRES_HOST:$POSTGRES_PORT

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
python manage.py collectstatic --no-input --clear

exec "$@"
