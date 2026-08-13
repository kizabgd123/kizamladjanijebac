FROM node:18-slim

# Install system dependencies (Python3 for nlm CLI integration)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv and notebooklm-mcp-cli for cloud NotebookLM RAG execution
RUN pip install --no-cache-dir uv && \
    uv tool install notebooklm-mcp-cli || true

WORKDIR /app

# Copy package descriptors and install dependencies
COPY package*.json ./
RUN npm install

# Copy application source files
COPY . .

# Build Vite frontend bundle
RUN npm run build

# Expose server port (Cloud Run sets PORT dynamically)
ENV PORT=5000
EXPOSE 5000

# Start server
CMD ["node", "server.js"]
