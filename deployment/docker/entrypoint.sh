#!/bin/sh

set -e

if [ "$(id -u)" = "0" ]; then
	mkdir -p /app/staticfiles
	chown -R appuser:appuser /app/staticfiles
	exec gosu appuser "$0" "$@"
fi

echo "Running database migrations..."

python manage.py migrate --noinput

echo "Collecting static files..."

python manage.py collectstatic --noinput

echo "Starting application..."

exec "$@"