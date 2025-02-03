# Start RabbitMQ

Pull a docker container:
```
docker pull rabbitmq:3.13.1-management
```

Run Docker container
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
```

# Start Celery

```
celery -A medicalAssistant worker --loglevel=info  
```

# Start Tailwind4

```
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css --watch
```

# Run Django Server
```
python manange.py runserver
```