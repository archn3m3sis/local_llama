from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Asset(SQLModel, table=True):
    asset_id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.project_id")
    serial_no: str = Field(max_length=100)
    letterkenny_barcode: str = Field(max_length=100)
    building_id: int = Field(foreign_key="building.building_id")
    floor_id: int = Field(foreign_key="floor.floor_id")
    room_id: int = Field(foreign_key="room.room_id")
    systype_id: int = Field(foreign_key="systype.systype_id")
    hwmanu_id: int = Field(foreign_key="hardwaremanufacturer.hwmanu_id")
    os_id: int = Field(foreign_key="operatingsystem.os_id")
    osedition_id: int = Field(foreign_key="osedition.osedition_id")
    osversion_id: int = Field(foreign_key="osversion.osversion_id")
    physical_memory: Optional[int] = Field(default=None)
    physical_storage_total: Optional[int] = Field(default=None)
    physical_storage_used: Optional[int] = Field(default=None)
    physical_storage_remaining: Optional[int] = Field(default=None)
    av_deployment: bool = Field(default=False)
    cpu_id: Optional[int] = Field(foreign_key="cputype.cpu_id", default=None)
    gpu_id: Optional[int] = Field(foreign_key="gputype.gpu_id", default=None)
    last_acas_scan: Optional[datetime] = Field(default=None)
    last_scap_scan: Optional[datetime] = Field(default=None)
    last_log_collection: Optional[datetime] = Field(default=None)
    last_image_collection: Optional[datetime] = Field(default=None)
    last_datfile_update: Optional[datetime] = Field(default=None)