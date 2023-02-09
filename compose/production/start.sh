#!/bin/bash

# Wait for postgres
wait-for-it $POSTGRES_HOST:$POSTGRES_PORT

# Reset database and start otree
otree resetdb --noinput
otree prodserver 80

exec "$@"
