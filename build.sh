#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin@haatify.com').exists():
    User.objects.create_superuser('admin@haatify.com', 'admin@haatify.com', 'Haatify@2026')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"
