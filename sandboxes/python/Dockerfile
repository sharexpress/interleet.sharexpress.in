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

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

# Fix ownership
RUN chown judge:judge /workspace

USER judge

CMD ["python3", "--version"]
