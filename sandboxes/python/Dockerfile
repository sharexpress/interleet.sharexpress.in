# ─────────────────────────────────────────────
# Interleet Sandbox — Python 3.12
# Minimal Alpine-based Python runtime
# ─────────────────────────────────────────────
FROM python:3.12-alpine

# Security: disable pip version checks and analytics
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install sqlite and redis for Phase 4.1 Database Mocking
RUN apk add --no-cache sqlite redis

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

# Pre-install FastAPI and Uvicorn for APIs challenges
RUN pip install --no-cache-dir fastapi uvicorn pymongo psycopg2-binary PyMySQL python-jose pyjwt passlib bcrypt cryptography

# Copy the service runner for Phase 4 Backend execution
COPY service_runner.py /app/service_runner.py
RUN chown -R judge:judge /app

# Fix ownership
RUN chown judge:judge /workspace

USER judge

CMD ["python3", "--version"]
