"""
Master seed file that combines all individual seed data files into a singular script.
This file must be updated after each seed data file addition to ensure all seed data 
can be executed in one script without errors.
"""

from sqlmodel import Session, create_engine, select
from local_llama.models.building import Building
from local_llama.models.floor import Floor
from local_llama.models.sys_type import SysType
from local_llama.models.hardware_manufacturer import HardwareManufacturer
from local_llama.models.sw_manufacturer import SWManufacturer
from local_llama.models.project import Project
from local_llama.models.operating_system import OperatingSystem
from local_llama.models.os_edition import OSEdition
from local_llama.models.os_version import OSVersion
from local_llama.models.log_type import LogType
from local_llama.models.imaging_method import ImagingMethod
from local_llama.models.sys_architecture import SysArchitecture
from local_llama.models.cpu_type import CPUType
from local_llama.models.gpu_type import GPUType
from local_llama.models.privilege_level import PrivilegeLevel
from local_llama.models.department import Department
from local_llama.models.av_version import AVVersion
from local_llama.models.dat_version import DatVersion
from local_llama.models.employee import Employee
from local_llama.models.app_user import AppUser
from local_llama.models.room import Room
from local_llama.models.vm_type import VMType
from local_llama.models.virt_source import VirtualizationSource
from local_llama.models.vm_status import VMStatus
from local_llama.models.asset import Asset
from local_llama.models.software_catalog import SoftwareCatalog
import os
from dotenv import load_dotenv

load_dotenv()

def seed_buildings():
    """Seed the Building table with predefined building data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Building data to insert
    buildings_data = [
        {"building_name": "Building 370"},
        {"building_name": "Building 377"},
        {"building_name": "Building 403"},
        {"building_name": "Building 350"},
        {"building_name": "Building 012"},
        {"building_name": "Building 014"},
        {"building_name": "Building 001"},
        {"building_name": "Building 010"},
    ]
    
    with Session(engine) as session:
        # Check if buildings already exist to avoid duplicates
        existing_buildings = session.exec(select(Building)).all()
        existing_names = {building.building_name for building in existing_buildings}
        
        buildings_to_add = []
        for building_data in buildings_data:
            if building_data["building_name"] not in existing_names:
                buildings_to_add.append(Building(**building_data))
        
        if buildings_to_add:
            session.add_all(buildings_to_add)
            session.commit()
            print(f"Added {len(buildings_to_add)} buildings to the database.")
        else:
            print("All buildings already exist in the database.")

def seed_floors():
    """Seed the Floor table with predefined floor data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Floor data to insert
    floors_data = [
        {"floor_name": "Floor 001"},
        {"floor_name": "Floor_002"},
        {"floor_name": "Floor Ground"},
    ]
    
    with Session(engine) as session:
        # Check if floors already exist to avoid duplicates
        existing_floors = session.exec(select(Floor)).all()
        existing_names = {floor.floor_name for floor in existing_floors}
        
        floors_to_add = []
        for floor_data in floors_data:
            if floor_data["floor_name"] not in existing_names:
                floors_to_add.append(Floor(**floor_data))
        
        if floors_to_add:
            session.add_all(floors_to_add)
            session.commit()
            print(f"Added {len(floors_to_add)} floors to the database.")
        else:
            print("All floors already exist in the database.")

