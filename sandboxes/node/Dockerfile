# ─────────────────────────────────────────────
# Interleet Sandbox — Node.js 20
# Minimal Alpine-based Node.js runtime
# ─────────────────────────────────────────────
FROM node:20-alpine

# Disable npm update nags
ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NODE_ENV=production

# Install common modules in the root /node_modules
WORKDIR /
RUN npm install lodash axios redis ws uuid && \
    npm cache clean --force

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

# Ensure judge user has permissions for /node_modules
RUN chown -R judge:judge /node_modules

WORKDIR /workspace
RUN chown judge:judge /workspace

USER judge

CMD ["node", "--version"]
