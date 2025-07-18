from sqlmodel import Session, create_engine, select
from local_llama.models.app_user import AppUser
import os
from dotenv import load_dotenv

load_dotenv()

def seed_appusers():
    """Seed the AppUser table with predefined application user data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # AppUser data to insert (id will be auto-generated)
    appusers_data = [
        {"first_name": "Kyle", "last_name": "Hurston", "email": "kyle.m.hurston.civ@army.mil", "phone": None, "employee_id": 1, "department_id": 2, "priv_level_id": 3},
        {"first_name": "David", "last_name": "Felmlee", "email": "david.felmlee.civ@army.mil", "phone": None, "employee_id": 2, "department_id": 2, "priv_level_id": 3},
        {"first_name": "Robert", "last_name": "Shipp", "email": "robert.shipp.2.civ@army.mil", "phone": None, "employee_id": 3, "department_id": 5, "priv_level_id": 3},
        {"first_name": "Mary", "last_name": "Steigerwald", "email": "mary.steigerwald.civ@army.mil", "phone": None, "employee_id": 4, "department_id": 5, "priv_level_id": 3},
        {"first_name": "Craig", "last_name": "Alleman", "email": "craig.alleman.civ@army.mil", "phone": None, "employee_id": 5, "department_id": 2, "priv_level_id": 3},
        {"first_name": "Justin", "last_name": "Ile", "email": "justin.ile.civ@army.mil", "phone": None, "employee_id": 6, "department_id": 6, "priv_level_id": 2},
        {"first_name": "Tim", "last_name": "Rhoades", "email": "tim.rhoades.civ@army.mil", "phone": None, "employee_id": 7, "department_id": 6, "priv_level_id": 2},
        {"first_name": "Tim", "last_name": "Blacker", "email": "tim.blacker.civ@army.mil", "phone": None, "employee_id": 8, "department_id": 6, "priv_level_id": 1},
        {"first_name": "Barry", "last_name": "Crawford", "email": "barry.crawford.civ@army.mil", "phone": None, "employee_id": 9, "department_id": 4, "priv_level_id": 3},
    ]
    
    with Session(engine) as session:
        # Check if app users already exist to avoid duplicates
        existing_appusers = session.exec(select(AppUser)).all()
        existing_emails = {user.email for user in existing_appusers}
        
        appusers_to_add = []
        for user_data in appusers_data:
            if user_data["email"] not in existing_emails:
                appusers_to_add.append(AppUser(**user_data))
        
        if appusers_to_add:
            session.add_all(appusers_to_add)
            session.commit()
            print(f"Added {len(appusers_to_add)} app users to the database.")
        else:
            print("All app users already exist in the database.")

if __name__ == "__main__":
    seed_appusers()