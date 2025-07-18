from sqlmodel import Session, create_engine, select
from local_llama.models.hardware_manufacturer import HardwareManufacturer
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    seed_hardware_manufacturers()