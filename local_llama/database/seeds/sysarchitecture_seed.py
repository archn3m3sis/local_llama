from sqlmodel import Session, create_engine, select
from local_llama.models.sys_architecture import SysArchitecture
import os
from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    seed_sysarchitectures()