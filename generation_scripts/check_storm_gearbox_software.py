#!/usr/bin/env python3
"""Check how many software entries are associated with storm.gearbox asset."""

import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, func
from local_llama.models import Asset, AssetSoftware, SoftwareCatalog, SWManufacturer

load_dotenv()

def check_storm_gearbox_software():
    """Check software entries for storm.gearbox."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Find storm.gearbox asset
        asset = session.exec(
            select(Asset).where(Asset.asset_name == "storm.gearbox")
        ).first()
        
        if not asset:
            print("storm.gearbox asset not found in database")
            return
        
        print(f"Found storm.gearbox asset with ID: {asset.asset_id}")
        
        # Get project info
        from local_llama.models import Project
        project = session.exec(
            select(Project).where(Project.project_id == asset.project_id)
        ).first()
        
        if project:
            print(f"Asset belongs to project: {project.project_name} (ID: {project.project_id})")
        
        # Count software entries
        software_count = session.exec(
            select(func.count(AssetSoftware.asset_software_id)).where(
                AssetSoftware.asset_id == asset.asset_id
            )
        ).one()
        
        print(f"\nTotal software entries for storm.gearbox: {software_count}")
        
        # Get first 10 software entries with details
        query = select(
            SoftwareCatalog.sw_name,
            AssetSoftware.installed_version,
            SWManufacturer.swmanu_name
        ).join(
            AssetSoftware,
            SoftwareCatalog.software_catalog_id == AssetSoftware.software_catalog_id
        ).join(
            SWManufacturer,
            SoftwareCatalog.sw_vendor == SWManufacturer.swmanu_id
        ).where(
            AssetSoftware.asset_id == asset.asset_id
        ).limit(10)
        
        results = session.exec(query).all()
        
        print("\nFirst 10 software entries:")
        print("-" * 80)
        for sw_name, version, vendor in results:
            print(f"{sw_name:<40} | {version or 'N/A':<15} | {vendor}")
        
        if software_count > 10:
            print(f"\n... and {software_count - 10} more entries")
        
        # Check if any have null installed_version
        null_version_count = session.exec(
            select(func.count(AssetSoftware.asset_software_id)).where(
                AssetSoftware.asset_id == asset.asset_id,
                AssetSoftware.installed_version == None
            )
        ).one()
        
        print(f"\nEntries with null version: {null_version_count}")

if __name__ == "__main__":
    check_storm_gearbox_software()