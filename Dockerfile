FROM python:3.11

WORKDIR /app

# Instalar Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Collectstatic
RUN python manage.py collectstatic --noinput

# Puerto
EXPOSE $PORT

# Comando de inicio
CMD python manage.py migrate && gunicorn medicalAssistant.wsgi:application --bind 0.0.0.0:$PORT
