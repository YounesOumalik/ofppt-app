FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL="postgresql://user:pass@db:5432/ofppt"
ENV JWT_SECRET="change-me-in-production"
ENV CORS_ORIGINS="https://efp.app.ma"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
