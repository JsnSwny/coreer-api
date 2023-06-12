release: python manage.py migrate
web: gunicorn coreer.wsgi --log-file -
worker: daphne coreer.asgi:application --$PORT --bind 0.0.0.0 -v2