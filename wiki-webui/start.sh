#!/bin/bash
# Antigravity Wiki UI - Startup Script

LOGFILE="/home/kizamladjanijebac/wiki-server.log"
PORT=3001

# Kill existing instance
pkill -f "wiki-webui/server.js" 2>/dev/null
sleep 1

echo "🚀 Starting Antigravity Wiki UI on port $PORT..."
setsid node /home/kizamladjanijebac/wiki-webui/server.js >> "$LOGFILE" 2>&1 < /dev/null &
disown

sleep 2
if curl -s "http://localhost:$PORT/api/stats" > /dev/null 2>&1; then
    echo "✅ Wiki UI is running at http://localhost:$PORT"
else
    echo "❌ Failed to start. Check $LOGFILE"
fi
