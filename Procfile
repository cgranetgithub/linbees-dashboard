# web: gunicorn service.wsgi
# web: newrelic-admin run-program gunicorn service.wsgi
web: newrelic-admin run-program waitress-serve --port=$PORT service.wsgi:application