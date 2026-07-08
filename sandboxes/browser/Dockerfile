FROM node:20-bookworm-slim

WORKDIR /app

# Install dependencies for the runner
COPY package.json ./

# Install npm packages without downloading browsers by default
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
RUN npm install

# Route download through fast CDN mirror and download only Chromium + dependencies
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
RUN npx playwright install chromium --with-deps

# Clean up caches and lists to minimize image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /root/.npm

# Copy the runner script
COPY runner.js ./

# Create the workspace base directory
RUN mkdir -p /workspace && chmod 777 /workspace

# Use sleep infinity to keep container alive
CMD ["sleep", "infinity"]
