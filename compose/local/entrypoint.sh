#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

uv sync --locked

exec "$@"
