from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class SoftwareCatalog(SQLModel, table=True):
    """Master catalog of all software products."""
    
    software_catalog_id: Optional[int] = Field(default=None, primary_key=True)
    sw_name: str = Field(max_length=200, unique=True)
    sw_vendor: Optional[int] = Field(foreign_key="swmanufacturer.swmanu_id", default=None)
    sw_category: Optional[str] = Field(max_length=50, default=None)  # 'OS', 'Security', 'Productivity', 'Development'
    sw_type: Optional[str] = Field(max_length=50, default=None)  # 'Application', 'Driver', 'Firmware', 'Patch'
    latest_version: Optional[str] = Field(max_length=50, default=None)
    sw_architecture_compatibility: Optional[str] = Field(max_length=500, default=None)  # CSV list of architectures
    dod_compliant: bool = Field(default=False)  # DoD compliance status
    compliance_status: Optional[str] = Field(max_length=50, default=None)  # Extended compliance status
    army_gold_master: bool = Field(default=False)  # Part of Army baseline OS deployment image
    is_approved: bool = Field(default=True)  # Approved for use in organization
    is_licensed: bool = Field(default=True)  # Requires license
    license_model: Optional[str] = Field(max_length=50, default=None)  # 'per-seat', 'site', 'subscription'
    eol_date: Optional[datetime] = Field(default=None)  # End of life date
    description: Optional[str] = Field(default=None)
    created_date: datetime = Field(default_factory=datetime.now)
    updated_date: datetime = Field(default_factory=datetime.now)