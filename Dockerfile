FROM python:3.14-slim

WORKDIR /app
COPY ./app /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y git \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove git \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "main:app"]