def seed_systypes():
    """Seed the SysType table with predefined system type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # SysType data to insert
    systypes_data = [
        {"systype_name": "Desktop Workstation"},
        {"systype_name": "Laptop Workstation"},
        {"systype_name": "Server"},
        {"systype_name": "Digital Oscilloscope"},
        {"systype_name": "Signal Analyzer"},
        {"systype_name": "Network Analyzer"},
        {"systype_name": "Network Appliance"},
        {"systype_name": "Network Firewall"},
        {"systype_name": "Network Gateway"},
        {"systype_name": "Program Logic Controller"},
        {"systype_name": "Single Board Computer"},
    ]
    
    with Session(engine) as session:
        # Check if systypes already exist to avoid duplicates
        existing_systypes = session.exec(select(SysType)).all()
        existing_names = {systype.systype_name for systype in existing_systypes}
        
        systypes_to_add = []
        for systype_data in systypes_data:
            if systype_data["systype_name"] not in existing_names:
                systypes_to_add.append(SysType(**systype_data))
        
        if systypes_to_add:
            session.add_all(systypes_to_add)
            session.commit()
            print(f"Added {len(systypes_to_add)} system types to the database.")
        else:
            print("All system types already exist in the database.")

def seed_hardware_manufacturers():
    """Seed the HardwareManufacturer table with predefined hardware manufacturer data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Hardware manufacturer data to insert (name, weblink)
    hardware_manufacturers_data = [
        {"hwmanu_name": "Apple", "weblink": "https://www.apple.com"},
        {"hwmanu_name": "Asus", "weblink": "https://www.asus.com"},
        {"hwmanu_name": "Dell", "weblink": "https://www.dell.com"},
        {"hwmanu_name": "HP", "weblink": "https://www.hp.com"},
        {"hwmanu_name": "HTC", "weblink": "https://www.htc.com"},
        {"hwmanu_name": "Lenovo", "weblink": "https://www.lenovo.com"},
        {"hwmanu_name": "Nintendo", "weblink": "https://www.nintendo.com"},
        {"hwmanu_name": "Sony", "weblink": "https://www.sony.com"},
        {"hwmanu_name": "Acer", "weblink": "https://www.acer.com"},
        {"hwmanu_name": "Microsoft", "weblink": "https://www.microsoft.com"},
        {"hwmanu_name": "Samsung", "weblink": "https://www.samsung.com"},
        {"hwmanu_name": "Toshiba", "weblink": "https://www.toshiba.com"},
        {"hwmanu_name": "MSI", "weblink": "https://www.msi.com"},
        {"hwmanu_name": "IBM", "weblink": "https://www.ibm.com"},
        {"hwmanu_name": "NEC", "weblink": "https://www.nec.com"},
        {"hwmanu_name": "Fujitsu", "weblink": "https://www.fujitsu.com"},
        {"hwmanu_name": "Intel", "weblink": "https://www.intel.com"},
        {"hwmanu_name": "AMD", "weblink": "https://www.amd.com"},
        {"hwmanu_name": "NVIDIA", "weblink": "https://www.nvidia.com"},
        {"hwmanu_name": "Qualcomm", "weblink": "https://www.qualcomm.com"},
        {"hwmanu_name": "Broadcom", "weblink": "https://www.broadcom.com"},
        {"hwmanu_name": "Texas Instruments", "weblink": "https://www.ti.com"},
        {"hwmanu_name": "Cisco", "weblink": "https://www.cisco.com"},
        {"hwmanu_name": "Juniper Networks", "weblink": "https://www.juniper.net"},
        {"hwmanu_name": "Arista Networks", "weblink": "https://www.arista.com"},
        {"hwmanu_name": "Extreme Networks", "weblink": "https://www.extremenetworks.com"},
        {"hwmanu_name": "Ruckus Networks", "weblink": "https://www.ruckusnetworks.com"},
        {"hwmanu_name": "CommScope", "weblink": "https://www.commscope.com"},
        {"hwmanu_name": "Foxconn", "weblink": "https://www.foxconn.com"},
        {"hwmanu_name": "LG", "weblink": "https://www.lg.com"},
        {"hwmanu_name": "Seagate", "weblink": "https://www.seagate.com"},
        {"hwmanu_name": "Western Digital", "weblink": "https://www.westerndigital.com"},
        {"hwmanu_name": "Kingston", "weblink": "https://www.kingston.com"},
        {"hwmanu_name": "Corsair", "weblink": "https://www.corsair.com"},
        {"hwmanu_name": "Logitech", "weblink": "https://www.logitech.com"},
        {"hwmanu_name": "Razer", "weblink": "https://www.razer.com"},
        {"hwmanu_name": "SteelSeries", "weblink": "https://steelseries.com"},
        {"hwmanu_name": "Belkin", "weblink": "https://www.belkin.com"},
        {"hwmanu_name": "Netgear", "weblink": "https://www.netgear.com"},
        {"hwmanu_name": "TP-Link", "weblink": "https://www.tp-link.com"},
        {"hwmanu_name": "D-Link", "weblink": "https://www.dlink.com"},
        {"hwmanu_name": "Linksys", "weblink": "https://www.linksys.com"},
        {"hwmanu_name": "Super Micro Computer", "weblink": "https://www.supermicro.com"},
        {"hwmanu_name": "ASML", "weblink": "https://www.asml.com"},
        {"hwmanu_name": "Applied Materials", "weblink": "https://www.appliedmaterials.com"},
        {"hwmanu_name": "Arm", "weblink": "https://www.arm.com"},
        {"hwmanu_name": "SiFive", "weblink": "https://www.sifive.com"},
        {"hwmanu_name": "TSMC", "weblink": "https://www.tsmc.com"},
        {"hwmanu_name": "Hon Hai Precision", "weblink": "https://www.honhai.com"},
        {"hwmanu_name": "RTX", "weblink": "https://www.rtx.com"},
        {"hwmanu_name": "Boeing", "weblink": "https://www.boeing.com"},
        {"hwmanu_name": "Lockheed Martin", "weblink": "https://www.lockheedmartin.com"},
        {"hwmanu_name": "Northrop Grumman", "weblink": "https://www.northropgrumman.com"},
        {"hwmanu_name": "General Dynamics", "weblink": "https://www.gd.com"},
        {"hwmanu_name": "BAE Systems", "weblink": "https://www.baesystems.com"},
        {"hwmanu_name": "L3Harris Technologies", "weblink": "https://www.l3harris.com"},
        {"hwmanu_name": "Huntington Ingalls Industries", "weblink": "https://www.hii.com"},
        {"hwmanu_name": "Leidos", "weblink": "https://www.leidos.com"},
        {"hwmanu_name": "Airbus", "weblink": "https://www.airbus.com"},
        {"hwmanu_name": "Thales", "weblink": "https://www.thalesgroup.com"},
        {"hwmanu_name": "Leonardo", "weblink": "https://www.leonardo.com"},
        {"hwmanu_name": "Saab", "weblink": "https://www.saab.com"},
        {"hwmanu_name": "Rheinmetall", "weblink": "https://www.rheinmetall.com"},
        {"hwmanu_name": "Elbit Systems", "weblink": "https://elbitsystems.com"},
        {"hwmanu_name": "Canon", "weblink": "https://www.canon.com"},
        {"hwmanu_name": "Xiaomi", "weblink": "https://www.xiaomi.com"},
        {"hwmanu_name": "Huawei", "weblink": "https://www.huawei.com"},
        {"hwmanu_name": "Panasonic", "weblink": "https://www.panasonic.com"},
        {"hwmanu_name": "Sharp", "weblink": "https://global.sharp"},
        {"hwmanu_name": "Hitachi", "weblink": "https://www.hitachi.com"},
        {"hwmanu_name": "Oracle", "weblink": "https://www.oracle.com"},
        {"hwmanu_name": "HPE", "weblink": "https://www.hpe.com"},
        {"hwmanu_name": "Micron", "weblink": "https://www.micron.com"},
        {"hwmanu_name": "SK Hynix", "weblink": "https://www.skhynix.com"},
        {"hwmanu_name": "Epson", "weblink": "https://www.epson.com"},
        {"hwmanu_name": "Brother Industries", "weblink": "https://www.brother.com"},
        {"hwmanu_name": "GlobalFoundries", "weblink": "https://www.gf.com"},
        {"hwmanu_name": "Ericsson", "weblink": "https://www.ericsson.com"},
        {"hwmanu_name": "Nokia", "weblink": "https://www.nokia.com"},
        {"hwmanu_name": "Gigabyte Technology", "weblink": "https://www.gigabyte.com"},
        {"hwmanu_name": "ASRock", "weblink": "https://www.asrock.com"},
        {"hwmanu_name": "Biostar", "weblink": "https://www.biostar.com.tw"},
        {"hwmanu_name": "EVGA", "weblink": "https://www.evga.com"},
        {"hwmanu_name": "Antec", "weblink": "https://www.antec.com"},
        {"hwmanu_name": "Cooler Master", "weblink": "https://www.coolermaster.com"},
        {"hwmanu_name": "Lian Li", "weblink": "https://www.lian-li.com"},
        {"hwmanu_name": "Thermaltake", "weblink": "https://www.thermaltake.com"},
        {"hwmanu_name": "Sapphire Technology", "weblink": "https://www.sapphiretech.com"},
        {"hwmanu_name": "Zotac", "weblink": "https://www.zotac.com"},
    ]
    
    with Session(engine) as session:
        # Check if hardware manufacturers already exist to avoid duplicates
        existing_manufacturers = session.exec(select(HardwareManufacturer)).all()
        existing_names = {manufacturer.hwmanu_name for manufacturer in existing_manufacturers}
        
        manufacturers_to_add = []
        for manufacturer_data in hardware_manufacturers_data:
            if manufacturer_data["hwmanu_name"] not in existing_names:
                manufacturers_to_add.append(HardwareManufacturer(**manufacturer_data))
        
        if manufacturers_to_add:
            session.add_all(manufacturers_to_add)
            session.commit()
            print(f"Added {len(manufacturers_to_add)} hardware manufacturers to the database.")
        else:
            print("All hardware manufacturers already exist in the database.")

