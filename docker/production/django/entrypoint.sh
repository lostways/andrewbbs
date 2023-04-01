#!/bin/sh
set -e

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate --noinput

# Run command
exec "$@"