web: gunicorn medicalAssistant.wsgi:application
worker: celery -A medicalAssistant worker --loglevel=info