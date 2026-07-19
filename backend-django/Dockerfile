# Start from the official Python image
FROM python:3.11-slim

# Expose port
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create a working directory
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the whole project after dependencies are installed
COPY . .

RUN DJANGO_SECRET_KEY=build-only \
    python manage.py collectstatic --noinput

# gcloud builds submit --tag europe-central2-docker.pkg.dev/psychological-app-a359c/psycho-docker/quickstart
# Run gunicorn with binding
CMD exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --threads 8 \
    --timeout 120