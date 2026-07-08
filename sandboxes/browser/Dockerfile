FROM node:20-bookworm-slim

WORKDIR /app

# Install dependencies for the runner
COPY package.json ./

# Install npm packages without downloading browsers by default
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
RUN npm install

# Download only Chromium and install its required OS library dependencies
RUN npx playwright install chromium --with-deps

# Clean up caches and lists to minimize image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /root/.npm

# Copy the runner script
COPY runner.js ./

# Create the workspace base directory
RUN mkdir -p /workspace && chmod 777 /workspace

# Use sleep infinity to keep container alive
CMD ["sleep", "infinity"]
