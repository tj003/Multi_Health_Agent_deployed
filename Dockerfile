# FROM python:3.11-slim

# WORKDIR /app
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # ✅ Create writable local dirs for crewai
# RUN mkdir -p /app/.local /app/.cache && chmod -R 777 /app

# # ✅ Point HOME + XDG dirs to /app
# ENV HOME=/app
# ENV XDG_DATA_HOME=/app/.local
# ENV XDG_CACHE_HOME=/app/.cache

# COPY . .

# CMD ["streamlit", "run", "ui.py", "--server.port=7860", "--server.address=0.0.0.0"]
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Create writable local dirs for crewai
RUN mkdir -p /app/.local /app/.cache && chmod -R 777 /app

# ✅ Point HOME + XDG dirs to /app
ENV HOME=/app
ENV XDG_DATA_HOME=/app/.local
ENV XDG_CACHE_HOME=/app/.cache

COPY . .

EXPOSE 8000
EXPOSE 8501

CMD bash -c "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"
