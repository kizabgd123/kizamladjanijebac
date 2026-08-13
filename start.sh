#!/bin/bash

echo "======================================================="
echo "🚀 Pokretanje Nexus Multi-Agent RAG Studio"
echo "======================================================="

# Build the frontend if dist doesn't exist
if [ ! -d "dist" ]; then
    echo "📦 Kompajliranje frontend aplikacije..."
    npm run build
fi

# Kill any existing server on port 5000
echo "🧹 Oslobađanje portova..."
lsof -ti:5000 | xargs kill -9 2>/dev/null

echo "✅ Pokretanje backend servera..."
# Start the Node.js server which serves both API and static frontend
node server.js
