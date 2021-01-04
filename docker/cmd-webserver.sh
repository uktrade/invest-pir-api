#!/bin/bash -xe
ARG1=${1-prod}

cd /usr/src/app
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py update_translation_fields
python manage.py update_countries_plus
python manage.py collectstatic --noinput
if [ $ARG1 = 'dev' ]
then
    python manage.py runserver 0.0.0.0:$PORT
else
    gunicorn config.wsgi --bind 0.0.0.0:$PORT --log-file -
fi
