release: python manage.py migrate
web: bin/start-pgbouncer
web: daphne coreer.asgi:application --port $PORT --bind 0.0.0.0