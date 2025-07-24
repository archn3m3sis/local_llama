#!/bin/bash
# Quick launcher for the offline demo app

echo "🚀 Launching IAMS Offline Demo..."
echo ""

# Check if offline_app exists
if [ ! -d "offline_app" ]; then
    echo "❌ offline_app directory not found!"
    echo "Run: python setup_offline_app.py"
    exit 1
fi

# Change to offline_app and run
cd offline_app && ./run.sh