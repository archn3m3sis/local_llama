#!/usr/bin/env python3
"""
Set up a complete offline app directory with all components.
This creates a self-contained offline version of the IAMS app.
"""

import os
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and return result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        if result.stdout:
            print(result.stdout)
    return result.returncode == 0

def create_directory_structure():
    """Create the offline app directory structure."""
    offline_dir = Path("offline_app")
    
    # Remove existing offline_app if it exists
    if offline_dir.exists():
        print("Removing existing offline_app directory...")
        shutil.rmtree(offline_dir)
    
    # Create directory structure
    dirs = [
        "offline_app",
        "offline_app/local_llama",
        "offline_app/.uv-cache",
        "offline_app/.uv",
        "offline_app/offline_packages",
        "offline_app/npm-offline-cache",
        "offline_app/offline_mocks",
        "offline_app/scripts",
        "offline_app/config",
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")
    
    return offline_dir

def copy_application_files(offline_dir):
    """Copy the main application files."""
    print("\nCopying application files...")
    
    # Copy the entire local_llama module
    if Path("local_llama").exists():
        shutil.copytree("local_llama", offline_dir / "local_llama", dirs_exist_ok=True)
        print("✓ Copied local_llama module")
    
    # Copy .web directory if it exists
    if Path(".web").exists():
        shutil.copytree(".web", offline_dir / ".web", dirs_exist_ok=True)
        print("✓ Copied .web directory")
    
    # Copy Python files
    files_to_copy = [
        "pyproject.toml",
        "requirements-demo.txt",
        "requirements-minimal.txt",
        "alembic.ini",
    ]
    
    for file in files_to_copy:
        if Path(file).exists():
            shutil.copy(file, offline_dir / file)
            print(f"✓ Copied {file}")

def copy_offline_components(offline_dir):
    """Copy offline-specific components."""
    print("\nCopying offline components...")
    
    # Copy UV cache
    if Path(".uv-cache").exists():
        shutil.copytree(".uv-cache", offline_dir / ".uv-cache", dirs_exist_ok=True)
        print("✓ Copied UV cache")
    
    # Copy offline packages
    if Path("offline_packages").exists():
        shutil.copytree("offline_packages", offline_dir / "offline_packages", dirs_exist_ok=True)
        print("✓ Copied offline packages")
    
    # Copy npm cache
    if Path("npm-offline-cache").exists():
        shutil.copytree("npm-offline-cache", offline_dir / "npm-offline-cache", dirs_exist_ok=True)
        print("✓ Copied npm cache")
    
    # Copy mock modules
    if Path("offline_mocks").exists():
        shutil.copytree("offline_mocks", offline_dir / "offline_mocks", dirs_exist_ok=True)
        print("✓ Copied mock modules")
    
    # Copy demo database
    if Path("demo_offline.db").exists():
        shutil.copy("demo_offline.db", offline_dir / "demo_offline.db")
        print("✓ Copied demo database")

def create_offline_configs(offline_dir):
    """Create offline-specific configuration files."""
    print("\nCreating offline configurations...")
    
    # Create rxconfig for offline mode
    rxconfig_content = '''import reflex as rx
import os

# Offline mode configuration
config = rx.Config(
    app_name="local_llama",
    # Disable telemetry for offline mode
    telemetry_enabled=False,
    # Environment
    env=rx.Env.DEV,
    # Database URL (use SQLite for offline)
    db_url=os.getenv("DATABASE_URL", "sqlite:///demo_offline.db"),
)
'''
    
    with open(offline_dir / "rxconfig.py", "w") as f:
        f.write(rxconfig_content)
    print("✓ Created rxconfig.py")
    
    # Create UV configuration
    uv_config = """[pip]
offline = true
no-cache = false
cache-dir = "./.uv-cache"
find-links = ["./offline_packages"]
no-index = true
"""
    
    with open(offline_dir / ".uv" / "uv.toml", "w") as f:
        f.write(uv_config)
    print("✓ Created UV configuration")
    
    # Create .env file for offline mode
    env_content = """# Offline Mode Environment Variables
OFFLINE_MODE=true
DATABASE_URL=sqlite:///demo_offline.db
CLERK_PUBLISHABLE_KEY=offline_mock_key
CLERK_SECRET_KEY=offline_mock_secret
REFLEX_TELEMETRY_ENABLED=false
DO_NOT_TRACK=1
UV_OFFLINE=1
NPM_CONFIG_OFFLINE=true
NPM_CONFIG_PREFER_OFFLINE=true
"""
    
    with open(offline_dir / ".env", "w") as f:
        f.write(env_content)
    print("✓ Created .env file")

def create_scripts(offline_dir):
    """Create runner scripts for the offline app."""
    print("\nCreating runner scripts...")
    
    # Main runner script
    run_script = '''#!/bin/bash
# Run IAMS in offline mode

echo "🚀 Starting IAMS Offline App..."
echo "================================"

# Change to script directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set additional environment variables
export UV_CACHE_DIR=$(pwd)/.uv-cache
export UV_FIND_LINKS=$(pwd)/offline_packages
export NPM_CONFIG_CACHE=$(pwd)/npm-offline-cache
export PYTHONPATH=$(pwd)/offline_mocks:$PYTHONPATH

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install packages if needed
if ! python -c "import reflex" 2>/dev/null; then
    echo "Installing packages from cache..."
    uv pip install -r requirements-minimal.txt
fi

# Check database
if [ ! -f "demo_offline.db" ]; then
    echo "Creating demo database..."
    python scripts/create_demo_db.py
fi

echo ""
echo "✅ Offline app ready!"
echo "📍 Access at: http://localhost:3000"
echo "🛑 Press Ctrl+C to stop"
echo ""

# Run Reflex
reflex run --env dev
'''
    
    with open(offline_dir / "run.sh", "w") as f:
        f.write(run_script)
    os.chmod(offline_dir / "run.sh", 0o755)
    print("✓ Created run.sh")
    
    # Setup script for first time
    setup_script = '''#!/bin/bash
# Initial setup for offline app

echo "Setting up offline app environment..."

# Create virtual environment
if [ ! -d ".venv" ]; then
    uv venv .venv
fi

# Activate and install
source .venv/bin/activate
uv pip install -r requirements-minimal.txt

# Create database
python scripts/create_demo_db.py

echo "✅ Setup complete! Run ./run.sh to start the app"
'''
    
    with open(offline_dir / "setup.sh", "w") as f:
        f.write(setup_script)
    os.chmod(offline_dir / "setup.sh", 0o755)
    print("✓ Created setup.sh")
    
    # Create demo database script
    db_script = '''import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DATABASE_URL"] = "sqlite:///demo_offline.db"

from local_llama.models import *
from sqlmodel import create_engine, SQLModel, Session

# Create engine and tables
engine = create_engine("sqlite:///demo_offline.db")
SQLModel.metadata.create_all(engine)

# Add some demo data
with Session(engine) as session:
    # Add departments
    dept = Department(dept_name="IT Department", dept_description="Demo IT Dept")
    session.add(dept)
    session.commit()
    
    # Add privilege level
    priv = PrivilegeLevel(priv_name="Admin", priv_description="Demo Admin")
    session.add(priv)
    session.commit()
    
    # Add demo employee with required email
    emp = Employee(
        first_name="Demo",
        last_name="User",
        email="demo@offline.local",
        department_id=dept.dept_id
    )
    session.add(emp)
    session.commit()
    
    # Add a demo project
    project = Project(
        project_name="Demo Project",
        project_description="Offline demo project"
    )
    session.add(project)
    session.commit()
    
    # Add buildings and floors
    building = Building(building_name="Demo Building")
    session.add(building)
    session.commit()
    
    floor = Floor(floor_name="Ground Floor")
    session.add(floor)
    session.commit()
    
    # Add system types
    systype = SysType(sys_type="Desktop")
    session.add(systype)
    session.commit()
    
    # Add a demo asset
    asset = Asset(
        asset_name="DEMO-PC-001",
        project_id=project.project_id,
        building_id=building.building_id,
        floor_id=floor.floor_id,
        systype_id=systype.systype_id
    )
    session.add(asset)
    session.commit()
    
    print("✅ Demo database created with sample data")
'''
    
    scripts_dir = offline_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    with open(scripts_dir / "create_demo_db.py", "w") as f:
        f.write(db_script)
    print("✓ Created database script")

def create_readme(offline_dir):
    """Create README for the offline app."""
    readme_content = '''# IAMS Offline App

This is a self-contained offline version of the IAMS application.

## Quick Start

```bash
# Enter the offline app directory
cd offline_app

# Run the application
./run.sh
```

The app will start at http://localhost:3000

## Directory Structure

```
offline_app/
├── local_llama/        # Application code
├── .web/               # Frontend build
├── .uv-cache/          # UV Python package cache
├── offline_packages/   # Python wheel files
├── npm-offline-cache/  # NPM package cache
├── offline_mocks/      # Mock modules for offline mode
├── scripts/            # Utility scripts
├── config/             # Configuration files
├── demo_offline.db     # SQLite database
├── run.sh             # Main runner script
├── setup.sh           # Initial setup script
└── .env               # Environment variables
```

## Features

- Runs completely offline (no internet required)
- Uses SQLite instead of SQL Server
- Mock authentication (no Clerk needed)
- All dependencies cached locally
- Fast startup with UV package manager

## Troubleshooting

### Reset Database
```bash
rm demo_offline.db
python scripts/create_demo_db.py
```

### Reinstall Packages
```bash
rm -rf .venv
./setup.sh
```

### Port Already in Use
```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

## Moving to Another Machine

1. Copy the entire `offline_app` directory
2. Install UV on the target machine
3. Run `./run.sh`

No internet connection required!
'''
    
    with open(offline_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("✓ Created README.md")

def main():
    """Main function to create offline app directory."""
    print("=== Creating Offline App Directory ===\n")
    
    # Create directory structure
    offline_dir = create_directory_structure()
    
    # Copy files
    copy_application_files(offline_dir)
    copy_offline_components(offline_dir)
    
    # Create configurations
    create_offline_configs(offline_dir)
    
    # Create scripts
    create_scripts(offline_dir)
    
    # Create README
    create_readme(offline_dir)
    
    # Create a simple gitignore
    gitignore_content = """.venv/
*.pyc
__pycache__/
.DS_Store
*.log
"""
    with open(offline_dir / ".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("\n" + "="*50)
    print("✅ Offline App Directory Created Successfully!")
    print("="*50)
    print("\n📂 Location: ./offline_app/")
    print("\n🚀 To use:")
    print("   cd offline_app")
    print("   ./run.sh")
    print("\n📦 Everything needed for offline operation is contained within this directory.")
    print("💡 You can move this entire directory to any machine and run it offline.")

if __name__ == "__main__":
    main()