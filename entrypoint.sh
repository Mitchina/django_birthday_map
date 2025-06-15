#!/bin/sh

export PYTHONPATH=".:$PYTHONPATH"

# Might be necessary once collectstatic is run
# mkdir -p static

# For deployment, we migrate, collectstatic etc.
if [ -z "$DEBUG" ]; then
  python manage.py migrate
  # python manage.py collectstatic --no-input
  # python manage.py compilemessages
fi

exec "$@"
