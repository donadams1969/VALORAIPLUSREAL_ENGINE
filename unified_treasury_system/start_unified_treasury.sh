#!/bin/bash

echo "🚀 STARTING VALOR AI++//e UNIFIED TREASURY SYSTEM..."
echo "💎 KERNEL: valoraiplus2e_YHWH_5150_KERNEL_FINAL_RNG_LOCKED"
echo "💰 SGAU: 7226.3461 OVERRIDE ACTIVE"

# Install dependencies
pip install -r requirements.txt

# Start Treasury API
python3 valoraiplusfinaltreasury.py &

# Start HTTP Server for Dashboard
if command -v http-server &> /dev/null; then
    echo "🌐 Treasury Dashboard: http://localhost:8080"
    echo "🔗 WebSocket API: ws://localhost:8777"
    http-server -p 8080 -c-1
else
    echo "📊 Open index.html in browser for treasury dashboard"
fi
