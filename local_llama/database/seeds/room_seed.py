from sqlmodel import Session, create_engine, select
from local_llama.models.room import Room
import os
from dotenv import load_dotenv

load_dotenv()

def seed_rooms():
    """Seed the Room table with predefined room data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Room data to insert (building_id, floor_id, room_name)
    rooms_data = [
        {"building_id": 1, "floor_id": 8, "room_name": "Gets PTCI / Test Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "Hawk DTE / Test Console Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "Steve Moritz Power Supply Test Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "201 / CRG ECT ICC & Radar Staging Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "201 / Hawk HFC / DTE Support Equipment Area"},
        {"building_id": 1, "floor_id": 7, "room_name": "AGPU Pump Area"},
        {"building_id": 1, "floor_id": 7, "room_name": "Hoist Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Boom Extension Test Set Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable & Harness Test Set Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable & Harness Fiber Optics Cell Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "DITMCO / User Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable Harness Wire Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Element Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Coolant Resevoir Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Hawk / Patriot Mechanical Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Circuit Card Rear Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Circuit Card Microwave Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Radar Antenna Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Avenger LRU Disassembly Area"},
        {"building_id": 2, "floor_id": 9, "room_name": "Multi Project Dip Tank Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "High Power Room"},
        {"building_id": 1, "floor_id": 9, "room_name": "Traversing Unit Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "IFTE Test Console Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Avenger Flir ODU Production Area"},
    ]
    
    with Session(engine) as session:
        # Check if rooms already exist to avoid duplicates
        existing_rooms = session.exec(select(Room)).all()
        existing_combinations = {(room.building_id, room.floor_id, room.room_name) for room in existing_rooms}
        
        rooms_to_add = []
        for room_data in rooms_data:
            room_combination = (room_data["building_id"], room_data["floor_id"], room_data["room_name"])
            if room_combination not in existing_combinations:
                rooms_to_add.append(Room(**room_data))
        
        if rooms_to_add:
            session.add_all(rooms_to_add)
            session.commit()
            print(f"Added {len(rooms_to_add)} rooms to the database.")
        else:
            print("All rooms already exist in the database.")

if __name__ == "__main__":
    seed_rooms()