#!/usr/bin/env python3
"""Update vendor information for storm.gearbox software based on known mappings."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select, func
from local_llama.models import SoftwareCatalog, SWManufacturer

load_dotenv()

# Direct mapping of software names to vendor names based on the data
SOFTWARE_TO_VENDOR = {
    # HP/Hewlett-Packard software
    "HPSSupply": "Hewlett-Packard",
    
    # Intel software
    "Intel Audio Studio": "Intel",
    "Intel Driver": "Intel",
    
    # Microsoft software
    "Microsoft .NET Framework": "Microsoft",
    "MSXML 4.0 SP2 Parser and SDK": "Microsoft",
    
    # National Instruments software (the majority)
    "NI Assistant Framework": "National Instruments",
    "NI Assistant Framework LabVIEW Code Generator": "National Instruments",
    "NI Assistant Framework LabVIEW Code Generator 6.1": "National Instruments",
    "NI Assistant Framework LabVIEW Code Generator 7.0": "National Instruments",
    "NI Assistant Framework LabVIEW Code Generator 7.1": "National Instruments",
    "NI Calibration Provider for MAX": "National Instruments",
    "NI Common Digital": "National Instruments",
    "NI DAQ Assistant": "National Instruments",
    "NI DDSP": "National Instruments",
    "NI Distribution Information - PDS English": "National Instruments",
    "NI DPPH": "National Instruments",
    "NI Example Finder": "National Instruments",
    "NI Fusion Standard Library": "National Instruments",
    "NI Instrument IO Assistant": "National Instruments",
    "NI Instrument IO Assistant for LabVIEW": "National Instruments",
    "NI LabVIEW": "National Instruments",
    "NI LabVIEW Advanced Analysis": "National Instruments",
    "NI LabVIEW Core Essentials": "National Instruments",
    "NI LabVIEW Full": "National Instruments",
    "NI LabVIEW Picture Control and CIN Tools": "National Instruments",
    "NI LabVIEW Professional Tools": "National Instruments",
    "NI LabVIEW Run-Time Engine 7.0": "National Instruments",
    "NI LabVIEW Run-Time Engine 7.1": "National Instruments",
    "NI LabVIEW Service Locator": "National Instruments",
    "NI Legacy DAQmxRF": "National Instruments",
    "NI License Manager": "National Instruments",
    "NI LVBrokerAux1071": "National Instruments",
    "NI LVBrokerAux70": "National Instruments",
    "NI LVBrokerAux71": "National Instruments",
    "NI Measurement & Automation Explorer": "National Instruments",
    "NI Measurement Studio Recipe Processor": "National Instruments",
    "NI Measurements eXtensions for PAL": "National Instruments",
    "NI PXI Platform Services for Windows": "National Instruments",
    "NI PXI Platform Services Provider for MAX": "National Instruments",
    "NI Registration Wizard": "National Instruments",
    "NI Remote Provider for MAX": "National Instruments",
    "NI Remote PXI Provider for MAX": "National Instruments",
    "NI SCXI": "National Instruments",
    "NI Software Provider for MAX": "National Instruments",
    "NI STC": "National Instruments",
    "NI Timing": "National Instruments",
    "NI Uninstaller": "National Instruments",
    "NI-488.2": "National Instruments",
    "NI-488.2 Provider for MAX": "National Instruments",
    "NI-653x Support": "National Instruments",
    "NI-DAQ INF Files": "National Instruments",
    "NI-DAQ Provider for MAX": "National Instruments",
    "NI-DAQmx": "National Instruments",
    "NI-DAQmx Documentation": "National Instruments",
    "NI-DAQmx MAX Support": "National Instruments",
    "NI-DAQmx support for LabVIEW": "National Instruments",
    "NI-MDBG": "National Instruments",
    "NI-MRU": "National Instruments",
    "NI-MXDF": "National Instruments",
    "NI-PAL": "National Instruments",
    "NI-RPC": "National Instruments",
    "NI-RPC for Phar Lap ETS": "National Instruments",
    "NI-RPC for PharLap": "National Instruments",
    "NI-VISA": "National Instruments",
    "NI-VISA MAX Provider": "National Instruments",
    "NI-VISA Runtime": "National Instruments",
    "NI-VISA Server": "National Instruments",
    "NI-VXI Support for LabVIEW": "National Instruments",
    
    # Other vendors
    "R1178-1": "Test Automation Services",
    "TorqueConverter": "Bolt Science",
    "Traditional NI-DAQ": "National Instruments",
    "Traditional NI-DAQ Documentation": "National Instruments",
    "WorkBench": "Baldor UK Ltd"
}

# Vendor website mappings
VENDOR_WEBSITES = {
    "National Instruments": "https://www.ni.com",
    "Hewlett-Packard": "https://www.hp.com",
    "Intel": "https://www.intel.com",
    "Microsoft": "https://www.microsoft.com",
    "Test Automation Services": "https://www.testautomation.com",
    "Bolt Science": "https://www.boltscience.com",
    "Baldor UK Ltd": "https://www.baldor.com"
}

def update_vendors():
    """Update software vendor information in the database."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # First, ensure all vendors exist in SWManufacturer table
        vendor_ids = {}
        unique_vendors = set(SOFTWARE_TO_VENDOR.values())
        
        print("Ensuring all vendors exist in database:")
        for vendor_name in unique_vendors:
            # Check if vendor exists
            vendor = session.exec(
                select(SWManufacturer).where(SWManufacturer.swmanu_name == vendor_name)
            ).first()
            
            if not vendor:
                # Create new vendor with weblink
                weblink = VENDOR_WEBSITES.get(vendor_name, f"https://www.google.com/search?q={vendor_name.replace(' ', '+')}")
                vendor = SWManufacturer(
                    swmanu_name=vendor_name,
                    weblink=weblink
                )
                session.add(vendor)
                session.commit()
                print(f"  Created vendor: {vendor_name} (ID: {vendor.swmanu_id})")
            else:
                print(f"  Found existing vendor: {vendor_name} (ID: {vendor.swmanu_id})")
            
            vendor_ids[vendor_name] = vendor.swmanu_id
        
        # Now update software entries with vendor IDs
        print("\nUpdating software vendor information:")
        updated_count = 0
        not_found_count = 0
        
        for software_name, vendor_name in SOFTWARE_TO_VENDOR.items():
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
                not_found_count += 1
                print(f"  Not found in database: {software_name}")
        
        session.commit()
        
        print(f"\nSummary:")
        print(f"  Successfully updated: {updated_count} software entries")
        print(f"  Software not found: {not_found_count} entries")
        
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
        
        print(f"  Software with vendors: {total_with_vendors}")
        print(f"  Software without vendors: {total_without_vendors}")
        print(f"  Total software: {total_with_vendors + total_without_vendors}")

if __name__ == "__main__":
    update_vendors()