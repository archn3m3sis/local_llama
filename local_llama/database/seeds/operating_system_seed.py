from sqlmodel import Session, create_engine, select
from local_llama.models.operating_system import OperatingSystem
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    seed_operating_systems()