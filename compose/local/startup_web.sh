#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
if [[ "${GENERATE_FAKE_DATA:-0}" == "1" ]]; then
    python manage.py generate_fake_data
fi
python manage.py collectstatic --no-input --clear -v 0
gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --reload

exec "$@"
