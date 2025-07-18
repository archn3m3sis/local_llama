from sqlmodel import Session, create_engine, select
from local_llama.models.sys_type import SysType
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    seed_systypes()