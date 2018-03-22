#!/bin/bash -xe

python /usr/src/app/manage.py migrate --noinput
python /usr/src/app/manage.py collectstatic --noinput
python manage.py sync_page_translation_fields --noinput
gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
