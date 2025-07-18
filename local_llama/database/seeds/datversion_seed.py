from sqlmodel import Session, create_engine, select
from local_llama.models.dat_version import DatVersion
import os
from dotenv import load_dotenv

load_dotenv()

def seed_datversions():
    """Seed the DatVersion table with predefined DAT version data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # DatVersion data to insert
    datversions_data = [
        {"datversion_name": "Version02 Datfiles", "avversion_id": 1},
        {"datversion_name": "Version03 Datfiles", "avversion_id": 2},
    ]
    
    with Session(engine) as session:
        # Check if DAT versions already exist to avoid duplicates
        existing_datversions = session.exec(select(DatVersion)).all()
        existing_datversion_names = {dv.datversion_name for dv in existing_datversions}
        
        datversions_to_add = []
        for dat_data in datversions_data:
            if dat_data["datversion_name"] not in existing_datversion_names:
                datversions_to_add.append(DatVersion(**dat_data))
        
        if datversions_to_add:
            session.add_all(datversions_to_add)
            session.commit()
            print(f"Added {len(datversions_to_add)} DAT versions to the database.")
        else:
            print("All DAT versions already exist in the database.")

if __name__ == "__main__":
    seed_datversions()