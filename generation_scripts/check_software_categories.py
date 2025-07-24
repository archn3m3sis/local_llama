#!/usr/bin/env python3
"""Check software categories in the database."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, func
from local_llama.models import SoftwareCatalog

load_dotenv()

def check_categories():
    """Check all unique categories in the software catalog."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Get all unique categories
        categories = session.exec(
            select(SoftwareCatalog.sw_category, func.count(SoftwareCatalog.software_catalog_id))
            .group_by(SoftwareCatalog.sw_category)
            .order_by(SoftwareCatalog.sw_category)
        ).all()
        
        print("Software Categories:")
        print("-" * 50)
        for category, count in categories:
            cat_display = category if category else "NULL/None"
            print(f"{cat_display:<30} | Count: {count}")
        
        # Check compliance status
        print("\nCompliance Status:")
        print("-" * 50)
        compliant_count = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
            .where(SoftwareCatalog.dod_compliant == True)
        ).one()
        
        non_compliant_count = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
            .where(SoftwareCatalog.dod_compliant == False)
        ).one()
        
        null_compliant_count = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id))
            .where(SoftwareCatalog.dod_compliant.is_(None))
        ).one()
        
        print(f"DoD Compliant: {compliant_count}")
        print(f"Non-Compliant: {non_compliant_count}")
        print(f"Unknown (NULL): {null_compliant_count}")

if __name__ == "__main__":
    check_categories()