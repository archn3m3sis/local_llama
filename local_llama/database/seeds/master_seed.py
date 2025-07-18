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

def run_all_seeds():
    """Run all seed functions in the correct order to avoid foreign key constraint errors."""
    print("Starting database seeding process...")
    
    # Run seed functions in dependency order
    seed_buildings()
    seed_floors()
    seed_systypes()
    seed_hardware_manufacturers()
    seed_sw_manufacturers()
    
    print("Database seeding process completed.")

if __name__ == "__main__":
    run_all_seeds()