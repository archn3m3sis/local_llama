"""
Master seed file that combines all individual seed data files into a singular script.
This file must be updated after each seed data file addition to ensure all seed data 
can be executed in one script without errors.
"""

from sqlmodel import Session, create_engine, select
from local_llama.models.building import Building
from local_llama.models.floor import Floor
from local_llama.models.sys_type import SysType
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

def seed_floors():
    """Seed the Floor table with predefined floor data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Floor data to insert
    floors_data = [
        {"floor_name": "Floor 001"},
        {"floor_name": "Floor_002"},
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

def seed_systypes():
    """Seed the SysType table with predefined system type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # SysType data to insert
    systypes_data = [
        {"systype_name": "Desktop Workstation"},
        {"systype_name": "Laptop Workstation"},
        {"systype_name": "Server"},
        {"systype_name": "Digital Oscilloscope"},
        {"systype_name": "Signal Analyzer"},
        {"systype_name": "Network Analyzer"},
        {"systype_name": "Network Appliance"},
        {"systype_name": "Network Firewall"},
        {"systype_name": "Network Gateway"},
        {"systype_name": "Program Logic Controller"},
        {"systype_name": "Single Board Computer"},
    ]
    
    with Session(engine) as session:
        # Check if systypes already exist to avoid duplicates
        existing_systypes = session.exec(select(SysType)).all()
        existing_names = {systype.systype_name for systype in existing_systypes}
        
        systypes_to_add = []
        for systype_data in systypes_data:
            if systype_data["systype_name"] not in existing_names:
                systypes_to_add.append(SysType(**systype_data))
        
        if systypes_to_add:
            session.add_all(systypes_to_add)
            session.commit()
            print(f"Added {len(systypes_to_add)} system types to the database.")
        else:
            print("All system types already exist in the database.")

def run_all_seeds():
    """Run all seed functions in the correct order to avoid foreign key constraint errors."""
    print("Starting database seeding process...")
    
    # Run seed functions in dependency order
    seed_buildings()
    seed_floors()
    seed_systypes()
    
    print("Database seeding process completed.")

if __name__ == "__main__":
    run_all_seeds()