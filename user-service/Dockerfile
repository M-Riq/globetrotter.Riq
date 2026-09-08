FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY user-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY user-service/ .

EXPOSE 5002

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request as u; import sys; sys.exit(0 if u.urlopen('http://localhost:5002/health').status==200 else 1)"

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "2", "app:app"]
