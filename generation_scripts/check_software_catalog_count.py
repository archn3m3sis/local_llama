#!/usr/bin/env python3
"""Check total software entries in the catalog."""

import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, func
from local_llama.models import SoftwareCatalog

load_dotenv()

def check_catalog():
    """Check software catalog entries."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Count total entries in catalog
        total_count = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
        ).one()
        
        print(f"Total software entries in catalog: {total_count}")
        
        # Show first 20 entries
        catalog_entries = session.exec(
            select(SoftwareCatalog).limit(20)
        ).all()
        
        print("\nFirst 20 entries in catalog:")
        print("-" * 80)
        for sw in catalog_entries:
            print(f"{sw.sw_name:<50} | Category: {sw.sw_category or 'N/A'}")

if __name__ == "__main__":
    check_catalog()