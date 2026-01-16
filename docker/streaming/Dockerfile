FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    pydantic==2.5.0 \
    pydantic[email]==2.5.0 \
    httpx==0.26.0 \
    prometheus-client==0.19.0 \
    asyncpg==0.29.0 \
    pika==1.3.0 \
    aio-pika==9.3.0 \
    boto3==1.34.0 \
    minio==7.2.0 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    slowapi==0.1.9

# Copy source code
COPY src/ ./src/

EXPOSE 8001

CMD ["uvicorn", "src.streaming.infrastructure.web.main:app", "--host", "0.0.0.0", "--port", "8001"]
