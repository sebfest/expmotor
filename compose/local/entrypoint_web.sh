#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

wait-for-it $POSTGRES_HOST:$POSTGRES_PORT

python manage.py migrate
python manage.py createsuperuserwithpassword \
        --username admin \
        --password admin \
        --email admin@example.org \
        --preserve
python manage.py collectstatic --no-input --clear

exec "$@"
