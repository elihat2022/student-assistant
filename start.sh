#!/bin/bash

# Imprimir variables de entorno (sin valores sensibles)
echo "Checking environment variables..."
if [ -n "$SECRET_KEY" ]; then
    echo "SECRET_KEY is set"
else
    echo "SECRET_KEY is NOT set"
fi

if [ -n "$PGDATABASE" ]; then
    echo "PGDATABASE is set"
else
    echo "PGDATABASE is NOT set"
fi

# Iniciar la aplicación
echo "Starting application..."
gunicorn medicalAssistant.wsgi:application
