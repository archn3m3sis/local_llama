#!/bin/bash
# Run IAMS in offline mode using UV

echo "Starting IAMS in OFFLINE MODE with UV..."

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "Error: UV is not installed. Please install UV first."
    echo "Run: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Set environment variables
export OFFLINE_MODE=true
export DATABASE_URL=sqlite:///local_llama_offline.db
export CLERK_PUBLISHABLE_KEY=offline_mock_key
export CLERK_SECRET_KEY=offline_mock_secret
export REFLEX_CONFIG_FILE=rxconfig_offline.py
export UV_OFFLINE=1
export UV_CACHE_DIR=$(pwd)/.uv-cache
export UV_FIND_LINKS=$(pwd)/offline_packages

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with UV..."
    uv venv .venv --python python3.11
fi

# Activate virtual environment
source .venv/bin/activate

# Install packages from offline cache if needed
if ! python -c "import reflex" 2>/dev/null; then
    echo "Installing packages from offline cache with UV..."
    uv pip install --offline --find-links offline_packages/ -r requirements-minimal.txt
fi

# Initialize database if needed
if [ ! -f "local_llama_offline.db" ]; then
    echo "Initializing offline database..."
    python init_offline_db.py
fi

# Run the application
echo "Starting Reflex app..."
reflex run --env dev --loglevel debug

