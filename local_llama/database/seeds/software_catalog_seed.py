from sqlmodel import Session, create_engine, select
from local_llama.models.software_catalog import SoftwareCatalog
import os
from dotenv import load_dotenv

load_dotenv()

def seed_software_catalog():
    """Seed the SoftwareCatalog table with common software."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Software catalog data
    # Note: sw_vendor IDs correspond to SWManufacturer seed data
    software_catalog_data = [
        # Operating Systems
        {
            "sw_name": "Microsoft Windows 10 Enterprise",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "OS",
            "sw_type": "Operating System",
            "latest_version": "22H2",
            "sw_architecture_compatibility": "x86_64,x86",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Enterprise edition of Windows 10 operating system"
        },
        {
            "sw_name": "Microsoft Windows 11 Enterprise",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "OS",
            "sw_type": "Operating System",
            "latest_version": "23H2",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Enterprise edition of Windows 11 operating system"
        },
        {
            "sw_name": "Red Hat Enterprise Linux",
            "sw_vendor": 23,  # Red Hat
            "sw_category": "OS",
            "sw_type": "Operating System",
            "latest_version": "9.3",
            "sw_architecture_compatibility": "x86_64,ARM64,PowerPC64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "subscription",
            "description": "Enterprise Linux distribution"
        },
        
        # Security Software
        {
            "sw_name": "McAfee Endpoint Security",
            "sw_vendor": 16,  # McAfee
            "sw_category": "Security",
            "sw_type": "Application",
            "latest_version": "10.7.0",
            "sw_architecture_compatibility": "x86_64,x86",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Enterprise endpoint protection platform"
        },
        {
            "sw_name": "Symantec Endpoint Protection",
            "sw_vendor": 17,  # Symantec
            "sw_category": "Security",
            "sw_type": "Application",
            "latest_version": "14.3",
            "sw_architecture_compatibility": "x86_64,x86",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Enterprise antivirus and security solution"
        },
        
        # Productivity Software
        {
            "sw_name": "Microsoft Office Professional Plus 2021",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "Productivity",
            "sw_type": "Application",
            "latest_version": "2021",
            "sw_architecture_compatibility": "x86_64,x86",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Office productivity suite"
        },
        {
            "sw_name": "Adobe Acrobat Pro DC",
            "sw_vendor": 2,  # Adobe
            "sw_category": "Productivity",
            "sw_type": "Application",
            "latest_version": "2023.008",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "subscription",
            "description": "PDF creation and editing software"
        },
        
        # Development Tools
        {
            "sw_name": "Microsoft Visual Studio Enterprise",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "Development",
            "sw_type": "Application",
            "latest_version": "2022",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": False,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-seat",
            "description": "Integrated development environment"
        },
        {
            "sw_name": "Python",
            "sw_vendor": 40,  # Python Software Foundation
            "sw_category": "Development",
            "sw_type": "Runtime",
            "latest_version": "3.11.7",
            "sw_architecture_compatibility": "x86_64,x86,ARM64,ARM",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "open-source",
            "description": "Python programming language runtime"
        },
        
        # Database Software
        {
            "sw_name": "Microsoft SQL Server Enterprise",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "Database",
            "sw_type": "Application",
            "latest_version": "2022",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-core",
            "description": "Enterprise database management system"
        },
        {
            "sw_name": "PostgreSQL",
            "sw_vendor": 39,  # PostgreSQL Global Development Group
            "sw_category": "Database",
            "sw_type": "Application",
            "latest_version": "16.1",
            "sw_architecture_compatibility": "x86_64,x86,ARM64,ARM",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "open-source",
            "description": "Open source relational database"
        },
        
        # Utility Software
        {
            "sw_name": "7-Zip",
            "sw_vendor": 49,  # Igor Pavlov
            "sw_category": "Utility",
            "sw_type": "Application",
            "latest_version": "23.01",
            "sw_architecture_compatibility": "x86_64,x86,ARM64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "open-source",
            "description": "File compression utility"
        },
        {
            "sw_name": "PuTTY",
            "sw_vendor": 50,  # Simon Tatham
            "sw_category": "Utility",
            "sw_type": "Application",
            "latest_version": "0.79",
            "sw_architecture_compatibility": "x86_64,x86",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "open-source",
            "description": "SSH and telnet client"
        },
        
        # Drivers
        {
            "sw_name": "NVIDIA Graphics Driver",
            "sw_vendor": 48,  # NVIDIA
            "sw_category": "Driver",
            "sw_type": "Driver",
            "latest_version": "546.33",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": False,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "proprietary",
            "description": "Graphics card driver for NVIDIA GPUs"
        },
        
        # Firmware
        {
            "sw_name": "Dell BIOS Update",
            "sw_vendor": 13,  # Dell
            "sw_category": "Firmware",
            "sw_type": "Firmware",
            "latest_version": "2.19.0",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": False,
            "license_model": "proprietary",
            "description": "System BIOS firmware update"
        },
        
        # Virtualization
        {
            "sw_name": "VMware vSphere ESXi",
            "sw_vendor": 6,  # VMware
            "sw_category": "Virtualization",
            "sw_type": "Application",
            "latest_version": "8.0 U2",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-socket",
            "description": "Enterprise virtualization platform"
        },
        {
            "sw_name": "Microsoft Hyper-V Server",
            "sw_vendor": 1,  # Microsoft
            "sw_category": "Virtualization",
            "sw_type": "Application",
            "latest_version": "2022",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": True,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-core",
            "description": "Microsoft virtualization platform"
        },
        
        # Monitoring
        {
            "sw_name": "SolarWinds Network Performance Monitor",
            "sw_vendor": 31,  # SolarWinds
            "sw_category": "Monitoring",
            "sw_type": "Application",
            "latest_version": "2024.1",
            "sw_architecture_compatibility": "x86_64",
            "dod_compliant": False,
            "is_approved": True,
            "is_licensed": True,
            "license_model": "per-element",
            "description": "Network monitoring and management"
        },
    ]
    
    with Session(engine) as session:
        # Check if software already exists to avoid duplicates
        existing_software = session.exec(select(SoftwareCatalog)).all()
        existing_names = {sw.sw_name for sw in existing_software}
        
        software_to_add = []
        skipped_software = []
        
        for software_data in software_catalog_data:
            if software_data["sw_name"] not in existing_names:
                try:
                    software_to_add.append(SoftwareCatalog(**software_data))
                except Exception as e:
                    skipped_software.append((software_data["sw_name"], str(e)))
            else:
                skipped_software.append((software_data["sw_name"], "Already exists"))
        
        if software_to_add:
            session.add_all(software_to_add)
            session.commit()
            print(f"Added {len(software_to_add)} software entries to the catalog.")
        else:
            print("No new software to add.")
        
        if skipped_software:
            print(f"\nSkipped {len(skipped_software)} software entries:")
            for name, reason in skipped_software:
                print(f"  - {name}: {reason}")

if __name__ == "__main__":
    seed_software_catalog()