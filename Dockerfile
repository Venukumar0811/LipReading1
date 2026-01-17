# Multi-stage build for the lip reading application

FROM python:3.11-slim as backend-builder

WORKDIR /app

COPY backend/requirements-prod.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-prod.txt

COPY backend/ .

EXPOSE 8080

ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    DEVICE=cpu

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
