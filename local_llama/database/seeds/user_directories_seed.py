import os
import sys
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from sqlmodel import Session, create_engine, select
from datetime import datetime
from local_llama.models.file_storage import FileDirectory, DirectoryType
from local_llama.models.employee import Employee
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("DATABASE_URL environment variable not set")
    exit(1)

engine = create_engine(database_url)


def create_user_directories():
    """Create personal directory structure for each cybersecurity team member."""
    
    with Session(engine) as session:
        # First, rename the existing playbook_personal to users if it exists
        personal_dir = session.exec(
            select(FileDirectory).where(FileDirectory.full_path == "/playbook/playbook_personal")
        ).first()
        
        if personal_dir:
            # Update existing personal directory to become the users container
            personal_dir.name = "users"
            personal_dir.full_path = "/playbook/users"
            personal_dir.description = "User personal workspaces"
            personal_dir.icon = "users"
            session.add(personal_dir)
            session.commit()
            print("Updated existing playbook_personal to users directory")
            
            # Delete old personal subdirectories
            old_personal_dirs = session.exec(
                select(FileDirectory).where(
                    FileDirectory.full_path.startswith("/playbook/playbook_personal/")
                )
            ).all()
            
            for old_dir in old_personal_dirs:
                session.delete(old_dir)
            session.commit()
            print(f"Removed {len(old_personal_dirs)} old personal subdirectories")
        else:
            # Create new users directory
            users_dir = FileDirectory(
                name="users",
                full_path="/playbook/users",
                description="User personal workspaces",
                icon="users",
                color="#7c3aed",
                is_system_directory=True,
                directory_type=DirectoryType.SYSTEM,
                parent_id=session.exec(
                    select(FileDirectory).where(FileDirectory.full_path == "/playbook")
                ).first().directory_id,
                sort_order=1,
                can_create_subdirs=False,  # Only system can create user dirs here
                can_upload_files=False,
            )
            session.add(users_dir)
            session.commit()
            print("Created new users directory")
        
        # Get the users directory
        users_dir = session.exec(
            select(FileDirectory).where(FileDirectory.full_path == "/playbook/users")
        ).first()
        
        # Get all cybersecurity employees (department_id = 2) and cybersecurity management
        cyber_employees = session.exec(
            select(Employee).where(
                (Employee.department_id == 2) |  # Cybersecurity department
                (Employee.email == "robert.shipp.2.civ@army.mil")  # Robert Shipp - Cybersecurity Manager
            )
        ).all()
        
        print(f"Found {len(cyber_employees)} cybersecurity team members")
        
        # Personal subdirectory templates
        personal_subdirs = [
            {
                "name": "drafts",
                "description": "Work in progress documents",
                "icon": "file-text",
                "color": "#6366f1",
                "sort_order": 1,
            },
            {
                "name": "templates",
                "description": "Personal document templates",
                "icon": "layout-template", 
                "color": "#8b5cf6",
                "sort_order": 2,
            },
            {
                "name": "published",
                "description": "Completed and published documents",
                "icon": "check-circle",
                "color": "#10b981",
                "sort_order": 3,
            },
            {
                "name": "filesystem",
                "description": "General file storage",
                "icon": "folder-open",
                "color": "#f59e0b",
                "sort_order": 4,
                "can_create_subdirs": True,  # Users can create subdirs here
            },
        ]
        
        # Create personal directory structure for each cybersecurity employee
        for employee in cyber_employees:
            # Create username from first_last format
            username = f"{employee.first_name.lower()}_{employee.last_name.lower()}"
            user_dir_path = f"/playbook/users/{username}"
            
            # Check if user directory already exists
            existing_user_dir = session.exec(
                select(FileDirectory).where(FileDirectory.full_path == user_dir_path)
            ).first()
            
            if existing_user_dir:
                print(f"User directory already exists for {employee.first_name} {employee.last_name}")
                continue
            
            # Create user's personal root directory
            user_dir = FileDirectory(
                name=username,
                full_path=user_dir_path,
                description=f"Personal workspace for {employee.first_name} {employee.last_name}",
                icon="user",
                color="#7c3aed",
                is_system_directory=True,  # Protect from accidental deletion
                directory_type=DirectoryType.SYSTEM,
                owner_id=employee.id,
                parent_id=users_dir.directory_id,
                is_public=False,
                can_create_subdirs=False,  # Subdirs are predefined
                can_upload_files=False,  # Files go in subdirs
                sort_order=employee.id,
            )
            session.add(user_dir)
            session.flush()  # Get the directory_id
            
            print(f"Created personal directory for {employee.first_name} {employee.last_name}")
            
            # Create subdirectories for this user
            for subdir_template in personal_subdirs:
                subdir_data = subdir_template.copy()
                subdir_data.update({
                    "full_path": f"{user_dir_path}/{subdir_data['name']}",
                    "parent_id": user_dir.directory_id,
                    "directory_type": DirectoryType.SYSTEM,
                    "is_system_directory": True,
                    "owner_id": employee.id,
                    "is_public": False,
                    "can_upload_files": True,
                    "can_create_subdirs": subdir_data.get("can_create_subdirs", False),
                })
                
                subdir = FileDirectory(**subdir_data)
                session.add(subdir)
            
            print(f"  Created {len(personal_subdirs)} subdirectories for {username}")
        
        # Update the public directory path
        public_dir = session.exec(
            select(FileDirectory).where(FileDirectory.full_path == "/playbook/playbook_public")
        ).first()
        
        if public_dir:
            public_dir.name = "public"
            public_dir.full_path = "/playbook/public"
            public_dir.sort_order = 2
            session.add(public_dir)
            
            # Update all child paths
            public_children = session.exec(
                select(FileDirectory).where(
                    FileDirectory.full_path.startswith("/playbook/playbook_public/")
                )
            ).all()
            
            for child in public_children:
                child.full_path = child.full_path.replace("/playbook/playbook_public", "/playbook/public")
                # Remove pbpub_ prefix from names for cleaner look
                if child.name.startswith("pbpub_"):
                    child.name = child.name[6:]  # Remove pbpub_ prefix
                session.add(child)
            
            print(f"Updated public directory and {len(public_children)} child directories")
        
        session.commit()
        print("\nUser directory structure creation completed!")
        
        # Display summary
        all_user_dirs = session.exec(
            select(FileDirectory).where(
                FileDirectory.full_path.startswith("/playbook/users/")
            ).order_by(FileDirectory.full_path)
        ).all()
        
        print(f"\nTotal user directories created: {len(all_user_dirs)}")
        current_user = None
        for dir in all_user_dirs:
            if dir.owner_id != current_user:
                current_user = dir.owner_id
                owner = session.get(Employee, current_user)
                if owner:
                    print(f"\n{owner.first_name} {owner.last_name}:")
            print(f"  {dir.full_path}")


if __name__ == "__main__":
    create_user_directories()