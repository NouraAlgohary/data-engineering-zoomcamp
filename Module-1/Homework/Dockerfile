FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary pyarrow sh

WORKDIR /app
COPY ingestion_script.py .

ENTRYPOINT ["python", "ingestion_script.py"]