from typing import Optional
from sqlmodel import SQLModel, Field


class VirtualMachine(SQLModel, table=True):
    virtmachine_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    project_id: int = Field(foreign_key="project.project_id")
    imgcollection_id: int = Field(foreign_key="imagecollection.imgcollection_id")
    virtsource_id: int = Field(foreign_key="virtualizationsource.virtsource_id")
    creator_employee_id: int = Field(foreign_key="employee.id")
    vmtype_id: int = Field(foreign_key="vmtype.vmtype_id")
    vmstatus_id: int = Field(foreign_key="vmstatus.vmstatus_id")
    
    # VM Specifications
    ram_mb: Optional[int] = Field(default=None, description="RAM in MB")
    cpu_cores: Optional[int] = Field(default=None, description="Number of CPU cores")
    disk_size_mb: Optional[int] = Field(default=None, description="Disk size in MB")
    
    # Scan Status
    acas_scan_completed: bool = Field(default=False)
    scap_scan_completed: bool = Field(default=False)