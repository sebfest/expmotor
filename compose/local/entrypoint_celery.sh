#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

uv sync --locked

wait-for-it web_dev:8000

exec "$@"
