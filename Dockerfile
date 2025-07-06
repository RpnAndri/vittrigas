FROM python:3.11-slim

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set initial working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire repo
COPY . .

# Change to Django root directory
WORKDIR /app/vittrigas

# Environment setup
ENV DJANGO_SETTINGS_MODULE=vittrigas.settings
ENV PYTHONPATH=/app/vittrigas

# Set up static file output directory
RUN mkdir -p /app/vittrigas/staticfiles

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Run app
CMD ["gunicorn", "vittrigas.wsgi:application", "--bind", "0.0.0.0:8080"]
