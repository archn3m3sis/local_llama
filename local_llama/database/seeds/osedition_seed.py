from sqlmodel import Session, create_engine, select
from local_llama.models.os_edition import OSEdition
import os
from dotenv import load_dotenv

load_dotenv()

def seed_oseditions():
    """Seed the OSEdition table with predefined OS edition data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # OS Edition data to insert (edition_name)
    oseditions_data = [
        {"osedition_name": "Standard"},
        {"osedition_name": "OEM"},
        {"osedition_name": "OSR2"},
        {"osedition_name": "First Edition"},
        {"osedition_name": "Second Edition"},
        {"osedition_name": "Workstation"},
        {"osedition_name": "Server"},
        {"osedition_name": "Server Enterprise"},
        {"osedition_name": "Terminal Server"},
        {"osedition_name": "Professional"},
        {"osedition_name": "Advanced Server"},
        {"osedition_name": "Datacenter Server"},
        {"osedition_name": "Home"},
        {"osedition_name": "Media Center"},
        {"osedition_name": "Tablet PC"},
        {"osedition_name": "Starter"},
        {"osedition_name": "Embedded"},
        {"osedition_name": "Professional x64"},
        {"osedition_name": "Home Basic"},
        {"osedition_name": "Home Premium"},
        {"osedition_name": "Business"},
        {"osedition_name": "Enterprise"},
        {"osedition_name": "Ultimate"},
        {"osedition_name": "Core"},
        {"osedition_name": "Pro"},
        {"osedition_name": "RT"},
        {"osedition_name": "Education"},
        {"osedition_name": "Pro Education"},
        {"osedition_name": "Pro for Workstations"},
        {"osedition_name": "S"},
        {"osedition_name": "IoT Core"},
        {"osedition_name": "IoT Enterprise"},
        {"osedition_name": "Pocket PC"},
        {"osedition_name": "AutoPC"},
        {"osedition_name": "Handheld PC"},
        {"osedition_name": "Smartphone"},
        {"osedition_name": "Desktop"},
        {"osedition_name": "LTS"},
        {"osedition_name": "Cloud"},
        {"osedition_name": "Workstation"},
        {"osedition_name": "LMDE"},
        {"osedition_name": "GNOME"},
        {"osedition_name": "KDE"},
        {"osedition_name": "XFCE"},
        {"osedition_name": "Lite"},
        {"osedition_name": "Flex"},
        {"osedition_name": "Home"},
        {"osedition_name": "Security"},
    ]
    
    with Session(engine) as session:
        # Check if OS editions already exist to avoid duplicates
        existing_oseditions = session.exec(select(OSEdition)).all()
        existing_names = {osedition.osedition_name for osedition in existing_oseditions}
        
        oseditions_to_add = []
        for osedition_data in oseditions_data:
            if osedition_data["osedition_name"] not in existing_names:
                oseditions_to_add.append(OSEdition(**osedition_data))
        
        if oseditions_to_add:
            session.add_all(oseditions_to_add)
            session.commit()
            print(f"Added {len(oseditions_to_add)} OS editions to the database.")
        else:
            print("All OS editions already exist in the database.")

if __name__ == "__main__":
    seed_oseditions()