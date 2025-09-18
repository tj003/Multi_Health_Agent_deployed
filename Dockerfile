FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ✅ Redirect all local data/cache paths to /app/.local
ENV HOME=/app
ENV XDG_DATA_HOME=/app/.local
ENV XDG_CACHE_HOME=/app/.cache

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
