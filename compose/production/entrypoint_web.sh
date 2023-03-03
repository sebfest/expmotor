#!/bin/bash

wait-for-it $POSTGRES_HOST:$POSTGRES_PORT

python manage.py collectstatic --no-input --clear

exec "$@"
