from sqlmodel import Session, create_engine, select
from local_llama.models.privilege_level import PrivilegeLevel
import os
from dotenv import load_dotenv

load_dotenv()

def seed_privilegelevels():
    """Seed the PrivilegeLevel table with predefined privilege level data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # PrivilegeLevel data to insert
    privilegelevels_data = [
        {"priv_name": "Standard User", "priv_description": ""},
        {"priv_name": "Power User", "priv_description": ""},
        {"priv_name": "Administrator", "priv_description": ""},
    ]
    
    with Session(engine) as session:
        # Check if privilege levels already exist to avoid duplicates
        existing_privilegelevels = session.exec(select(PrivilegeLevel)).all()
        existing_priv_names = {priv.priv_name for priv in existing_privilegelevels}
        
        privilegelevels_to_add = []
        for priv_data in privilegelevels_data:
            if priv_data["priv_name"] not in existing_priv_names:
                privilegelevels_to_add.append(PrivilegeLevel(**priv_data))
        
        if privilegelevels_to_add:
            session.add_all(privilegelevels_to_add)
            session.commit()
            print(f"Added {len(privilegelevels_to_add)} privilege levels to the database.")
        else:
            print("All privilege levels already exist in the database.")

if __name__ == "__main__":
    seed_privilegelevels()