# ─────────────────────────────────────────────
# Interleet Sandbox — Node.js 20
# Minimal Alpine-based Node.js runtime
# ─────────────────────────────────────────────
FROM node:20-alpine

# Disable npm update nags
ENV NPM_CONFIG_UPDATE_NOTIFIER=false \
    NODE_ENV=production

# Install sqlite and redis for Phase 4.1 Database Mocking
RUN apk add --no-cache sqlite redis

# Install common modules in the root /node_modules via a temp directory
WORKDIR /tmp/deps
RUN npm init -y && \
    npm install lodash axios redis ws uuid jsdom express sqlite3 mongodb pg mysql2 jsonwebtoken bcryptjs cors dotenv && \
    mv node_modules /node_modules && \
    cd / && rm -rf /tmp/deps

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

# Ensure judge user has permissions for /node_modules
RUN chown -R judge:judge /node_modules

WORKDIR /workspace
RUN chown judge:judge /workspace

# Copy the service runner for Phase 4 Backend execution
COPY service_runner.js /app/service_runner.js
RUN chown -R judge:judge /app

USER judge

CMD ["node", "--version"]
