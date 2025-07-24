#!/usr/bin/env python3
"""Debug script to investigate software display issue on Configuration Management page"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select, func, create_engine
from local_llama.models import SoftwareCatalog, AssetSoftware, Asset, InstalledSoftware
from dotenv import load_dotenv

load_dotenv()

def debug_software_display():
    """Debug software display issues"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        print("=== SOFTWARE DISPLAY DEBUG ===\n")
        
        # 1. Check total software count in SoftwareCatalog
        total_count = session.exec(select(func.count(SoftwareCatalog.software_catalog_id))).one()
        print(f"1. Total SoftwareCatalog entries: {total_count}")
        
        # 2. List first 10 software entries
        print("\n2. First 10 SoftwareCatalog entries:")
        software_query = select(SoftwareCatalog).limit(10)
        software_items = session.exec(software_query).all()
        for idx, sw in enumerate(software_items, 1):
            print(f"   {idx}. ID: {sw.software_catalog_id}, Name: {sw.sw_name}, Version: {sw.latest_version}")
        
        # 3. Check storm.gearbox asset
        print("\n3. Checking storm.gearbox asset:")
        storm_query = select(Asset).where(Asset.asset_name == "storm.gearbox")
        storm_asset = session.exec(storm_query).first()
        if storm_asset:
            print(f"   Found storm.gearbox with asset_id: {storm_asset.asset_id}")
            
            # Check AssetSoftware entries for storm.gearbox
            asset_sw_count = session.exec(
                select(func.count(AssetSoftware.asset_software_id))
                .where(AssetSoftware.asset_id == storm_asset.asset_id)
            ).one()
            print(f"   AssetSoftware entries for storm.gearbox: {asset_sw_count}")
            
            # List AssetSoftware entries
            asset_sw_query = select(AssetSoftware).where(AssetSoftware.asset_id == storm_asset.asset_id)
            asset_sw_items = session.exec(asset_sw_query).all()
            print(f"\n   AssetSoftware details for storm.gearbox:")
            for idx, asw in enumerate(asset_sw_items, 1):
                print(f"   {idx}. AssetSoftware ID: {asw.asset_software_id}, Software Catalog ID: {asw.software_catalog_id}")
        else:
            print("   storm.gearbox asset NOT FOUND!")
        
        # 4. Check InstalledSoftware table
        print("\n4. Checking InstalledSoftware table:")
        installed_count = session.exec(select(func.count(InstalledSoftware.software_id))).one()
        print(f"   Total InstalledSoftware entries: {installed_count}")
        
        if storm_asset:
            storm_installed_count = session.exec(
                select(func.count(InstalledSoftware.software_id))
                .where(InstalledSoftware.asset_id == storm_asset.asset_id)
            ).one()
            print(f"   InstalledSoftware entries for storm.gearbox: {storm_installed_count}")
            
            # List InstalledSoftware entries for storm.gearbox
            installed_query = select(InstalledSoftware).where(
                InstalledSoftware.asset_id == storm_asset.asset_id
            ).limit(10)
            installed_items = session.exec(installed_query).all()
            print(f"\n   First 10 InstalledSoftware entries for storm.gearbox:")
            for idx, inst in enumerate(installed_items, 1):
                print(f"   {idx}. ID: {inst.software_id}, Name: {inst.sw_name}, Version: {inst.sw_version}")
        
        # 5. Test the exact query pattern from configuration_management_state
        print("\n5. Testing query pattern from configuration_management_state:")
        
        # First, let's see what the state might be using
        if storm_asset:
            # Simulate the query that might be in the state
            query = select(SoftwareCatalog).limit(100)  # Check if there's a limit
            results = session.exec(query).all()
            print(f"   Query with limit(100): {len(results)} results")
            
            # Check if there's a join with AssetSoftware
            join_query = (
                select(SoftwareCatalog)
                .join(AssetSoftware, AssetSoftware.software_catalog_id == SoftwareCatalog.software_catalog_id)
                .where(AssetSoftware.asset_id == storm_asset.asset_id)
            )
            join_results = session.exec(join_query).all()
            print(f"   Query with AssetSoftware join for storm.gearbox: {len(join_results)} results")
            
            # Check if there's a join with InstalledSoftware
            installed_join_query = (
                select(SoftwareCatalog)
                .join(InstalledSoftware, InstalledSoftware.software_id == SoftwareCatalog.software_catalog_id)
                .where(InstalledSoftware.asset_id == storm_asset.asset_id)
            )
            installed_join_results = session.exec(installed_join_query).all()
            print(f"   Query with InstalledSoftware join for storm.gearbox: {len(installed_join_results)} results")
        
        # 6. Check for any hardcoded limits or pagination issues
        print("\n6. Checking for pagination/limit issues:")
        print("   Looking for any queries that might return exactly 2 items...")
        
        # Test different limit values
        for limit_val in [1, 2, 5, 10, 20]:
            limited_query = select(SoftwareCatalog).limit(limit_val)
            limited_results = session.exec(limited_query).all()
            print(f"   Limit {limit_val}: {len(limited_results)} results")
            if len(limited_results) == 2:
                print(f"   *** Found exact match with limit={limit_val} ***")

if __name__ == "__main__":
    debug_software_display()