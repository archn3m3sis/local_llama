from sqlmodel import Session, create_engine, select
from local_llama.models.department import Department
import os
from dotenv import load_dotenv

load_dotenv()

def seed_departments():
    """Seed the Department table with predefined department data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Department data to insert
    departments_data = [
        {"dept_name": "System Administrators", "dept_description": ""},
        {"dept_name": "Cybersecurity", "dept_description": ""},
        {"dept_name": "Applications", "dept_description": ""},
        {"dept_name": "Database Administrators", "dept_description": ""},
        {"dept_name": "Management", "dept_description": ""},
        {"dept_name": "Test Equipment Maintenance", "dept_description": ""},
        {"dept_name": "Network Engineers", "dept_description": ""},
    ]
    
    with Session(engine) as session:
        # Check if departments already exist to avoid duplicates
        existing_departments = session.exec(select(Department)).all()
        existing_dept_names = {dept.dept_name for dept in existing_departments}
        
        departments_to_add = []
        for dept_data in departments_data:
            if dept_data["dept_name"] not in existing_dept_names:
                departments_to_add.append(Department(**dept_data))
        
        if departments_to_add:
            session.add_all(departments_to_add)
            session.commit()
            print(f"Added {len(departments_to_add)} departments to the database.")
        else:
            print("All departments already exist in the database.")

if __name__ == "__main__":
    seed_departments()