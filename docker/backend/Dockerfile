FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY src/ ./src/

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=admin.infrastructure.web.django_app.settings

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "admin.infrastructure.web.django_app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
