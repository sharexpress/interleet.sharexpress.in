# ─────────────────────────────────────────────
# Interleet Sandbox — TypeScript 5
# Node.js 20 + TypeScript compiler (tsc)
# ─────────────────────────────────────────────
FROM node:20-alpine

ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NODE_ENV=production

# Install TypeScript globally (pinned version for reproducibility)
RUN npm install -g typescript@5.4.5 --prefer-offline 2>/dev/null || \
    npm install -g typescript@5 && \
    npm cache clean --force

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

RUN chown judge:judge /workspace

USER judge

CMD ["tsc", "--version"]
