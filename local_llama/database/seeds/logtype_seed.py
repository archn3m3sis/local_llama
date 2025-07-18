from sqlmodel import Session, create_engine, select
from local_llama.models.log_type import LogType
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    seed_logtypes()