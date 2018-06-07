#!/bin/bash -xe

cd /usr/src/app
./node_modules/.bin/gulp css
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py update_translation_fields
python manage.py update_countries_plus
python manage.py collectstatic --noinput
gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
