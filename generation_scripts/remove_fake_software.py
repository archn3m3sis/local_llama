#!/usr/bin/env python3
"""Remove fake software entries that were not part of the storm.gearbox import."""

import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, delete
from local_llama.models import SoftwareCatalog, AssetSoftware

load_dotenv()

# These are the fake entries from software_catalog_seed.py that should be removed
FAKE_SOFTWARE_NAMES = [
    "Microsoft Windows 10 Enterprise",
    "Microsoft Windows 11 Enterprise", 
    "Red Hat Enterprise Linux",
    "McAfee Endpoint Security",
    "Symantec Endpoint Protection",
    "Microsoft Office Professional Plus 2021",
    "Adobe Acrobat Pro DC",
    "Microsoft Visual Studio Enterprise",
    "Python",
    "Microsoft SQL Server Enterprise",
    "PostgreSQL",
    "7-Zip",
    "PuTTY",
    "NVIDIA Graphics Driver",
    "Dell BIOS Update",
    "VMware vSphere ESXi",
    "Microsoft Hyper-V Server",
    "SolarWinds Network Performance Monitor"
]

def remove_fake_software():
    """Remove fake software entries."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Count before removal
        total_before = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
        ).one()
        print(f"Total software entries before removal: {total_before}")
        
        removed_count = 0
        for fake_name in FAKE_SOFTWARE_NAMES:
            # Find the software entry
            software = session.exec(
                select(SoftwareCatalog).where(SoftwareCatalog.sw_name == fake_name)
            ).first()
            
            if software:
                # First remove any AssetSoftware relationships
                session.exec(
                    delete(AssetSoftware).where(
                        AssetSoftware.software_catalog_id == software.software_catalog_id
                    )
                )
                
                # Then remove the software entry
                session.delete(software)
                removed_count += 1
                print(f"Removed: {fake_name}")
        
        session.commit()
        
        # Count after removal
        total_after = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
        ).one()
        
        print(f"\nRemoved {removed_count} fake software entries")
        print(f"Total software entries after removal: {total_after}")

if __name__ == "__main__":
    from sqlmodel import func
    remove_fake_software()