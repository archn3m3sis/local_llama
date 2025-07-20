import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from sqlmodel import Session, create_engine, select
from local_llama.models.vm_type import VMType
from dotenv import load_dotenv

load_dotenv()

def seed_vmtypes():
    """Seed the VMType table with predefined virtual machine type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VMType data to insert
    vmtypes_data = [
        {"vm_type": "HyperV Virtual Machine Type 1"},
        {"vm_type": "HyperV Virtual Machine Type 2"},
    ]
    
    with Session(engine) as session:
        # Check if vmtypes already exist to avoid duplicates
        existing_vmtypes = session.exec(select(VMType)).all()
        existing_types = {vmtype.vm_type for vmtype in existing_vmtypes}
        
        vmtypes_to_add = []
        for vmtype_data in vmtypes_data:
            if vmtype_data["vm_type"] not in existing_types:
                vmtypes_to_add.append(VMType(**vmtype_data))
        
        if vmtypes_to_add:
            session.add_all(vmtypes_to_add)
            session.commit()
            print(f"Added {len(vmtypes_to_add)} VM types to the database.")
        else:
            print("All VM types already exist in the database.")

if __name__ == "__main__":
    seed_vmtypes()