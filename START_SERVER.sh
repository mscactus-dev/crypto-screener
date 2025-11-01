#!/bin/bash
# Bitcoin Astrology - Live Server Launcher
# Double-click this file to start the server!

echo "======================================================================"
echo "🌟 BITCOIN FINANCIAL ASTROLOGY - LIVE SERVER"
echo "======================================================================"
echo ""
echo "Starting Python web server..."
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Start the server
python3 server.py

# Keep window open if there's an error
read -p "Press Enter to exit..."
