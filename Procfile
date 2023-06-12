web: gunicorn coreer.wsgi --log-file -
worker: daphne coreer.asgi:application --port $PORT --bind 0.0.0.0 -v2