#!/usr/bin/env python3
"""Test storm.gearbox software pagination and counts."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, func
from local_llama.models import Asset, AssetSoftware, SoftwareCatalog, Project

load_dotenv()

def test_storm_gearbox():
    """Test storm.gearbox software counts and pagination."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Get storm.gearbox asset
        gearbox = session.exec(
            select(Asset).where(Asset.asset_name == "storm.gearbox")
        ).first()
        
        if not gearbox:
            print("storm.gearbox asset not found!")
            return
        
        print(f"Found storm.gearbox with asset_id: {gearbox.asset_id}")
        
        # Get project info
        project = session.exec(
            select(Project).where(Project.project_id == gearbox.project_id)
        ).first()
        print(f"Project: {project.project_name} (ID: {project.project_id})")
        
        # Count software for this asset
        software_count = session.exec(
            select(func.count(AssetSoftware.software_catalog_id)).where(
                AssetSoftware.asset_id == gearbox.asset_id
            )
        ).one()
        
        print(f"\nTotal software entries for storm.gearbox: {software_count}")
        
        # Get all software for this asset
        query = select(
            SoftwareCatalog.sw_name,
            AssetSoftware.installed_version
        ).join(
            AssetSoftware,
            SoftwareCatalog.software_catalog_id == AssetSoftware.software_catalog_id
        ).where(
            AssetSoftware.asset_id == gearbox.asset_id
        ).order_by(
            SoftwareCatalog.sw_name
        )
        
        results = session.exec(query).all()
        
        print(f"\nAll software for storm.gearbox (sorted by name):")
        print("-" * 80)
        for i, (name, version) in enumerate(results, 1):
            print(f"{i:3d}. {name:<50} | Version: {version or 'N/A'}")
        
        # Test pagination
        print(f"\n\nPagination Test (20 items per page):")
        print("-" * 80)
        
        items_per_page = 20
        total_pages = (software_count + items_per_page - 1) // items_per_page
        
        for page in range(1, total_pages + 1):
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, software_count)
            print(f"Page {page}/{total_pages}: Showing items {start_idx + 1}-{end_idx} of {software_count}")

if __name__ == "__main__":
    test_storm_gearbox()