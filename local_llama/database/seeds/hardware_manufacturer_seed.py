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
    
    # Hardware manufacturer data to insert (name, weblink, phone_number)
    hardware_manufacturers_data = [
        {"hwmanu_name": "Apple", "weblink": "https://www.apple.com", "phone_number": "1-800-275-2273"},
        {"hwmanu_name": "Asus", "weblink": "https://www.asus.com", "phone_number": "1-888-678-3688"},
        {"hwmanu_name": "Dell", "weblink": "https://www.dell.com", "phone_number": "1-800-624-9896"},
        {"hwmanu_name": "HP", "weblink": "https://www.hp.com", "phone_number": "1-800-752-0900"},
        {"hwmanu_name": "HTC", "weblink": "https://www.htc.com", "phone_number": "1-800-824-6779"},
        {"hwmanu_name": "Lenovo", "weblink": "https://www.lenovo.com", "phone_number": "1-855-253-6686"},
        {"hwmanu_name": "Nintendo", "weblink": "https://www.nintendo.com", "phone_number": "1-800-255-3700"},
        {"hwmanu_name": "Sony", "weblink": "https://www.sony.com", "phone_number": "1-800-345-7669"},
        {"hwmanu_name": "Acer", "weblink": "https://www.acer.com", "phone_number": "1-866-695-2237"},
        {"hwmanu_name": "Microsoft", "weblink": "https://www.microsoft.com", "phone_number": "1-800-426-9400"},
        {"hwmanu_name": "Samsung", "weblink": "https://www.samsung.com", "phone_number": "1-800-726-7864"},
        {"hwmanu_name": "Toshiba", "weblink": "https://www.toshiba.com", "phone_number": "1-877-323-0017"},
        {"hwmanu_name": "MSI", "weblink": "https://www.msi.com", "phone_number": "1-888-447-6564"},
        {"hwmanu_name": "IBM", "weblink": "https://www.ibm.com", "phone_number": "1-800-426-4968"},
        {"hwmanu_name": "NEC", "weblink": "https://www.nec.com", "phone_number": "1-800-852-4632"},
        {"hwmanu_name": "Fujitsu", "weblink": "https://www.fujitsu.com", "phone_number": "1-800-831-3183"},
        {"hwmanu_name": "Intel", "weblink": "https://www.intel.com", "phone_number": "1-800-538-3373"},
        {"hwmanu_name": "AMD", "weblink": "https://www.amd.com", "phone_number": "1-877-284-1566"},
        {"hwmanu_name": "NVIDIA", "weblink": "https://www.nvidia.com", "phone_number": "1-408-486-2000"},
        {"hwmanu_name": "Qualcomm", "weblink": "https://www.qualcomm.com", "phone_number": "1-858-587-1121"},
        {"hwmanu_name": "Broadcom", "weblink": "https://www.broadcom.com", "phone_number": "1-408-433-8000"},
        {"hwmanu_name": "Texas Instruments", "weblink": "https://www.ti.com", "phone_number": "1-972-995-2011"},
        {"hwmanu_name": "Cisco", "weblink": "https://www.cisco.com", "phone_number": "1-800-553-2447"},
        {"hwmanu_name": "Juniper Networks", "weblink": "https://www.juniper.net", "phone_number": "1-888-314-5822"},
        {"hwmanu_name": "Arista Networks", "weblink": "https://www.arista.com", "phone_number": "1-408-547-5500"},
        {"hwmanu_name": "Extreme Networks", "weblink": "https://www.extremenetworks.com", "phone_number": "1-800-998-2408"},
        {"hwmanu_name": "Ruckus Networks", "weblink": "https://www.ruckusnetworks.com", "phone_number": "1-650-265-0903"},
        {"hwmanu_name": "CommScope", "weblink": "https://www.commscope.com", "phone_number": "1-828-324-2200"},
        {"hwmanu_name": "Foxconn", "weblink": "https://www.foxconn.com", "phone_number": "+886-2-2268-3466"},
        {"hwmanu_name": "LG", "weblink": "https://www.lg.com", "phone_number": "1-800-243-0000"},
        {"hwmanu_name": "Seagate", "weblink": "https://www.seagate.com", "phone_number": "1-800-732-4283"},
        {"hwmanu_name": "Western Digital", "weblink": "https://www.westerndigital.com", "phone_number": "1-800-275-4932"},
        {"hwmanu_name": "Kingston", "weblink": "https://www.kingston.com", "phone_number": "1-800-435-0640"},
        {"hwmanu_name": "Corsair", "weblink": "https://www.corsair.com", "phone_number": "1-888-222-4346"},
        {"hwmanu_name": "Logitech", "weblink": "https://www.logitech.com", "phone_number": "1-646-454-3200"},
        {"hwmanu_name": "Razer", "weblink": "https://www.razer.com", "phone_number": "1-888-697-2037"},
        {"hwmanu_name": "SteelSeries", "weblink": "https://steelseries.com", "phone_number": "1-312-566-4101"},
        {"hwmanu_name": "Belkin", "weblink": "https://www.belkin.com", "phone_number": "1-800-223-5546"},
        {"hwmanu_name": "Netgear", "weblink": "https://www.netgear.com", "phone_number": "1-888-638-4327"},
        {"hwmanu_name": "TP-Link", "weblink": "https://www.tp-link.com", "phone_number": "1-866-225-8139"},
        {"hwmanu_name": "D-Link", "weblink": "https://www.dlink.com", "phone_number": "1-877-453-5465"},
        {"hwmanu_name": "Linksys", "weblink": "https://www.linksys.com", "phone_number": "1-800-546-5797"},
        {"hwmanu_name": "Super Micro Computer", "weblink": "https://www.supermicro.com", "phone_number": "1-408-503-8000"},
        {"hwmanu_name": "ASML", "weblink": "https://www.asml.com", "phone_number": "+31-40-268-3000"},
        {"hwmanu_name": "Applied Materials", "weblink": "https://www.appliedmaterials.com", "phone_number": "1-408-727-5555"},
        {"hwmanu_name": "Arm", "weblink": "https://www.arm.com", "phone_number": "+1-408-576-1500"},
        {"hwmanu_name": "SiFive", "weblink": "https://www.sifive.com", "phone_number": "1-415-673-2836"},
        {"hwmanu_name": "TSMC", "weblink": "https://www.tsmc.com", "phone_number": "+886-3-563-6688"},
        {"hwmanu_name": "Hon Hai Precision", "weblink": "https://www.honhai.com", "phone_number": "+886-2-2268-3466"},
        {"hwmanu_name": "RTX", "weblink": "https://www.rtx.com", "phone_number": "1-781-522-3000"},
        {"hwmanu_name": "Boeing", "weblink": "https://www.boeing.com", "phone_number": "1-312-544-2000"},
        {"hwmanu_name": "Lockheed Martin", "weblink": "https://www.lockheedmartin.com", "phone_number": "1-301-897-6000"},
        {"hwmanu_name": "Northrop Grumman", "weblink": "https://www.northropgrumman.com", "phone_number": "1-703-280-2900"},
        {"hwmanu_name": "General Dynamics", "weblink": "https://www.gd.com", "phone_number": "1-703-876-3000"},
        {"hwmanu_name": "BAE Systems", "weblink": "https://www.baesystems.com", "phone_number": "+44-1252-373232"},
        {"hwmanu_name": "L3Harris Technologies", "weblink": "https://www.l3harris.com", "phone_number": "1-321-727-9100"},
        {"hwmanu_name": "Huntington Ingalls Industries", "weblink": "https://www.hii.com", "phone_number": "1-757-380-2000"},
        {"hwmanu_name": "Leidos", "weblink": "https://www.leidos.com", "phone_number": "1-571-526-6000"},
        {"hwmanu_name": "Airbus", "weblink": "https://www.airbus.com", "phone_number": "+33-5-6193-3333"},
        {"hwmanu_name": "Thales", "weblink": "https://www.thalesgroup.com", "phone_number": "+33-1-5777-8000"},
        {"hwmanu_name": "Leonardo", "weblink": "https://www.leonardo.com", "phone_number": "+39-06-324731"},
        {"hwmanu_name": "Saab", "weblink": "https://www.saab.com", "phone_number": "+46-13-180000"},
        {"hwmanu_name": "Rheinmetall", "weblink": "https://www.rheinmetall.com", "phone_number": "+49-211-47301"},
        {"hwmanu_name": "Elbit Systems", "weblink": "https://elbitsystems.com", "phone_number": "+972-77-294-6661"},
        {"hwmanu_name": "Canon", "weblink": "https://www.canon.com", "phone_number": "+81-3-3758-2111"},
        {"hwmanu_name": "Xiaomi", "weblink": "https://www.xiaomi.com", "phone_number": "+86-400-100-5678"},
        {"hwmanu_name": "Huawei", "weblink": "https://www.huawei.com", "phone_number": "+86-755-2878-0808"},
        {"hwmanu_name": "Panasonic", "weblink": "https://www.panasonic.com", "phone_number": "+81-6-6908-1121"},
        {"hwmanu_name": "Sharp", "weblink": "https://global.sharp", "phone_number": "+81-6-6621-1221"},
        {"hwmanu_name": "Hitachi", "weblink": "https://www.hitachi.com", "phone_number": "+81-3-3258-1111"},
        {"hwmanu_name": "Oracle", "weblink": "https://www.oracle.com", "phone_number": "1-800-392-2999"},
        {"hwmanu_name": "HPE", "weblink": "https://www.hpe.com", "phone_number": "1-888-342-2156"},
        {"hwmanu_name": "Micron", "weblink": "https://www.micron.com", "phone_number": "1-208-368-4000"},
        {"hwmanu_name": "SK Hynix", "weblink": "https://www.skhynix.com", "phone_number": "+82-31-5185-4114"},
        {"hwmanu_name": "Epson", "weblink": "https://www.epson.com", "phone_number": "1-800-463-7766"},
        {"hwmanu_name": "Brother Industries", "weblink": "https://www.brother.com", "phone_number": "1-877-276-8437"},
        {"hwmanu_name": "GlobalFoundries", "weblink": "https://www.gf.com", "phone_number": "1-518-305-9013"},
        {"hwmanu_name": "Ericsson", "weblink": "https://www.ericsson.com", "phone_number": "+46-10-719-0000"},
        {"hwmanu_name": "Nokia", "weblink": "https://www.nokia.com", "phone_number": "+358-10-4488-000"},
        {"hwmanu_name": "Gigabyte Technology", "weblink": "https://www.gigabyte.com", "phone_number": "+886-2-8912-4000"},
        {"hwmanu_name": "ASRock", "weblink": "https://www.asrock.com", "phone_number": "+886-2-2896-5588"},
        {"hwmanu_name": "Biostar", "weblink": "https://www.biostar.com.tw", "phone_number": "+886-2-2218-0150"},
        {"hwmanu_name": "EVGA", "weblink": "https://www.evga.com", "phone_number": "1-888-881-3842"},
        {"hwmanu_name": "Antec", "weblink": "https://www.antec.com", "phone_number": "1-510-770-1200"},
        {"hwmanu_name": "Cooler Master", "weblink": "https://www.coolermaster.com", "phone_number": "1-888-624-5099"},
        {"hwmanu_name": "Lian Li", "weblink": "https://www.lian-li.com", "phone_number": "+886-2-2459-8989"},
        {"hwmanu_name": "Thermaltake", "weblink": "https://www.thermaltake.com", "phone_number": "1-909-598-1888"},
        {"hwmanu_name": "Sapphire Technology", "weblink": "https://www.sapphiretech.com", "phone_number": "+852-2687-8888"},
        {"hwmanu_name": "Zotac", "weblink": "https://www.zotac.com", "phone_number": "+852-2793-6363"},
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