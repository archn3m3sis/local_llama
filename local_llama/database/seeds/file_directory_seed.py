import os
import sys
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from sqlmodel import Session, create_engine, select
from datetime import datetime
from local_llama.models.file_storage import FileDirectory, DirectoryType
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("DATABASE_URL environment variable not set")
    exit(1)

engine = create_engine(database_url)

# Predefined directory structure
SYSTEM_DIRECTORIES = [
    # Root directories
    {
        "name": "playbook",
        "full_path": "/playbook",
        "description": "Root directory for all playbook documents",
        "icon": "book",
        "color": "#2563eb",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "sort_order": 1,
    },
    
    # Personal playbook directories
    {
        "name": "playbook_personal",
        "full_path": "/playbook/playbook_personal",
        "description": "Private/personal documents",
        "icon": "user",
        "color": "#7c3aed",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook",
        "sort_order": 1,
    },
    {
        "name": "pbper_drafts",
        "full_path": "/playbook/playbook_personal/pbper_drafts",
        "description": "Drafts not yet published",
        "icon": "file-text",
        "color": "#6366f1",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_personal",
        "sort_order": 1,
    },
    {
        "name": "pbper_templates",
        "full_path": "/playbook/playbook_personal/pbper_templates",
        "description": "Personal template storage",
        "icon": "layout-template",
        "color": "#8b5cf6",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_personal",
        "sort_order": 2,
    },
    {
        "name": "pbper_published",
        "full_path": "/playbook/playbook_personal/pbper_published",
        "description": "Personal publications/completed work",
        "icon": "check-circle",
        "color": "#10b981",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_personal",
        "sort_order": 3,
    },
    {
        "name": "pbper_fs",
        "full_path": "/playbook/playbook_personal/pbper_fs",
        "description": "Personal filesystem storage",
        "icon": "folder-open",
        "color": "#f59e0b",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_personal",
        "sort_order": 4,
        "can_create_subdirs": True,  # Users can create subdirectories here
    },
    
    # Public playbook directories
    {
        "name": "playbook_public",
        "full_path": "/playbook/playbook_public",
        "description": "Public/team documents",
        "icon": "users",
        "color": "#059669",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook",
        "sort_order": 2,
        "is_public": True,
    },
    {
        "name": "pbpub_wips",
        "full_path": "/playbook/playbook_public/pbpub_wips",
        "description": "Work in progress",
        "icon": "clock",
        "color": "#f97316",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public",
        "sort_order": 1,
        "is_public": True,
    },
    {
        "name": "pbpub_templates",
        "full_path": "/playbook/playbook_public/pbpub_templates",
        "description": "Public templates",
        "icon": "layout-template",
        "color": "#0891b2",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public",
        "sort_order": 2,
        "is_public": True,
    },
    {
        "name": "pbpub_articles",
        "full_path": "/playbook/playbook_public/pbpub_articles",
        "description": "Published articles",
        "icon": "newspaper",
        "color": "#be123c",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public",
        "sort_order": 3,
        "is_public": True,
    },
    {
        "name": "pbpub_documentation",
        "full_path": "/playbook/playbook_public/pbpub_documentation",
        "description": "System documentation",
        "icon": "book-open",
        "color": "#1e40af",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public",
        "sort_order": 4,
        "is_public": True,
    },
    
    # Documentation subcategories - matching the playbook page categories
    {
        "name": "incident_response",
        "full_path": "/playbook/playbook_public/pbpub_documentation/incident_response",
        "description": "Quick response procedures for security incidents",
        "icon": "shield-alert",
        "color": "#ef4444",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 1,
        "is_public": True,
    },
    {
        "name": "maintenance",
        "full_path": "/playbook/playbook_public/pbpub_documentation/maintenance",
        "description": "Routine maintenance and update procedures",
        "icon": "wrench",
        "color": "#10b981",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 2,
        "is_public": True,
    },
    {
        "name": "compliance",
        "full_path": "/playbook/playbook_public/pbpub_documentation/compliance",
        "description": "Regulatory compliance and audit procedures",
        "icon": "clipboard-check",
        "color": "#f59e0b",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 3,
        "is_public": True,
    },
    {
        "name": "emergency",
        "full_path": "/playbook/playbook_public/pbpub_documentation/emergency",
        "description": "Emergency response and disaster recovery",
        "icon": "siren",
        "color": "#8b5cf6",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 4,
        "is_public": True,
    },
    {
        "name": "security",
        "full_path": "/playbook/playbook_public/pbpub_documentation/security",
        "description": "Security protocols and access control procedures",
        "icon": "lock",
        "color": "#06b6d4",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 5,
        "is_public": True,
    },
    {
        "name": "standard_operating_procedures",
        "full_path": "/playbook/playbook_public/pbpub_documentation/standard_operating_procedures",
        "description": "Daily operational procedures and checklists",
        "icon": "settings",
        "color": "#ec4899",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 6,
        "is_public": True,
    },
    {
        "name": "training",
        "full_path": "/playbook/playbook_public/pbpub_documentation/training",
        "description": "Training materials and onboarding procedures",
        "icon": "graduation-cap",
        "color": "#14b8a6",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_documentation",
        "sort_order": 7,
        "is_public": True,
    },
    
    # Article subcategories
    {
        "name": "networking",
        "full_path": "/playbook/playbook_public/pbpub_articles/networking",
        "description": "Network infrastructure and protocols articles",
        "icon": "network",
        "color": "#3b82f6",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 1,
        "is_public": True,
    },
    {
        "name": "cybersecurity",
        "full_path": "/playbook/playbook_public/pbpub_articles/cybersecurity",
        "description": "Security best practices and threat analysis",
        "icon": "shield",
        "color": "#dc2626",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 2,
        "is_public": True,
    },
    {
        "name": "development",
        "full_path": "/playbook/playbook_public/pbpub_articles/development",
        "description": "Software development practices and tutorials",
        "icon": "code",
        "color": "#10b981",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 3,
        "is_public": True,
    },
    {
        "name": "career_development",
        "full_path": "/playbook/playbook_public/pbpub_articles/career_development",
        "description": "Professional growth and career advancement",
        "icon": "trending-up",
        "color": "#f59e0b",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 4,
        "is_public": True,
    },
    {
        "name": "emerging_tech",
        "full_path": "/playbook/playbook_public/pbpub_articles/emerging_tech",
        "description": "Latest technology trends and innovations",
        "icon": "zap",
        "color": "#8b5cf6",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 5,
        "is_public": True,
    },
    {
        "name": "hardware",
        "full_path": "/playbook/playbook_public/pbpub_articles/hardware",
        "description": "Hardware reviews and technical specifications",
        "icon": "cpu",
        "color": "#06b6d4",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 6,
        "is_public": True,
    },
    {
        "name": "software",
        "full_path": "/playbook/playbook_public/pbpub_articles/software",
        "description": "Software reviews and application guides",
        "icon": "package",
        "color": "#ec4899",
        "is_system_directory": True,
        "directory_type": DirectoryType.SYSTEM,
        "parent_path": "/playbook/playbook_public/pbpub_articles",
        "sort_order": 7,
        "is_public": True,
    },
]


