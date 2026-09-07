FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install service dependencies first for better layer caching
COPY auth-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Shared infrastructure (single source of truth, copied at build time)
COPY common ./common

# Service code
COPY auth-service/ .

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request as u; import sys; sys.exit(0 if u.urlopen('http://localhost:5001/health').status==200 else 1)"

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
