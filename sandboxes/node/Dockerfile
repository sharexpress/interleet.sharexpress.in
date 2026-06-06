# ─────────────────────────────────────────────
# Interleet Sandbox — Node.js 20
# Minimal Alpine-based Node.js runtime
# ─────────────────────────────────────────────
FROM node:20-alpine

# Disable npm update nags
ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NODE_ENV=production

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

RUN chown judge:judge /workspace

USER judge

CMD ["node", "--version"]
