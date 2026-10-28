#!/bin/sh
set -e

if [ "$1" = "gunicorn" ]; then
    echo "→ Миграции"
    python manage.py migrate --noinput

    export PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
    rm -rf "$PROMETHEUS_MULTIPROC_DIR"
    mkdir -p "$PROMETHEUS_MULTIPROC_DIR"
fi

exec "$@"