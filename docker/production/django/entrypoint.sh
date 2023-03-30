#!/bin/sh
set -e

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
until psql $DATABASE_URL -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
  python manage.py migrate --noinput
fi

# Run command
exec "$@"