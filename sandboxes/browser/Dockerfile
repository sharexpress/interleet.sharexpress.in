FROM mcr.microsoft.com/playwright:v1.44.0-jammy

WORKDIR /app

# Install dependencies for the runner
COPY package.json ./
RUN npm install

# Copy the runner script
COPY runner.js ./

# Create the workspace base directory
RUN mkdir -p /workspace && chmod 777 /workspace

# Use sleep infinity to keep container alive
CMD ["sleep", "infinity"]
