FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install uvicorn==0.23.1 --no-cache-dir
# RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD ["gunicorn", "root.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["uvicorn", "root.asgi:application", "--host", "0.0.0.0", "--port", "9000"]