def seed_sw_manufacturers():
    """Seed the SWManufacturer table with predefined software manufacturer data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Software manufacturer data to insert (name, weblink, contact)
    sw_manufacturers_data = [
        {"swmanu_name": "Adobe", "weblink": "https://www.adobe.com", "swmanu_contact": "1-800-833-6687"},
        {"swmanu_name": "Microsoft", "weblink": "https://www.microsoft.com", "swmanu_contact": "1-800-426-9400"},
        {"swmanu_name": "Oracle", "weblink": "https://www.oracle.com", "swmanu_contact": "1-800-392-2999"},
        {"swmanu_name": "SAP", "weblink": "https://www.sap.com", "swmanu_contact": "1-800-872-1727"},
        {"swmanu_name": "Salesforce", "weblink": "https://www.salesforce.com", "swmanu_contact": "1-800-667-6389"},
        {"swmanu_name": "IBM", "weblink": "https://www.ibm.com", "swmanu_contact": "1-800-426-4968"},
        {"swmanu_name": "Intuit", "weblink": "https://www.intuit.com", "swmanu_contact": "1-800-446-8848"},
        {"swmanu_name": "ServiceNow", "weblink": "https://www.servicenow.com", "swmanu_contact": "1-888-914-9661"},
        {"swmanu_name": "Workday", "weblink": "https://www.workday.com", "swmanu_contact": "1-877-967-5329"},
        {"swmanu_name": "Autodesk", "weblink": "https://www.autodesk.com", "swmanu_contact": "1-855-301-1941"},
        {"swmanu_name": "VMware", "weblink": "https://www.vmware.com", "swmanu_contact": "1-877-486-9273"},
        {"swmanu_name": "Red Hat", "weblink": "https://www.redhat.com", "swmanu_contact": "1-888-733-4281"},
        {"swmanu_name": "Atlassian", "weblink": "https://www.atlassian.com", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "Epicor Software Corporation", "weblink": "https://www.epicor.com", "swmanu_contact": "1-800-999-6995"},
        {"swmanu_name": "Infor", "weblink": "https://www.infor.com", "swmanu_contact": "1-800-260-2640"},
        {"swmanu_name": "Sage", "weblink": "https://www.sage.com", "swmanu_contact": "1-866-996-7243"},
        {"swmanu_name": "NetSuite", "weblink": "https://www.netsuite.com", "swmanu_contact": "1-877-638-7848"},
        {"swmanu_name": "Zoho Corporation", "weblink": "https://www.zoho.com", "swmanu_contact": "1-888-900-9646"},
        {"swmanu_name": "Splunk", "weblink": "https://www.splunk.com", "swmanu_contact": "1-888-773-5865"},
        {"swmanu_name": "Palo Alto Networks", "weblink": "https://www.paloaltonetworks.com", "swmanu_contact": "1-866-320-4788"},
        {"swmanu_name": "Cisco", "weblink": "https://www.cisco.com", "swmanu_contact": "1-800-553-2447"},
        {"swmanu_name": "Symantec", "weblink": "https://www.broadcom.com", "swmanu_contact": "1-800-441-7234"},
        {"swmanu_name": "McAfee", "weblink": "https://www.mcafee.com", "swmanu_contact": "1-888-847-8766"},
        {"swmanu_name": "Fortinet", "weblink": "https://www.fortinet.com", "swmanu_contact": "1-866-868-3678"},
        {"swmanu_name": "Crowdstrike", "weblink": "https://www.crowdstrike.com", "swmanu_contact": "1-888-510-3623"},
        {"swmanu_name": "Okta", "weblink": "https://www.okta.com", "swmanu_contact": "1-888-722-7871"},
        {"swmanu_name": "Zendesk", "weblink": "https://www.zendesk.com", "swmanu_contact": "1-888-670-4887"},
        {"swmanu_name": "HubSpot", "weblink": "https://www.hubspot.com", "swmanu_contact": "1-888-482-7768"},
        {"swmanu_name": "Slack", "weblink": "https://slack.com", "swmanu_contact": "1-855-980-5920"},
        {"swmanu_name": "Tableau", "weblink": "https://www.tableau.com", "swmanu_contact": "1-833-559-0075"},
        {"swmanu_name": "Snowflake", "weblink": "https://www.snowflake.com", "swmanu_contact": "1-844-766-9355"},
        {"swmanu_name": "Databricks", "weblink": "https://www.databricks.com", "swmanu_contact": "1-866-330-0121"},
        {"swmanu_name": "MongoDB", "weblink": "https://www.mongodb.com", "swmanu_contact": "1-844-666-4632"},
        {"swmanu_name": "Cloudera", "weblink": "https://www.cloudera.com", "swmanu_contact": "1-888-789-1488"},
        {"swmanu_name": "Teradata", "weblink": "https://www.teradata.com", "swmanu_contact": "1-866-548-8348"},
        {"swmanu_name": "SAS", "weblink": "https://www.sas.com", "swmanu_contact": "1-800-727-0025"},
        {"swmanu_name": "Informatica", "weblink": "https://www.informatica.com", "swmanu_contact": "1-650-385-5000"},
        {"swmanu_name": "Talend", "weblink": "https://www.talend.com", "swmanu_contact": "1-650-485-2730"},
        {"swmanu_name": "Google Cloud", "weblink": "https://cloud.google.com", "swmanu_contact": "1-844-613-7589"},
        {"swmanu_name": "Amazon Web Services", "weblink": "https://aws.amazon.com", "swmanu_contact": "1-800-257-1778"},
        {"swmanu_name": "Azure", "weblink": "https://azure.microsoft.com", "swmanu_contact": "1-800-867-1389"},
        {"swmanu_name": "GitLab", "weblink": "https://about.gitlab.com", "swmanu_contact": "1-415-689-8249"},
        {"swmanu_name": "GitHub", "weblink": "https://github.com", "swmanu_contact": "1-877-448-4820"},
        {"swmanu_name": "Bitbucket", "weblink": "https://bitbucket.org", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "Freshworks", "weblink": "https://www.freshworks.com", "swmanu_contact": "1-855-818-1151"},
        {"swmanu_name": "Monday.com", "weblink": "https://monday.com", "swmanu_contact": "1-201-778-4567"},
        {"swmanu_name": "Asana", "weblink": "https://asana.com", "swmanu_contact": "1-415-525-8474"},
        {"swmanu_name": "Trello", "weblink": "https://trello.com", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "QuickBooks", "weblink": "https://quickbooks.intuit.com", "swmanu_contact": "1-800-446-8848"},
        {"swmanu_name": "Xero", "weblink": "https://www.xero.com", "swmanu_contact": "1-844-829-3726"},
        {"swmanu_name": "Wave", "weblink": "https://www.waveapps.com", "swmanu_contact": "1-833-928-3424"},
    ]
    
    with Session(engine) as session:
        # Check if software manufacturers already exist to avoid duplicates
        existing_manufacturers = session.exec(select(SWManufacturer)).all()
        existing_names = {manufacturer.swmanu_name for manufacturer in existing_manufacturers}
        
        manufacturers_to_add = []
        for manufacturer_data in sw_manufacturers_data:
            if manufacturer_data["swmanu_name"] not in existing_names:
                manufacturers_to_add.append(SWManufacturer(**manufacturer_data))
        
        if manufacturers_to_add:
            session.add_all(manufacturers_to_add)
            session.commit()
            print(f"Added {len(manufacturers_to_add)} software manufacturers to the database.")
        else:
            print("All software manufacturers already exist in the database.")

def seed_projects():
    """Seed the Project table with predefined project data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Project data to insert
    projects_data = [
        {"project_name": "IFMC"},
        {"project_name": "SHIELD"},
        {"project_name": "STARE"},
        {"project_name": "STORM"},
        {"project_name": "MULTI"},
        {"project_name": "TAGM"},
    ]
    
    with Session(engine) as session:
        # Check if projects already exist to avoid duplicates
        existing_projects = session.exec(select(Project)).all()
        existing_names = {project.project_name for project in existing_projects}
        
        projects_to_add = []
        for project_data in projects_data:
            if project_data["project_name"] not in existing_names:
                projects_to_add.append(Project(**project_data))
        
        if projects_to_add:
            session.add_all(projects_to_add)
            session.commit()
            print(f"Added {len(projects_to_add)} projects to the database.")
        else:
            print("All projects already exist in the database.")

