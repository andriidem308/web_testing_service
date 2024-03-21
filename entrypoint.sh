#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn web_testing_service.wsgi:application --bind 0.0.0.0:8000
