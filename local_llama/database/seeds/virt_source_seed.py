import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from sqlmodel import Session, create_engine, select
from local_llama.models.virt_source import VirtualizationSource
from dotenv import load_dotenv

load_dotenv()

def seed_virtualization_sources():
    """Seed the VirtualizationSource table with predefined virtualization source data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VirtualizationSource data to insert
    virtualization_sources_data = [
        {"virt_source": "UHA Virtualization Server"},
        {"virt_source": "UHB Virtualization Server"},
    ]
    
    with Session(engine) as session:
        # Check if virtualization sources already exist to avoid duplicates
        existing_sources = session.exec(select(VirtualizationSource)).all()
        existing_source_names = {source.virt_source for source in existing_sources}
        
        sources_to_add = []
        for source_data in virtualization_sources_data:
            if source_data["virt_source"] not in existing_source_names:
                sources_to_add.append(VirtualizationSource(**source_data))
        
        if sources_to_add:
            session.add_all(sources_to_add)
            session.commit()
            print(f"Added {len(sources_to_add)} virtualization sources to the database.")
        else:
            print("All virtualization sources already exist in the database.")

if __name__ == "__main__":
    seed_virtualization_sources()