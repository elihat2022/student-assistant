#!/bin/bash

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar Celery en background
celery -A medicalAssistant worker --loglevel=info &

# Iniciar Gunicorn
gunicorn medicalAssistant.wsgi
