
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/model.gguf

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" llama-cpp-python

RUN curl -fL \
    "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf" \
    -o /app/model.gguf

COPY app.py .

ENV PORT=8080

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]