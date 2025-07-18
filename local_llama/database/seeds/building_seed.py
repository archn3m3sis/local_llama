from sqlmodel import Session, create_engine, select
from local_llama.models.building import Building
import os
from dotenv import load_dotenv

load_dotenv()

def seed_buildings():
    """Seed the Building table with predefined building data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Building data to insert
    buildings_data = [
        {"building_name": "Building 370"},
        {"building_name": "Building 377"},
        {"building_name": "Building 403"},
        {"building_name": "Building 350"},
        {"building_name": "Building 012"},
        {"building_name": "Building 014"},
        {"building_name": "Building 001"},
        {"building_name": "Building 010"},
    ]
    
    with Session(engine) as session:
        # Check if buildings already exist to avoid duplicates
        existing_buildings = session.exec(select(Building)).all()
        existing_names = {building.building_name for building in existing_buildings}
        
        buildings_to_add = []
        for building_data in buildings_data:
            if building_data["building_name"] not in existing_names:
                buildings_to_add.append(Building(**building_data))
        
        if buildings_to_add:
            session.add_all(buildings_to_add)
            session.commit()
            print(f"Added {len(buildings_to_add)} buildings to the database.")
        else:
            print("All buildings already exist in the database.")

if __name__ == "__main__":
    seed_buildings()