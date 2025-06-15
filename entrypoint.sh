#!/bin/sh

export PYTHONPATH=".:$PYTHONPATH"

mkdir -p static

# For deployment, we migrate, collectstatic etc.
if [ -z "$DEBUG" ]; then
  python manage.py migrate
  # python manage.py collectstatic --no-input
  # python manage.py compilemessages
else
  python manage.py migrate
  # python manage.py collectstatic --no-input
  # python manage.py compilemessages
  python manage.py loaddata events/fixtures/events.json
fi

exec "$@"