def seed_operating_systems():
    """Seed the OperatingSystem table with predefined operating system data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Operating system data to insert
    operating_systems_data = [
        {"os_name": "Microsoft Windows 1.0"},
        {"os_name": "Microsoft Windows 2.0"},
        {"os_name": "Microsoft Windows 2.1"},
        {"os_name": "Microsoft Windows 3.0"},
        {"os_name": "Microsoft Windows 3.1"},
        {"os_name": "Microsoft Windows for Workgroups 3.11"},
        {"os_name": "Microsoft Windows 95"},
        {"os_name": "Microsoft Windows 98"},
        {"os_name": "Microsoft Windows ME"},
        {"os_name": "Microsoft Windows NT 3.1"},
        {"os_name": "Microsoft Windows NT 3.5"},
        {"os_name": "Microsoft Windows NT 3.51"},
        {"os_name": "Microsoft Windows NT 4.0"},
        {"os_name": "Microsoft Windows 2000"},
        {"os_name": "Microsoft Windows XP"},
        {"os_name": "Microsoft Windows Vista"},
        {"os_name": "Microsoft Windows 7"},
        {"os_name": "Microsoft Windows 8"},
        {"os_name": "Microsoft Windows 8.1"},
        {"os_name": "Microsoft Windows 10"},
        {"os_name": "Microsoft Windows 11"},
        {"os_name": "Microsoft Windows CE"},
        {"os_name": "Microsoft Windows Mobile"},
        {"os_name": "Microsoft Windows Phone"},
        {"os_name": "Microsoft Windows RT"},
        {"os_name": "Microsoft Windows Embedded Compact"},
        {"os_name": "Microsoft Windows IoT"},
        {"os_name": "macOS"},
        {"os_name": "iOS"},
        {"os_name": "iPadOS"},
        {"os_name": "watchOS"},
        {"os_name": "tvOS"},
        {"os_name": "visionOS"},
        {"os_name": "Ubuntu"},
        {"os_name": "Debian"},
        {"os_name": "Fedora"},
        {"os_name": "CentOS"},
        {"os_name": "Red Hat Enterprise Linux"},
        {"os_name": "openSUSE"},
        {"os_name": "Arch Linux"},
        {"os_name": "Kali Linux"},
        {"os_name": "Linux Mint"},
        {"os_name": "Manjaro"},
        {"os_name": "Zorin OS"},
        {"os_name": "Pop!_OS"},
        {"os_name": "elementary OS"},
        {"os_name": "SUSE Linux Enterprise"},
        {"os_name": "Gentoo"},
        {"os_name": "Slackware"},
        {"os_name": "Alpine Linux"},
        {"os_name": "Rocky Linux"},
        {"os_name": "Oracle Linux"},
        {"os_name": "Clear Linux"},
        {"os_name": "Android"},
        {"os_name": "Chrome OS"},
        {"os_name": "FreeBSD"},
        {"os_name": "OpenBSD"},
        {"os_name": "NetBSD"},
        {"os_name": "DragonFly BSD"},
        {"os_name": "Solaris"},
        {"os_name": "AIX"},
        {"os_name": "HP-UX"},
        {"os_name": "HarmonyOS"},
        {"os_name": "Tizen"},
        {"os_name": "BlackBerry OS"},
        {"os_name": "Sailfish OS"},
        {"os_name": "KaiOS"},
        {"os_name": "Fuchsia"},
        {"os_name": "Yocto Project"},
        {"os_name": "Buildroot"},
        {"os_name": "VxWorks"},
        {"os_name": "QNX"},
        {"os_name": "FreeRTOS"},
        {"os_name": "Zephyr"},
        {"os_name": "RTEMS"},
        {"os_name": "ThreadX"},
        {"os_name": "OpenWrt"},
        {"os_name": "Ubuntu Core"},
        {"os_name": "Raspbian"},
        {"os_name": "Parrot OS"},
        {"os_name": "PureOS"},
        {"os_name": "Linux Lite"},
        {"os_name": "Deepin"},
        {"os_name": "Linux From Scratch"},
        {"os_name": "EMBEDDED Linux"},
        {"os_name": "OS/2"},
        {"os_name": "BeOS"},
        {"os_name": "ReactOS"},
        {"os_name": "Haiku"},
        {"os_name": "Plan 9"},
        {"os_name": "Inferno"},
        {"os_name": "Syllable"},
        {"os_name": "ArcaOS"},
        {"os_name": "Xen"},
        {"os_name": "uC/OS-II"},
        {"os_name": "uC/OS-III"},
    ]
    
    with Session(engine) as session:
        # Check if operating systems already exist to avoid duplicates
        existing_operating_systems = session.exec(select(OperatingSystem)).all()
        existing_names = {os.os_name for os in existing_operating_systems}
        
        operating_systems_to_add = []
        for os_data in operating_systems_data:
            if os_data["os_name"] not in existing_names:
                operating_systems_to_add.append(OperatingSystem(**os_data))
        
        if operating_systems_to_add:
            session.add_all(operating_systems_to_add)
            session.commit()
            print(f"Added {len(operating_systems_to_add)} operating systems to the database.")
        else:
            print("All operating systems already exist in the database.")

def seed_oseditions():
    """Seed the OSEdition table with predefined OS edition data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # OS Edition data to insert (edition_name)
    oseditions_data = [
        {"osedition_name": "Standard"},
        {"osedition_name": "OEM"},
        {"osedition_name": "OSR2"},
        {"osedition_name": "First Edition"},
        {"osedition_name": "Second Edition"},
        {"osedition_name": "Workstation"},
        {"osedition_name": "Server"},
        {"osedition_name": "Server Enterprise"},
        {"osedition_name": "Terminal Server"},
        {"osedition_name": "Professional"},
        {"osedition_name": "Advanced Server"},
        {"osedition_name": "Datacenter Server"},
        {"osedition_name": "Home"},
        {"osedition_name": "Media Center"},
        {"osedition_name": "Tablet PC"},
        {"osedition_name": "Starter"},
        {"osedition_name": "Embedded"},
        {"osedition_name": "Professional x64"},
        {"osedition_name": "Home Basic"},
        {"osedition_name": "Home Premium"},
        {"osedition_name": "Business"},
        {"osedition_name": "Enterprise"},
        {"osedition_name": "Ultimate"},
        {"osedition_name": "Core"},
        {"osedition_name": "Pro"},
        {"osedition_name": "RT"},
        {"osedition_name": "Education"},
        {"osedition_name": "Pro Education"},
        {"osedition_name": "Pro for Workstations"},
        {"osedition_name": "S"},
        {"osedition_name": "IoT Core"},
        {"osedition_name": "IoT Enterprise"},
        {"osedition_name": "Pocket PC"},
        {"osedition_name": "AutoPC"},
        {"osedition_name": "Handheld PC"},
        {"osedition_name": "Smartphone"},
        {"osedition_name": "Desktop"},
        {"osedition_name": "LTS"},
        {"osedition_name": "Cloud"},
        {"osedition_name": "Workstation"},
        {"osedition_name": "LMDE"},
        {"osedition_name": "GNOME"},
        {"osedition_name": "KDE"},
        {"osedition_name": "XFCE"},
        {"osedition_name": "Lite"},
        {"osedition_name": "Flex"},
        {"osedition_name": "Home"},
        {"osedition_name": "Security"},
    ]
    
    with Session(engine) as session:
        # Check if OS editions already exist to avoid duplicates
        existing_oseditions = session.exec(select(OSEdition)).all()
        existing_names = {osedition.osedition_name for osedition in existing_oseditions}
        
        oseditions_to_add = []
        for osedition_data in oseditions_data:
            if osedition_data["osedition_name"] not in existing_names:
                oseditions_to_add.append(OSEdition(**osedition_data))
        
        if oseditions_to_add:
            session.add_all(oseditions_to_add)
            session.commit()
            print(f"Added {len(oseditions_to_add)} OS editions to the database.")
        else:
            print("All OS editions already exist in the database.")

