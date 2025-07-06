FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Ensure environment is ready for collectstatic
ENV DJANGO_SETTINGS_MODULE=vittrigas.settings
ENV PYTHONPATH=/app

# Optional: Create the static root folder if needed
# RUN mkdir -p /app/staticfiles

# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "vittrigas.wsgi:application", "--bind", "0.0.0.0:8080"]
