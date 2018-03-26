#!/bin/bash -xe

cd /usr/src/app
python manage.py migrate --noinput
python manage.py update_translation_fields
python manage.py collectstatic --noinput
python manage.py sync_page_translation_fields --noinput
gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