def seed_osversions():
    """Seed the OSVersion table with predefined OS version data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Get all existing OSEditions to create a mapping
    with Session(engine) as session:
        oseditions = session.exec(select(OSEdition)).all()
        edition_map = {edition.osedition_name: edition.osedition_id for edition in oseditions}
        
        # If we don't have "Standard" edition, create it
        if "Standard" not in edition_map:
            standard_edition = OSEdition(osedition_name="Standard")
            session.add(standard_edition)
            session.commit()
            session.refresh(standard_edition)
            edition_map["Standard"] = standard_edition.osedition_id
    
    # Function to get edition ID by name
    def get_edition_id(edition_name):
        return edition_map.get(edition_name, edition_map["Standard"])
    
    # OS Version data to insert (sample subset - in practice you'd include all 700+ versions)
    osversions_data = [
        # Windows versions with proper editions
        {"osversion_name": "Microsoft Windows 1.0-1.01", "os_id": 1, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "Microsoft Windows 1.0-1.02", "os_id": 1, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "Microsoft Windows 1.0-1.03", "os_id": 1, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "Microsoft Windows 1.0-1.04", "os_id": 1, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "Microsoft Windows 95-4.0", "os_id": 7, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "Microsoft Windows 95-4.0 OSR1", "os_id": 7, "osedition_id": get_edition_id("OEM")},
        {"osversion_name": "Microsoft Windows 95-4.0 OSR2", "os_id": 7, "osedition_id": get_edition_id("OSR2")},
        {"osversion_name": "Microsoft Windows XP-5.1", "os_id": 15, "osedition_id": get_edition_id("Home")},
        {"osversion_name": "Microsoft Windows XP-5.1 Professional", "os_id": 15, "osedition_id": get_edition_id("Professional")},
        {"osversion_name": "Microsoft Windows 10-1507", "os_id": 20, "osedition_id": get_edition_id("Home")},
        {"osversion_name": "Microsoft Windows 10-1511", "os_id": 20, "osedition_id": get_edition_id("Pro")},
        {"osversion_name": "Microsoft Windows 11-21H2", "os_id": 21, "osedition_id": get_edition_id("Home")},
        {"osversion_name": "Microsoft Windows 11-22H2", "os_id": 21, "osedition_id": get_edition_id("Pro")},
        
        # macOS versions
        {"osversion_name": "macOS-10.0 Cheetah", "os_id": 28, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "macOS-10.15 Catalina", "os_id": 28, "osedition_id": get_edition_id("Standard")},
        {"osversion_name": "macOS-15 Sequoia", "os_id": 28, "osedition_id": get_edition_id("Standard")},
        
        # Ubuntu versions with proper editions
        {"osversion_name": "Ubuntu-20.04 Focal Fossa", "os_id": 34, "osedition_id": get_edition_id("LTS")},
        {"osversion_name": "Ubuntu-22.04 Jammy Jellyfish", "os_id": 34, "osedition_id": get_edition_id("LTS")},
        {"osversion_name": "Ubuntu-24.04 Noble Numbat", "os_id": 34, "osedition_id": get_edition_id("LTS")},
        
        # Add more versions as needed - this is a subset for brevity
    ]
    
    with Session(engine) as session:
        # Check if OS versions already exist to avoid duplicates
        existing_osversions = session.exec(select(OSVersion)).all()
        existing_names = {osversion.osversion_name for osversion in existing_osversions}
        
        osversions_to_add = []
        for osversion_data in osversions_data:
            if osversion_data["osversion_name"] not in existing_names:
                osversions_to_add.append(OSVersion(**osversion_data))
        
        if osversions_to_add:
            session.add_all(osversions_to_add)
            session.commit()
            print(f"Added {len(osversions_to_add)} OS versions to the database.")
        else:
            print("All OS versions already exist in the database.")

def seed_logtypes():
    """Seed the LogType table with predefined log type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # LogType data to insert
    logtypes_data = [
        # Windows Event Logs
        {"logtype": "Windows Event Application Logs"},
        {"logtype": "Windows Event System Logs"},
        {"logtype": "Windows Event Security Logs"},
        {"logtype": "Windows Event Setup Logs"},
        {"logtype": "Windows Event Forwarded Events Logs"},
        {"logtype": "Windows Event Directory Service Logs"},
        {"logtype": "Windows Event DNS Server Logs"},
        {"logtype": "Windows Event File Replication Service Logs"},
        {"logtype": "Windows Event Hardware Events Logs"},
        {"logtype": "Windows Event Internet Explorer Logs"},
        {"logtype": "Windows Event Windows PowerShell Logs"},
        {"logtype": "Windows Event IIS Access Logs"},
        {"logtype": "Windows Event Task Scheduler Logs"},
        
        # Linux Logs
        {"logtype": "Linux Syslog"},
        {"logtype": "Linux Auth Logs"},
        {"logtype": "Linux Kernel Logs"},
        {"logtype": "Linux Boot Logs"},
        {"logtype": "Linux Cron Logs"},
        {"logtype": "Linux Mail Logs"},
        {"logtype": "Linux Apache Access Logs"},
        {"logtype": "Linux Apache Error Logs"},
        {"logtype": "Linux MySQL Logs"},
        {"logtype": "Linux Samba Logs"},
        {"logtype": "Linux X11 Logs"},
        {"logtype": "Linux Faillog"},
        {"logtype": "Linux Btmp Logs"},
        {"logtype": "Linux CUPS Print System Logs"},
        {"logtype": "Linux Rootkit Hunter Logs"},
        {"logtype": "Linux Journald Logs"},
        
        # macOS Logs
        {"logtype": "macOS System Logs"},
        {"logtype": "macOS Diagnostic Logs"},
        {"logtype": "macOS Crash Logs"},
        {"logtype": "macOS Application Logs"},
        {"logtype": "macOS Install Logs"},
        {"logtype": "macOS Daily Logs"},
        {"logtype": "macOS Weekly Logs"},
        {"logtype": "macOS Monthly Logs"},
        {"logtype": "macOS WiFi Logs"},
        {"logtype": "macOS Firewall Logs"},
        {"logtype": "macOS Power Logs"},
        {"logtype": "macOS Analytics Logs"},
    ]
    
    with Session(engine) as session:
        # Check if log types already exist to avoid duplicates
        existing_logtypes = session.exec(select(LogType)).all()
        existing_types = {logtype.logtype for logtype in existing_logtypes}
        
        logtypes_to_add = []
        for logtype_data in logtypes_data:
            if logtype_data["logtype"] not in existing_types:
                logtypes_to_add.append(LogType(**logtype_data))
        
        if logtypes_to_add:
            session.add_all(logtypes_to_add)
            session.commit()
            print(f"Added {len(logtypes_to_add)} log types to the database.")
        else:
            print("All log types already exist in the database.")

def seed_imagingmethods():
    """Seed the ImagingMethod table with predefined imaging method data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # ImagingMethod data to insert
    imagingmethods_data = [
        {"img_method": "Acronis x86_64 WinPE-5.0"},
        {"img_method": "Acronix x86_64 WinPE-4.0"},
        {"img_method": "Acronis x86_64 WinPE-3.0"},
        {"img_method": "Acronis x86_64 WinPE-3.0"},
        {"img_method": "Acronis x86 WinPE 5.0"},
        {"img_method": "Acronis x86 WinPE 4.0"},
        {"img_method": "Acronis x86 WinPE 3.0"},
        {"img_method": "Acronis x86 WinPE-3.0"},
        {"img_method": "Acronis SCS Linux x86"},
        {"img_method": "Acronis SCS Linux x86_64"},
        {"img_method": "Norton Ghost x86"},
        {"img_method": "Windows Built In BakcupImage"},
        {"img_method": "Direct Drive Cloning"},
    ]
    
    with Session(engine) as session:
        # Check if imaging methods already exist to avoid duplicates
        existing_methods = session.exec(select(ImagingMethod)).all()
        existing_method_names = {method.img_method for method in existing_methods}
        
        methods_to_add = []
        for method_data in imagingmethods_data:
            if method_data["img_method"] not in existing_method_names:
                methods_to_add.append(ImagingMethod(**method_data))
        
        if methods_to_add:
            session.add_all(methods_to_add)
            session.commit()
            print(f"Added {len(methods_to_add)} imaging methods to the database.")
        else:
            print("All imaging methods already exist in the database.")

def seed_sysarchitectures():
    """Seed the SysArchitecture table with predefined system architecture data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # SysArchitecture data to insert
    sysarchitectures_data = [
        {"sys_architecture": "x86_64"},
        {"sys_architecture": "x86"},
        {"sys_architecture": "ARM"},
        {"sys_architecture": "ARM64"},
        {"sys_architecture": "RISC-V"},
        {"sys_architecture": "IA-64"},
        {"sys_architecture": "PowerPC"},
        {"sys_architecture": "PowerPC64"},
        {"sys_architecture": "MIPS"},
        {"sys_architecture": "MIPS64"},
        {"sys_architecture": "SPARC"},
        {"sys_architecture": "SPARC64"},
        {"sys_architecture": "Alpha"},
        {"sys_architecture": "PA-RISC"},
        {"sys_architecture": "SuperH"},
        {"sys_architecture": "m68k"},
        {"sys_architecture": "AVR"},
        {"sys_architecture": "PIC"},
        {"sys_architecture": "ARMv7"},
        {"sys_architecture": "ARMv8-A"},
        {"sys_architecture": "ARMv8-R"},
        {"sys_architecture": "ARMv8-M"},
        {"sys_architecture": "ARMv9-A"},
        {"sys_architecture": "RISC-V RV32"},
        {"sys_architecture": "RISC-V RV64"},
        {"sys_architecture": "s390"},
        {"sys_architecture": "s390x"},
        {"sys_architecture": "IA-32"},
        {"sys_architecture": "Power ISA"},
        {"sys_architecture": "z/Architecture"},
        {"sys_architecture": "AVR32"},
        {"sys_architecture": "Blackfin"},
        {"sys_architecture": "Nios II"},
        {"sys_architecture": "MicroBlaze"},
        {"sys_architecture": "ARC"},
        {"sys_architecture": "Xtensa"},
        {"sys_architecture": "VAX"},
        {"sys_architecture": "RX"},
        {"sys_architecture": "E2K"},
        {"sys_architecture": "LoongArch"},
        {"sys_architecture": "Or1k"},
        {"sys_architecture": "SH-4"},
        {"sys_architecture": "68000"},
        {"sys_architecture": "8051"},
        {"sys_architecture": "RISC"},
        {"sys_architecture": "CISC"},
    ]
    
    with Session(engine) as session:
        # Check if architectures already exist to avoid duplicates
        existing_architectures = session.exec(select(SysArchitecture)).all()
        existing_architecture_names = {arch.sys_architecture for arch in existing_architectures}
        
        architectures_to_add = []
        for arch_data in sysarchitectures_data:
            if arch_data["sys_architecture"] not in existing_architecture_names:
                architectures_to_add.append(SysArchitecture(**arch_data))
        
        if architectures_to_add:
            session.add_all(architectures_to_add)
            session.commit()
            print(f"Added {len(architectures_to_add)} system architectures to the database.")
        else:
            print("All system architectures already exist in the database.")

