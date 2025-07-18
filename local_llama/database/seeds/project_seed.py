from sqlmodel import Session, create_engine, select
from local_llama.models.project import Project
import os
from dotenv import load_dotenv

load_dotenv()

def seed_projects():
    """Seed the Project table with predefined project data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Project data to insert
    projects_data = [
        {"project_name": "IFMC"},
        {"project_name": "SHIELD"},
        {"project_name": "STARE"},
        {"project_name": "STORM"},
        {"project_name": "MULTI"},
        {"project_name": "TAGM"},
    ]
    
    with Session(engine) as session:
        # Check if projects already exist to avoid duplicates
        existing_projects = session.exec(select(Project)).all()
        existing_names = {project.project_name for project in existing_projects}
        
        projects_to_add = []
        for project_data in projects_data:
            if project_data["project_name"] not in existing_names:
                projects_to_add.append(Project(**project_data))
        
        if projects_to_add:
            session.add_all(projects_to_add)
            session.commit()
            print(f"Added {len(projects_to_add)} projects to the database.")
        else:
            print("All projects already exist in the database.")

if __name__ == "__main__":
    seed_projects()