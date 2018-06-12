web: mkdir -p ~/.local/share/fonts && cp ./fonts/* ~/.local/share/fonts/ && fc-cache -f -v && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py clear_cache && gunicorn config.wsgi --bind 0.0.0.0:$PORT
worker: mkdir -p ~/.local/share/fonts && cp ./fonts/* ~/.local/share/fonts/ && fc-cache -f -v && celery -A config worker -l info
