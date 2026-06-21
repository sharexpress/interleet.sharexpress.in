# ─────────────────────────────────────────────
# Interleet Sandbox — TypeScript 5
# Node.js 20 + TypeScript compiler (tsc)
# ─────────────────────────────────────────────
FROM node:20-alpine

ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NODE_ENV=production

# Install typescript and ts-node globally so they are in the PATH
RUN npm install -g typescript ts-node && \
    npm cache clean --force

# Install types and dependencies in the root /node_modules
WORKDIR /
RUN npm install @types/node lodash @types/lodash axios redis ws @types/ws uuid @types/uuid && \
    npm cache clean --force

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

# Ensure judge user has permissions for /node_modules
RUN chown -R judge:judge /node_modules

WORKDIR /workspace
RUN chown judge:judge /workspace

USER judge

CMD ["tsc", "--version"]
