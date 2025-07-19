from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Asset(SQLModel, table=True):
    asset_id: Optional[int] = Field(default=None, primary_key=True)
    asset_name: str = Field(max_length=100)
    project_id: int = Field(foreign_key="project.project_id")
    serial_no: Optional[str] = Field(max_length=100, default=None)
    letterkenny_barcode: Optional[str] = Field(max_length=100, default=None)
    building_id: int = Field(foreign_key="building.building_id")
    floor_id: int = Field(foreign_key="floor.floor_id")
    room_id: Optional[int] = Field(foreign_key="room.room_id", default=None)
    systype_id: int = Field(foreign_key="systype.systype_id")
    hwmanu_id: Optional[int] = Field(foreign_key="hardwaremanufacturer.hwmanu_id", default=None)
    os_id: Optional[int] = Field(foreign_key="operatingsystem.os_id", default=None)
    osedition_id: Optional[int] = Field(foreign_key="osedition.osedition_id", default=None)
    osversion_id: Optional[int] = Field(foreign_key="osversion.osversion_id", default=None)
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