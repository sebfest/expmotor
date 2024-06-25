#!/bin/bash

wait-for-it "$POSTGRES_HOST":"$POSTGRES_PORT"

DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}
until pg_isready -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}"; do
    sleep 1
    echo "Waiting for postgres at: ${DATABASE_URL}"
done


python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
python manage.py generate_fake_data
python manage.py collectstatic --no-input --clear
gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"
