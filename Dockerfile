# ─── Stage 1: Builder ───────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ─── Stage 2: Runtime ───────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="Student DevOps Lab"
LABEL description="Student Feedback System - Flask Application"

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/           ./app/
COPY app/templates/ ./templates/
COPY app/static/    ./static/

RUN mkdir -p /data && chown appuser:appuser /data

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/feedback.db \
    FLASK_ENV=production

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app.app:app"]
