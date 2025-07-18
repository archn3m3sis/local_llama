from sqlmodel import Session, create_engine, select
from local_llama.models.employee import Employee
import os
from dotenv import load_dotenv

load_dotenv()

def seed_employees():
    """Seed the Employee table with predefined employee data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Employee data to insert (id will be auto-generated)
    employees_data = [
        {"first_name": "Kyle", "last_name": "Hurston", "email": "kyle.m.civ@army.mil", "department_id": 2},
        {"first_name": "David", "last_name": "Felmlee", "email": "david.felmlee.civ@army.mil", "department_id": 2},
        {"first_name": "Robert", "last_name": "Shipp", "email": "robert.shipp.2.civ@army.mil", "department_id": 5},
        {"first_name": "Mary", "last_name": "Steigerwald", "email": "mary.steigerwald.civ@army.mil", "department_id": 5},
        {"first_name": "Craig", "last_name": "Alleman", "email": "craig.alleman.civ@army.mil", "department_id": 2},
        {"first_name": "Justin", "last_name": "Ile", "email": "justin.ile.civ@army.mil", "department_id": 6},
        {"first_name": "Tim", "last_name": "Rhoades", "email": "tim.rhoades.civ@army.mil", "department_id": 6},
        {"first_name": "Tim", "last_name": "Blacker", "email": "tim.blacker.civ@army.mil", "department_id": 6},
        {"first_name": "Barry", "last_name": "Crawford", "email": "barry.crawford.civ@army.mil", "department_id": 4},
    ]
    
    with Session(engine) as session:
        # Check if employees already exist to avoid duplicates
        existing_employees = session.exec(select(Employee)).all()
        existing_emails = {emp.email for emp in existing_employees}
        
        employees_to_add = []
        for emp_data in employees_data:
            if emp_data["email"] not in existing_emails:
                employees_to_add.append(Employee(**emp_data))
        
        if employees_to_add:
            session.add_all(employees_to_add)
            session.commit()
            print(f"Added {len(employees_to_add)} employees to the database.")
        else:
            print("All employees already exist in the database.")

if __name__ == "__main__":
    seed_employees()