def seed_cputypes():
    """Seed the CPUType table with predefined CPU type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # CPUType data to insert (abbreviated list for master seed file)
    cputypes_data = [
        {"cpu_name": "Intel Core i3"}, {"cpu_name": "Intel Core i5"}, {"cpu_name": "Intel Core i7"}, {"cpu_name": "Intel Core i9"},
        {"cpu_name": "AMD Ryzen 3 1200"}, {"cpu_name": "AMD Ryzen 5 1600"}, {"cpu_name": "AMD Ryzen 7 1700"}, {"cpu_name": "AMD Ryzen 9 3900X"},
        {"cpu_name": "ARM Cortex-A53"}, {"cpu_name": "ARM Cortex-A57"}, {"cpu_name": "ARM Cortex-A72"}, {"cpu_name": "ARM Cortex-A78"},
        {"cpu_name": "Apple M1"}, {"cpu_name": "Apple M2"}, {"cpu_name": "Apple M3"}, {"cpu_name": "Apple M4"},
        {"cpu_name": "Qualcomm Snapdragon 855"}, {"cpu_name": "Qualcomm Snapdragon 888"}, {"cpu_name": "Qualcomm Snapdragon 8 Gen 3"},
        {"cpu_name": "Intel Xeon E5-2600"}, {"cpu_name": "AMD EPYC 7002 Rome"}, {"cpu_name": "IBM POWER9"}
    ]
    
    with Session(engine) as session:
        # Check if CPU types already exist to avoid duplicates
        existing_cputypes = session.exec(select(CPUType)).all()
        existing_cpu_names = {cpu.cpu_name for cpu in existing_cputypes}
        
        cputypes_to_add = []
        for cpu_data in cputypes_data:
            if cpu_data["cpu_name"] not in existing_cpu_names:
                cputypes_to_add.append(CPUType(**cpu_data))
        
        if cputypes_to_add:
            session.add_all(cputypes_to_add)
            session.commit()
            print(f"Added {len(cputypes_to_add)} CPU types to the database.")
        else:
            print("All CPU types already exist in the database.")

def seed_gputypes():
    """Seed the GPUType table with predefined GPU type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # GPUType data to insert (abbreviated list for master seed file)
    gputypes_data = [
        {"gpu_name": "NVIDIA GeForce RTX 4090"}, {"gpu_name": "NVIDIA GeForce RTX 4080"}, {"gpu_name": "NVIDIA GeForce RTX 4070"},
        {"gpu_name": "NVIDIA GeForce RTX 3090"}, {"gpu_name": "NVIDIA GeForce RTX 3080"}, {"gpu_name": "NVIDIA GeForce RTX 3070"},
        {"gpu_name": "AMD Radeon RX 7900 XTX"}, {"gpu_name": "AMD Radeon RX 7800 XT"}, {"gpu_name": "AMD Radeon RX 6900 XT"},
        {"gpu_name": "Intel Arc A770"}, {"gpu_name": "Intel Arc A750"}, {"gpu_name": "Intel UHD Graphics 630"},
        {"gpu_name": "Apple GPU M1"}, {"gpu_name": "Apple GPU M2"}, {"gpu_name": "Apple GPU M3"},
        {"gpu_name": "ARM Mali-G78"}, {"gpu_name": "Qualcomm Adreno 750"}, {"gpu_name": "NVIDIA A100"}
    ]
    
    with Session(engine) as session:
        # Check if GPU types already exist to avoid duplicates
        existing_gputypes = session.exec(select(GPUType)).all()
        existing_gpu_names = {gpu.gpu_name for gpu in existing_gputypes}
        
        gputypes_to_add = []
        for gpu_data in gputypes_data:
            if gpu_data["gpu_name"] not in existing_gpu_names:
                gputypes_to_add.append(GPUType(**gpu_data))
        
        if gputypes_to_add:
            session.add_all(gputypes_to_add)
            session.commit()
            print(f"Added {len(gputypes_to_add)} GPU types to the database.")
        else:
            print("All GPU types already exist in the database.")

def seed_privilegelevels():
    """Seed the PrivilegeLevel table with predefined privilege level data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # PrivilegeLevel data to insert
    privilegelevels_data = [
        {"priv_name": "Standard User", "priv_description": ""},
        {"priv_name": "Power User", "priv_description": ""},
        {"priv_name": "Administrator", "priv_description": ""},
    ]
    
    with Session(engine) as session:
        # Check if privilege levels already exist to avoid duplicates
        existing_privilegelevels = session.exec(select(PrivilegeLevel)).all()
        existing_priv_names = {priv.priv_name for priv in existing_privilegelevels}
        
        privilegelevels_to_add = []
        for priv_data in privilegelevels_data:
            if priv_data["priv_name"] not in existing_priv_names:
                privilegelevels_to_add.append(PrivilegeLevel(**priv_data))
        
        if privilegelevels_to_add:
            session.add_all(privilegelevels_to_add)
            session.commit()
            print(f"Added {len(privilegelevels_to_add)} privilege levels to the database.")
        else:
            print("All privilege levels already exist in the database.")

def seed_departments():
    """Seed the Department table with predefined department data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Department data to insert
    departments_data = [
        {"dept_name": "System Administrators", "dept_description": ""},
        {"dept_name": "Cybersecurity", "dept_description": ""},
        {"dept_name": "Applications", "dept_description": ""},
        {"dept_name": "Database Administrators", "dept_description": ""},
        {"dept_name": "Management", "dept_description": ""},
        {"dept_name": "Test Equipment Maintenance", "dept_description": ""},
        {"dept_name": "Network Engineers", "dept_description": ""},
    ]
    
    with Session(engine) as session:
        # Check if departments already exist to avoid duplicates
        existing_departments = session.exec(select(Department)).all()
        existing_dept_names = {dept.dept_name for dept in existing_departments}
        
        departments_to_add = []
        for dept_data in departments_data:
            if dept_data["dept_name"] not in existing_dept_names:
                departments_to_add.append(Department(**dept_data))
        
        if departments_to_add:
            session.add_all(departments_to_add)
            session.commit()
            print(f"Added {len(departments_to_add)} departments to the database.")
        else:
            print("All departments already exist in the database.")

def seed_avversions():
    """Seed the AVVersion table with predefined antivirus version data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # AVVersion data to insert
    avversions_data = [
        {"av_version": "Version 2", "av_description": "McAfee VirusScan Enterprise"},
        {"av_version": "Version 3", "av_description": "Trellix Endpoint Security"},
    ]
    
    with Session(engine) as session:
        # Check if AV versions already exist to avoid duplicates
        existing_avversions = session.exec(select(AVVersion)).all()
        existing_av_versions = {av.av_version for av in existing_avversions}
        
        avversions_to_add = []
        for av_data in avversions_data:
            if av_data["av_version"] not in existing_av_versions:
                avversions_to_add.append(AVVersion(**av_data))
        
        if avversions_to_add:
            session.add_all(avversions_to_add)
            session.commit()
            print(f"Added {len(avversions_to_add)} AV versions to the database.")
        else:
            print("All AV versions already exist in the database.")

def seed_datversions():
    """Seed the DatVersion table with predefined DAT version data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # DatVersion data to insert
    datversions_data = [
        {"datversion_name": "Version02 Datfiles", "avversion_id": 1},
        {"datversion_name": "Version03 Datfiles", "avversion_id": 2},
    ]
    
    with Session(engine) as session:
        # Check if DAT versions already exist to avoid duplicates
        existing_datversions = session.exec(select(DatVersion)).all()
        existing_datversion_names = {dv.datversion_name for dv in existing_datversions}
        
        datversions_to_add = []
        for dat_data in datversions_data:
            if dat_data["datversion_name"] not in existing_datversion_names:
                datversions_to_add.append(DatVersion(**dat_data))
        
        if datversions_to_add:
            session.add_all(datversions_to_add)
            session.commit()
            print(f"Added {len(datversions_to_add)} DAT versions to the database.")
        else:
            print("All DAT versions already exist in the database.")

