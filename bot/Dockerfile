FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y curl
RUN apt-get install -y redis-tools


COPY . .

# HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/api/students/create/ || exit 1

CMD ["python", "app.py"]
