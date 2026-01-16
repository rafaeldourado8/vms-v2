FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    httpx==0.26.0 \
    pydantic==2.5.0

COPY src/detection /app/detection

ENV PYTHONPATH=/app

EXPOSE 8002

CMD ["uvicorn", "detection.main:app", "--host", "0.0.0.0", "--port", "8002"]
