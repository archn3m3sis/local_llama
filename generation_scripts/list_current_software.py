#!/usr/bin/env python3
"""List current software in database to help with vendor mapping."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from local_llama.models import SoftwareCatalog

load_dotenv()

def list_software():
    """List all software currently in the database."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Get all software
        software_list = session.exec(
            select(SoftwareCatalog).order_by(SoftwareCatalog.sw_name)
        ).all()
        
        print(f"Total software entries: {len(software_list)}\n")
        
        print("Software in database:")
        print("-" * 80)
        for sw in software_list:
            vendor_status = "Has vendor" if sw.sw_vendor else "No vendor"
            print(f"{sw.sw_name:<60} | {vendor_status}")

if __name__ == "__main__":
    list_software()