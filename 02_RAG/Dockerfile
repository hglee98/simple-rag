FROM python:3.12.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .
COPY ./data ./data
COPY ./setting.py .
EXPOSE 8000
CMD ["python", "main.py"]