def seed_employees():
    """Seed the Employee table with predefined employee data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Employee data to insert (id will be auto-generated)
    employees_data = [
        {"first_name": "Kyle", "last_name": "Hurston", "email": "kyle.m.civ@army.mil", "department_id": 2},
        {"first_name": "David", "last_name": "Felmlee", "email": "david.felmlee.civ@army.mil", "department_id": 2},
        {"first_name": "Robert", "last_name": "Shipp", "email": "robert.shipp.2.civ@army.mil", "department_id": 5},
        {"first_name": "Mary", "last_name": "Steigerwald", "email": "mary.steigerwald.civ@army.mil", "department_id": 5},
        {"first_name": "Craig", "last_name": "Alleman", "email": "craig.alleman.civ@army.mil", "department_id": 2},
        {"first_name": "Justin", "last_name": "Ile", "email": "justin.ile.civ@army.mil", "department_id": 6},
        {"first_name": "Tim", "last_name": "Rhoades", "email": "tim.rhoades.civ@army.mil", "department_id": 6},
        {"first_name": "Tim", "last_name": "Blacker", "email": "tim.blacker.civ@army.mil", "department_id": 6},
        {"first_name": "Barry", "last_name": "Crawford", "email": "barry.crawford.civ@army.mil", "department_id": 4},
    ]
    
    with Session(engine) as session:
        # Check if employees already exist to avoid duplicates
        existing_employees = session.exec(select(Employee)).all()
        existing_emails = {emp.email for emp in existing_employees}
        
        employees_to_add = []
        for emp_data in employees_data:
            if emp_data["email"] not in existing_emails:
                employees_to_add.append(Employee(**emp_data))
        
        if employees_to_add:
            session.add_all(employees_to_add)
            session.commit()
            print(f"Added {len(employees_to_add)} employees to the database.")
        else:
            print("All employees already exist in the database.")

def seed_appusers():
    """Seed the AppUser table with predefined application user data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # AppUser data to insert (id will be auto-generated)
    appusers_data = [
        {"first_name": "Kyle", "last_name": "Hurston", "email": "kyle.m.hurston.civ@army.mil", "phone": None, "employee_id": 1, "department_id": 2, "priv_level_id": 3},
        {"first_name": "David", "last_name": "Felmlee", "email": "david.felmlee.civ@army.mil", "phone": None, "employee_id": 2, "department_id": 2, "priv_level_id": 3},
        {"first_name": "Robert", "last_name": "Shipp", "email": "robert.shipp.2.civ@army.mil", "phone": None, "employee_id": 3, "department_id": 5, "priv_level_id": 3},
        {"first_name": "Mary", "last_name": "Steigerwald", "email": "mary.steigerwald.civ@army.mil", "phone": None, "employee_id": 4, "department_id": 5, "priv_level_id": 3},
        {"first_name": "Craig", "last_name": "Alleman", "email": "craig.alleman.civ@army.mil", "phone": None, "employee_id": 5, "department_id": 2, "priv_level_id": 3},
        {"first_name": "Justin", "last_name": "Ile", "email": "justin.ile.civ@army.mil", "phone": None, "employee_id": 6, "department_id": 6, "priv_level_id": 2},
        {"first_name": "Tim", "last_name": "Rhoades", "email": "tim.rhoades.civ@army.mil", "phone": None, "employee_id": 7, "department_id": 6, "priv_level_id": 2},
        {"first_name": "Tim", "last_name": "Blacker", "email": "tim.blacker.civ@army.mil", "phone": None, "employee_id": 8, "department_id": 6, "priv_level_id": 1},
        {"first_name": "Barry", "last_name": "Crawford", "email": "barry.crawford.civ@army.mil", "phone": None, "employee_id": 9, "department_id": 4, "priv_level_id": 3},
    ]
    
    with Session(engine) as session:
        # Check if app users already exist to avoid duplicates
        existing_appusers = session.exec(select(AppUser)).all()
        existing_emails = {user.email for user in existing_appusers}
        
        appusers_to_add = []
        for user_data in appusers_data:
            if user_data["email"] not in existing_emails:
                appusers_to_add.append(AppUser(**user_data))
        
        if appusers_to_add:
            session.add_all(appusers_to_add)
            session.commit()
            print(f"Added {len(appusers_to_add)} app users to the database.")
        else:
            print("All app users already exist in the database.")

def seed_rooms():
    """Seed the Room table with predefined room data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Room data to insert (building_id, floor_id, room_name)
    rooms_data = [
        {"building_id": 1, "floor_id": 8, "room_name": "Gets PTCI / Test Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "Hawk DTE / Test Console Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "Steve Moritz Power Supply Test Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "201 / CRG ECT ICC & Radar Staging Area"},
        {"building_id": 1, "floor_id": 8, "room_name": "201 / Hawk HFC / DTE Support Equipment Area"},
        {"building_id": 1, "floor_id": 7, "room_name": "AGPU Pump Area"},
        {"building_id": 1, "floor_id": 7, "room_name": "Hoist Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Boom Extension Test Set Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable & Harness Test Set Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable & Harness Fiber Optics Cell Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "DITMCO / User Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Cable Harness Wire Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Element Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Coolant Resevoir Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Hawk / Patriot Mechanical Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Circuit Card Rear Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Circuit Card Microwave Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Radar Antenna Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Avenger LRU Disassembly Area"},
        {"building_id": 2, "floor_id": 9, "room_name": "Multi Project Dip Tank Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "High Power Room"},
        {"building_id": 1, "floor_id": 9, "room_name": "Traversing Unit Test Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "IFTE Test Console Area"},
        {"building_id": 1, "floor_id": 9, "room_name": "Avenger Flir ODU Production Area"},
    ]
    
    with Session(engine) as session:
        # Check if rooms already exist to avoid duplicates
        existing_rooms = session.exec(select(Room)).all()
        existing_combinations = {(room.building_id, room.floor_id, room.room_name) for room in existing_rooms}
        
        rooms_to_add = []
        for room_data in rooms_data:
            room_combination = (room_data["building_id"], room_data["floor_id"], room_data["room_name"])
            if room_combination not in existing_combinations:
                rooms_to_add.append(Room(**room_data))
        
        if rooms_to_add:
            session.add_all(rooms_to_add)
            session.commit()
            print(f"Added {len(rooms_to_add)} rooms to the database.")
        else:
            print("All rooms already exist in the database.")

def seed_vmtypes():
    """Seed the VMType table with predefined virtual machine type data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VMType data to insert
    vmtypes_data = [
        {"vm_type": "HyperV Virtual Machine Type 1"},
        {"vm_type": "HyperV Virtual Machine Type 2"},
    ]
    
    with Session(engine) as session:
        # Check if vmtypes already exist to avoid duplicates
        existing_vmtypes = session.exec(select(VMType)).all()
        existing_types = {vmtype.vm_type for vmtype in existing_vmtypes}
        
        vmtypes_to_add = []
        for vmtype_data in vmtypes_data:
            if vmtype_data["vm_type"] not in existing_types:
                vmtypes_to_add.append(VMType(**vmtype_data))
        
        if vmtypes_to_add:
            session.add_all(vmtypes_to_add)
            session.commit()
            print(f"Added {len(vmtypes_to_add)} VM types to the database.")
        else:
            print("All VM types already exist in the database.")

