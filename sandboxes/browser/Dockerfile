FROM node:20-bookworm-slim

WORKDIR /app

# Install system chromium and necessary packages from fast Debian mirrors
RUN apt-get update && apt-get install -y \
    chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies for the runner
COPY package.json ./

# Install npm packages without downloading browsers by default
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
RUN npm install

# Copy the runner script
COPY runner.js ./

# Create the workspace base directory
RUN mkdir -p /workspace && chmod 777 /workspace

# Use sleep infinity to keep container alive
CMD ["sleep", "infinity"]
