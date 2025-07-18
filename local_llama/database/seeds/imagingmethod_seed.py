from sqlmodel import Session, create_engine, select
from local_llama.models.imaging_method import ImagingMethod
import os
from dotenv import load_dotenv

load_dotenv()

def seed_imagingmethods():
    """Seed the ImagingMethod table with predefined imaging method data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # ImagingMethod data to insert
    imagingmethods_data = [
        {"img_method": "Acronis x86_64 WinPE-5.0"},
        {"img_method": "Acronix x86_64 WinPE-4.0"},
        {"img_method": "Acronis x86_64 WinPE-3.0"},
        {"img_method": "Acronis x86_64 WinPE-3.0"},
        {"img_method": "Acronis x86 WinPE 5.0"},
        {"img_method": "Acronis x86 WinPE 4.0"},
        {"img_method": "Acronis x86 WinPE 3.0"},
        {"img_method": "Acronis x86 WinPE-3.0"},
        {"img_method": "Acronis SCS Linux x86"},
        {"img_method": "Acronis SCS Linux x86_64"},
        {"img_method": "Norton Ghost x86"},
        {"img_method": "Windows Built In BakcupImage"},
        {"img_method": "Direct Drive Cloning"},
    ]
    
    with Session(engine) as session:
        # Check if imaging methods already exist to avoid duplicates
        existing_methods = session.exec(select(ImagingMethod)).all()
        existing_method_names = {method.img_method for method in existing_methods}
        
        methods_to_add = []
        for method_data in imagingmethods_data:
            if method_data["img_method"] not in existing_method_names:
                methods_to_add.append(ImagingMethod(**method_data))
        
        if methods_to_add:
            session.add_all(methods_to_add)
            session.commit()
            print(f"Added {len(methods_to_add)} imaging methods to the database.")
        else:
            print("All imaging methods already exist in the database.")

if __name__ == "__main__":
    seed_imagingmethods()