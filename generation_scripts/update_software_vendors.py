#!/usr/bin/env python3
"""Update software vendor information from gearbox_software_data.txt."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from local_llama.models import SoftwareCatalog, SWManufacturer
import re

load_dotenv()

# Map of vendor names from the file to standardized names
VENDOR_MAPPING = {
    "National Instruments": "National Instruments",
    "NI": "National Instruments",  # NI is short for National Instruments
    "Hewlett-Packard": "Hewlett-Packard",
    "Hewlett Packard Development Company L.P.": "Hewlett-Packard",
    "HP": "Hewlett-Packard",
    "Microsoft Corporation": "Microsoft",
    "Microsoft": "Microsoft",
    "Intel Corporation": "Intel",
    "Intel": "Intel",
    "Rockwell Software, Inc.": "Rockwell Software",
    "Rockwell Software": "Rockwell Software",
    "Test Automation Services": "Test Automation Services",
    "Bolt Science": "Bolt Science",
    "Baldor UK Ltd": "Baldor UK Ltd",
    "Acronis": "Acronis",
    "Adobe Systems": "Adobe",
    "Adobe": "Adobe",
    "Advanced Micro Devices": "AMD",
    "AMD": "AMD",
    "ATI Technologies": "ATI Technologies",
    "Belarc": "Belarc",
    "Dell": "Dell",
    "Dell Products": "Dell",
    "DoD PKE Engineering": "DoD PKE Engineering",
    "DoD-PKE": "DoD PKE Engineering",
    "GETS-1000": "Lockheed Martin",
    "Invincea": "Invincea",
    "JKI": "JKI",
    "Leidos": "Leidos",
    "LMSI": "Lockheed Martin",
    "Lockheed Martin": "Lockheed Martin",
    "Macrovision": "Macrovision",
    "McAfee": "McAfee",
    "NVIDIA": "NVIDIA",
    "OPC Foundation": "OPC Foundation",
    "Oracle": "Oracle",
    "Realtek Semiconductor": "Realtek",
    "Spellman": "Spellman",
    "Sun Microsystems": "Sun Microsystems",
    "UltraVNC": "UltraVNC"
}

def parse_gearbox_data():
    """Parse the aggregated_asset_sw.txt file to extract software and vendor info."""
    # Use aggregated_asset_sw.txt which has clearer format
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "local_llama/database/data/aggregated_asset_sw.txt"
    )
    
    software_vendors = {}
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse the format: (Vendor, Software Name, version X.X.X, architecture)
            # Example: (National Instruments, NI LabVIEW, version 7.1, 32-bit)
            if line.startswith('(') and line.endswith(')'):
                # Remove parentheses
                content = line[1:-1]
                
                # Split by comma
                parts = content.split(',')
                
                if len(parts) >= 3:  # Need at least vendor, name, version
                    vendor = parts[0].strip()
                    name = parts[1].strip()
                    
                    # Only process entries with actual vendor names
                    if vendor and vendor not in ["No Company Name", "<no manufacturer>"]:
                        # Map to standardized vendor name
                        standardized_vendor = VENDOR_MAPPING.get(vendor, vendor)
                        software_vendors[name] = standardized_vendor
    
    print(f"Parsed {len(software_vendors)} software entries from file")
    return software_vendors

def update_vendors():
    """Update software vendor information in the database."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    # Parse the gearbox data
    software_vendors = parse_gearbox_data()
    print(f"Found {len(software_vendors)} software entries with vendor information")
    
    with Session(engine) as session:
        # First, ensure all vendors exist in SWManufacturer table
        vendor_ids = {}
        unique_vendors = set(software_vendors.values())
        
        print("\nEnsuring all vendors exist in database:")
        for vendor_name in unique_vendors:
            # Check if vendor exists
            vendor = session.exec(
                select(SWManufacturer).where(SWManufacturer.swmanu_name == vendor_name)
            ).first()
            
            if not vendor:
                # Create new vendor
                vendor = SWManufacturer(swmanu_name=vendor_name)
                session.add(vendor)
                session.commit()
                print(f"  Created vendor: {vendor_name} (ID: {vendor.swmanu_id})")
            else:
                print(f"  Found existing vendor: {vendor_name} (ID: {vendor.swmanu_id})")
            
            vendor_ids[vendor_name] = vendor.swmanu_id
        
        # Now update software entries with vendor IDs
        print("\nUpdating software vendor information:")
        updated_count = 0
        
        for software_name, vendor_name in software_vendors.items():
            # Find the software entry
            software = session.exec(
                select(SoftwareCatalog).where(SoftwareCatalog.sw_name == software_name)
            ).first()
            
            if software:
                if software.sw_vendor is None:
                    # Update with vendor ID
                    software.sw_vendor = vendor_ids[vendor_name]
                    updated_count += 1
                    print(f"  Updated: {software_name} -> {vendor_name}")
                else:
                    print(f"  Skipped: {software_name} (already has vendor)")
            else:
                print(f"  Not found: {software_name}")
        
        session.commit()
        print(f"\nSuccessfully updated {updated_count} software entries with vendor information")
        
        # Verify the update
        print("\nVerifying update:")
        total_with_vendors = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id)).where(
                SoftwareCatalog.sw_vendor.isnot(None)
            )
        ).one()
        
        total_without_vendors = session.exec(
            select(func.count(SoftwareCatalog.software_catalog_id)).where(
                SoftwareCatalog.sw_vendor.is_(None)
            )
        ).one()
        
        print(f"Software with vendors: {total_with_vendors}")
        print(f"Software without vendors: {total_without_vendors}")

if __name__ == "__main__":
    from sqlmodel import func
    update_vendors()