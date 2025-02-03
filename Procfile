web: gunicorn medicalAssistant.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A medicalAssistant worker --loglevel=info