FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    django==5.0.0 \
    djangorestframework==3.14.0 \
    djangorestframework-simplejwt==5.3.0 \
    django-cors-headers==4.3.0 \
    django-filter==23.5 \
    psycopg2-binary==2.9.9 \
    uvicorn[standard]==0.27.0 \
    python-decouple==3.8 \
    pydantic==2.5.3 \
    pydantic-settings==2.1.0 \
    redis==5.0.1 \
    celery==5.3.4 \
    pika==1.3.2 \
    boto3==1.34.0 \
    prometheus-client==0.19.0 \
    whitenoise==6.6.0

COPY manage.py .
COPY src/ ./src/

ENV PYTHONPATH=/app/src
ENV DJANGO_SETTINGS_MODULE=admin.infrastructure.web.django_app.settings

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
