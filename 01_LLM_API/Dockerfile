FROM pytorch/pytorch:2.7.1-cuda12.6-cudnn9-devel

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV HF_HOME=/CHECKPOINT/huggingface-cache-dir
RUN mkdir -p $HF_HOME


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]