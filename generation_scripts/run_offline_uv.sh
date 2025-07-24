#!/bin/bash
echo "Starting IAMS in OFFLINE MODE with UV..."

# Set environment variables
export OFFLINE_MODE=true
export DATABASE_URL=sqlite:///local_llama_offline.db
export UV_OFFLINE=1
export UV_CACHE_DIR=$(pwd)/.uv-cache

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "Error: UV is not installed. Please install UV first."
    exit 1
fi

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with UV..."
    uv venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install packages with UV (will use offline cache if available)
echo "Installing packages..."
uv pip install -r requirements-minimal.txt

# Initialize database if needed
if [ ! -f "local_llama_offline.db" ]; then
    echo "Creating offline SQLite database..."
    python -c "
import os
os.environ['DATABASE_URL'] = 'sqlite:///local_llama_offline.db'
from local_llama.models import *
from sqlmodel import create_engine, SQLModel
engine = create_engine('sqlite:///local_llama_offline.db')
SQLModel.metadata.create_all(engine)
print('Database created successfully')
"
fi

# Run the application
echo "Starting Reflex app in offline mode..."
reflex run --env dev
