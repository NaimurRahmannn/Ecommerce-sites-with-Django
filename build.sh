#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Optional: create superuser from env vars.
if [ "${DJANGO_CREATE_SUPERUSER:-0}" = "1" ]; then
  : "${DJANGO_SUPERUSER_USERNAME:?Missing DJANGO_SUPERUSER_USERNAME}"
  : "${DJANGO_SUPERUSER_EMAIL:?Missing DJANGO_SUPERUSER_EMAIL}"
  : "${DJANGO_SUPERUSER_PASSWORD:?Missing DJANGO_SUPERUSER_PASSWORD}"

  python manage.py createsuperuser --noinput || echo "Superuser exists, skipping."
fi
