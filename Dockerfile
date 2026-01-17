# Multi-stage build for the lip reading application

FROM python:3.11-slim as backend-builder

WORKDIR /app

COPY backend/requirements.txt .
COPY backend/requirements-prod.txt .

RUN pip install --no-cache-dir -r requirements-prod.txt

COPY backend/ .

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
