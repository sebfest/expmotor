#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

wait-for-it web_dev:8000

exec "$@"