def seed_file_directories():
    """Seed the file directory structure."""
    with Session(engine) as session:
        # Create a map to store directory references
        directory_map = {}
        
        for dir_data in SYSTEM_DIRECTORIES:
            # Check if directory already exists
            existing_dir = session.exec(
                select(FileDirectory).where(FileDirectory.full_path == dir_data["full_path"])
            ).first()
            
            if existing_dir:
                print(f"Directory already exists: {dir_data['full_path']}")
                directory_map[dir_data["full_path"]] = existing_dir
                continue
            
            # Get parent_id if parent_path is specified
            parent_id = None
            if "parent_path" in dir_data:
                parent_dir = directory_map.get(dir_data["parent_path"])
                if parent_dir:
                    parent_id = parent_dir.directory_id
                else:
                    print(f"Warning: Parent directory not found for {dir_data['full_path']}")
            
            # Remove parent_path from data (not a model field)
            dir_create_data = dir_data.copy()
            dir_create_data.pop("parent_path", None)
            
            # Set default values
            dir_create_data["parent_id"] = parent_id
            dir_create_data["owner_id"] = 1  # System user
            if "can_upload_files" not in dir_create_data:
                dir_create_data["can_upload_files"] = True
            if "can_create_subdirs" not in dir_create_data:
                dir_create_data["can_create_subdirs"] = False
            
            # Create the directory
            directory = FileDirectory(**dir_create_data)
            
            session.add(directory)
            session.flush()  # Get the directory_id
            
            directory_map[directory.full_path] = directory
            print(f"Created directory: {directory.full_path}")
        
        session.commit()
        print("File directory seeding completed!")


if __name__ == "__main__":
    seed_file_directories()