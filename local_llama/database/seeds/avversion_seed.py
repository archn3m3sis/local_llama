from sqlmodel import Session, create_engine, select
from local_llama.models.av_version import AVVersion
import os
from dotenv import load_dotenv

load_dotenv()

def seed_avversions():
    """Seed the AVVersion table with predefined antivirus version data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # AVVersion data to insert
    avversions_data = [
        {"av_version": "Version 2", "av_description": "McAfee VirusScan Enterprise"},
        {"av_version": "Version 3", "av_description": "Trellix Endpoint Security"},
    ]
    
    with Session(engine) as session:
        # Check if AV versions already exist to avoid duplicates
        existing_avversions = session.exec(select(AVVersion)).all()
        existing_av_versions = {av.av_version for av in existing_avversions}
        
        avversions_to_add = []
        for av_data in avversions_data:
            if av_data["av_version"] not in existing_av_versions:
                avversions_to_add.append(AVVersion(**av_data))
        
        if avversions_to_add:
            session.add_all(avversions_to_add)
            session.commit()
            print(f"Added {len(avversions_to_add)} AV versions to the database.")
        else:
            print("All AV versions already exist in the database.")

if __name__ == "__main__":
    seed_avversions()