import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from sqlmodel import Session, create_engine, select
from local_llama.models.vm_status import VMStatus
from dotenv import load_dotenv

load_dotenv()

def seed_vm_statuses():
    """Seed the VMStatus table with predefined VM status data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VMStatus data to insert
    vm_statuses_data = [
        {"vm_status": "Fully Functional | Ready For Use"},
        {"vm_status": "Fully Functional | Waiting For Scans"},
        {"vm_status": "Machine Created | Testing Startup Processes"},
        {"vm_status": "Non-Functional VM | Boot Sequence Errors"},
        {"vm_status": "Non-Functional VM | Driver Related Errors"},
        {"vm_status": "Non-Functional VM | Unknown Virtualization Errors"},
        {"vm_status": "Non-Functional VM | Data Available For Extraction At Request"},
    ]
    
    with Session(engine) as session:
        # Check if VM statuses already exist to avoid duplicates
        existing_statuses = session.exec(select(VMStatus)).all()
        existing_status_names = {status.vm_status for status in existing_statuses}
        
        statuses_to_add = []
        for status_data in vm_statuses_data:
            if status_data["vm_status"] not in existing_status_names:
                statuses_to_add.append(VMStatus(**status_data))
        
        if statuses_to_add:
            session.add_all(statuses_to_add)
            session.commit()
            print(f"Added {len(statuses_to_add)} VM statuses to the database.")
        else:
            print("All VM statuses already exist in the database.")

if __name__ == "__main__":
    seed_vm_statuses()