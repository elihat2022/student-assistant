# Student Assistant

An AI-powered web application that transforms voice recordings into organized, actionable study materials. Built with Django and integrated with OpenAI's Whisper API for transcription and GPT-4 for content analysis.

## Features

- 🎙️ Voice recording and transcription using AI
- 📝 Automatic highlight extraction and summarization
- 🏷️ Tagging and organization system
- 🔍 Full-text search capabilities
- ☁️ Cloud storage with Cloudflare R2
- 📧 Email notifications
- 🔐 Secure user authentication with reCAPTCHA

## Tech Stack

- **Backend**: Django 5.1.4, PostgreSQL
- **Frontend**: Tailwind CSS, JavaScript
- **AI Services**: OpenAI (Whisper, GPT-4), Replicate
- **Queue**: Celery with Redis
- **Storage**: Cloudflare R2
- **Deployment**: Railway, Docker

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False

# Database (PostgreSQL)
PGDATABASE=your-db-name
PGUSER=your-db-user
PGPASSWORD=your-db-password
PGHOST=your-db-host
PGPORT=5432

# Redis
REDIS_URL=redis://localhost:6379

# Cloudflare R2 Storage
CLOUDFLARE_R2_BUCKET=your-bucket-name
CLOUDFLARE_R2_ACCESS_KEY=your-access-key
CLOUDFLARE_R2_SECRET_KEY=your-secret-key
CLOUDFLARE_R2_ENDPOINT=your-endpoint-url

# AI Services
OPENAI_API_KEY=your-openai-key
REPLICATE_API_TOKEN=your-replicate-token

# Email (SendGrid)
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_SENDER_EMAIL=your-verified-sender-email

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
```

## Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js (for Tailwind CSS)
- PostgreSQL
- Redis

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/elihat2022/student-assistant.git
   cd student-assistant
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start Redis (using Docker)**

   ```bash
   docker run -d --name redis -p 6379:6379 redis:latest
   ```

7. **Build Tailwind CSS**

   ```bash
   npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css --watch
   ```

8. **Start Celery worker** (in a new terminal)

   ```bash
   celery -A studentAssistant worker --loglevel=info
   ```

9. **Run Django development server**
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### Railway Deployment

This project is configured for Railway deployment with Docker.

1. **Push to Railway**

   ```bash
   # Connect your GitHub repository to Railway
   # or use Railway CLI
   railway login
   railway link
   railway up
   ```

2. **Environment Variables**
   Set all required environment variables in Railway dashboard

3. **Services Configuration**
   The project includes:
   - **Web service**: Django application (Dockerfile)
   - **Worker service**: Celery background tasks (Dockerfile.celery)
   - **Database**: PostgreSQL addon
   - **Redis**: Redis addon

### Docker Deployment

**Web Service:**

```bash
docker build -t student-assistant-web .
docker run -p 8080:8080 --env-file .env student-assistant-web
```

**Celery Worker:**

```bash
docker build -f Dockerfile.celery -t student-assistant-worker .
docker run --env-file .env student-assistant-worker
```

### Manual Server Deployment

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Collect static files**

   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Start services**

   ```bash
   # Web server
   gunicorn studentAssistant.wsgi:application --bind 0.0.0.0:8000

   # Celery worker
   celery -A studentAssistant worker --loglevel=info
   ```

## Project Structure

```
student-assistant/
├── account/              # User authentication
├── dashboard/            # Main application logic
├── helpers/             # Utility functions
│   └── cloudflare/      # Cloudflare R2 storage
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── student-assistant/   # Django project settings
├── Dockerfile           # Web service container
├── Dockerfile.celery    # Celery worker container
├── requirements.txt     # Python dependencies
├── railway.json         # Railway deployment config
└── manage.py           # Django management script
```

## API Integration

- **OpenAI Whisper**: Audio transcription
- **OpenAI GPT-4**: Content analysis and summarization
- **Replicate**: Alternative AI processing
- **SendGrid**: Email notifications
- **Cloudflare R2**: File storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
