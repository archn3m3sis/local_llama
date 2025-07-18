from sqlmodel import Session, create_engine, select
from local_llama.models.floor import Floor
import os
from dotenv import load_dotenv

load_dotenv()

def seed_floors():
    """Seed the Floor table with predefined floor data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Floor data to insert (generic floor levels)
    floors_data = [
        {"floor_name": "Floor 001"},
        {"floor_name": "Floor 002"},
        {"floor_name": "Floor Ground"},
    ]
    
    with Session(engine) as session:
        # Check if floors already exist to avoid duplicates
        existing_floors = session.exec(select(Floor)).all()
        existing_names = {floor.floor_name for floor in existing_floors}
        
        floors_to_add = []
        for floor_data in floors_data:
            if floor_data["floor_name"] not in existing_names:
                floors_to_add.append(Floor(**floor_data))
        
        if floors_to_add:
            session.add_all(floors_to_add)
            session.commit()
            print(f"Added {len(floors_to_add)} floors to the database.")
        else:
            print("All floors already exist in the database.")

if __name__ == "__main__":
    seed_floors()