def seed_virtualization_sources():
    """Seed the VirtualizationSource table with predefined virtualization source data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VirtualizationSource data to insert
    virtualization_sources_data = [
        {"virt_source": "UHA Virtualization Server"},
        {"virt_source": "UHB Virtualization Server"},
    ]
    
    with Session(engine) as session:
        # Check if virtualization sources already exist to avoid duplicates
        existing_sources = session.exec(select(VirtualizationSource)).all()
        existing_source_names = {source.virt_source for source in existing_sources}
        
        sources_to_add = []
        for source_data in virtualization_sources_data:
            if source_data["virt_source"] not in existing_source_names:
                sources_to_add.append(VirtualizationSource(**source_data))
        
        if sources_to_add:
            session.add_all(sources_to_add)
            session.commit()
            print(f"Added {len(sources_to_add)} virtualization sources to the database.")
        else:
            print("All virtualization sources already exist in the database.")

def seed_vm_statuses():
    """Seed the VMStatus table with predefined VM status data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # VMStatus data to insert
    vm_statuses_data = [
        {"vm_status": "Fully Functional | Ready For Use"},
        {"vm_status": "Fully Functional | Waiting For Scans"},
        {"vm_status": "Machine Created | Testing Startup Processes"},
        {"vm_status": "Non-Functional VM | Boot Sequence Errors"},
        {"vm_status": "Non-Functional VM | Driver Related Errors"},
        {"vm_status": "Non-Functional VM | Unknown Virtualization Errors"},
        {"vm_status": "Non-Functional VM | Data Available For Extraction At Request"},
    ]
    
    with Session(engine) as session:
        # Check if VM statuses already exist to avoid duplicates
        existing_statuses = session.exec(select(VMStatus)).all()
        existing_status_names = {status.vm_status for status in existing_statuses}
        
        statuses_to_add = []
        for status_data in vm_statuses_data:
            if status_data["vm_status"] not in existing_status_names:
                statuses_to_add.append(VMStatus(**status_data))
        
        if statuses_to_add:
            session.add_all(statuses_to_add)
            session.commit()
            print(f"Added {len(statuses_to_add)} VM statuses to the database.")
        else:
            print("All VM statuses already exist in the database.")

def seed_assets():
    """Seed the Asset table with baseline asset data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Asset data to insert
    # Format: (asset_name, project_id, building_id, floor_id, room_id, systype_id)
    assets_data = [
        {"asset_name": "ifmc.gets5a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets5b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets6a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets6b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets12a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets12b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets14a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets14b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets22a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets22b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        
        # Assets with unknown room locations - leaving room_id as None
        {"asset_name": "ifmc.gets25a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.gets26a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.gets30a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.gets35a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets35b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets27a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets28a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets29a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets39a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets40a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets42a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 41, "systype_id": 1},
        {"asset_name": "ifmc.gets42b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 41, "systype_id": 1},
        {"asset_name": "ifmc.laselec", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.defluxleft", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 39, "systype_id": 1},
        {"asset_name": "ifmc.defluxright", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 39, "systype_id": 1},
        {"asset_name": "ifmc.e2ic", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.vmeconsole", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.pfom", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 26, "systype_id": 1},
        {"asset_name": "ifmc.244m", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 28, "systype_id": 1},
        {"asset_name": "ifmc.247m", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 45, "systype_id": 1},
        {"asset_name": "ifmc.248a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 45, "systype_id": 1},
        {"asset_name": "ifmc.2058", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.2258", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 42, "systype_id": 1},
        
        # Asset with unknown room location - leaving room_id as None
        {"asset_name": "ifmc.2260", "project_id": 1, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.2259", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 42, "systype_id": 1},
        
        # Assets in other buildings with unknown room locations - leaving room_id as None
        {"asset_name": "ifmc.ftk1", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ftk2", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ftk3", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.hydraulic", "project_id": 1, "building_id": 7, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.termini", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 33, "systype_id": 1},
        
        # SHIELD project assets
        {"asset_name": "shield.afcc", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.geotest", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ir6100", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.ir6600", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.flir", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 48, "systype_id": 1},
        {"asset_name": "shield.ngats", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte1", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte2", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte3", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        
        # STARE project assets
        {"asset_name": "stare.wirestrip", "project_id": 3, "building_id": 1, "floor_id": 9, "room_id": 36, "systype_id": 1},
        {"asset_name": "stare.piu", "project_id": 3, "building_id": 1, "floor_id": 8, "room_id": 26, "systype_id": 2},
        
        # STORM project assets
        {"asset_name": "storm.chant", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.testek", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 30, "systype_id": 1},
        {"asset_name": "storm.tropel", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 30, "systype_id": 1},
        {"asset_name": "storm.gearbox", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.boom", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.shaker", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.blue", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        # MULTI project assets  
        {"asset_name": "multi.honeywell", "project_id": 5, "building_id": 2, "floor_id": 9, "room_id": 44, "systype_id": 1},
        
        # TAGM project assets
        {"asset_name": "tagm.tuts", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": 46, "systype_id": 1},
        {"asset_name": "tagm.jsts004", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "tagm.jsts800", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "tagm.mlv", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # Additional STORM assets
        {"asset_name": "storm.pump", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        # Additional IFMC numbered assets
        {"asset_name": "ifmc.226114", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.226118", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.2271", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.2275", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # Additional IFMC test equipment
        {"asset_name": "ifmc.actuatortest", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.hoffman", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.legacythermal", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.lts1", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ltsctc", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.nts1", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.nts2", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.thermal", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.v281", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.v323", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.vmeprogrammer", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # IFMC Oscilloscopes (Digital Oscilloscope - systype_id: 4)
        {"asset_name": "ifmc.oscope.aqg485", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.bgv085", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn4024", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn5201", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6242", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6256", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6309", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6310", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6312", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6387", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.hxx865", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.r7057", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zue544", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zuf375", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zug348", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zug356", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        
        # IFMC Analyzers (Signal Analyzer - systype_id: 5)
        {"asset_name": "ifmc.analyzer.5617", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.bgv083", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn4322", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5612", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5625", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5626", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6111", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6129", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6378", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6473", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6615", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.hxr172", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
    ]
    
    with Session(engine) as session:
        # Check if assets already exist to avoid duplicates
        existing_assets = session.exec(select(Asset)).all()
        existing_names = {asset.asset_name for asset in existing_assets}
        
        assets_to_add = []
        skipped_assets = []
        
        for asset_data in assets_data:
            if asset_data["asset_name"] not in existing_names:
                try:
                    assets_to_add.append(Asset(**asset_data))
                except Exception as e:
                    skipped_assets.append((asset_data["asset_name"], str(e)))
            else:
                skipped_assets.append((asset_data["asset_name"], "Already exists"))
        
        if assets_to_add:
            session.add_all(assets_to_add)
            session.commit()
            print(f"Added {len(assets_to_add)} assets to the database.")
        else:
            print("No new assets to add.")
        
        if skipped_assets:
            print(f"\nSkipped {len(skipped_assets)} assets:")
            for name, reason in skipped_assets:
                print(f"  - {name}: {reason}")

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

def run_all_seeds():
    """Run all seed functions in the correct order to avoid foreign key constraint errors."""
    print("Starting database seeding process...")
    
    # Run seed functions in dependency order
    seed_buildings()
    seed_floors()
    seed_systypes()
    seed_hardware_manufacturers()
    seed_sw_manufacturers()
    seed_projects()
    seed_operating_systems()
    seed_oseditions()
    seed_osversions()
    seed_logtypes()
    seed_imagingmethods()
    seed_sysarchitectures()
    seed_cputypes()
    seed_gputypes()
    seed_vmtypes()
    seed_virtualization_sources()
    seed_vm_statuses()
    seed_privilegelevels()
    seed_departments()
    seed_avversions()
    seed_datversions()
    seed_employees()
    seed_appusers()
    seed_rooms()
    seed_assets()
    seed_software_catalog()
    
    print("Database seeding process completed.")

if __name__ == "__main__":
    run_all_seeds()