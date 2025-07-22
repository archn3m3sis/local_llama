from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class AssetSoftware(SQLModel, table=True):
    """Junction table for many-to-many relationship between assets and software."""
    
    asset_software_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    software_catalog_id: int = Field(foreign_key="softwarecatalog.software_catalog_id")
    installed_version: Optional[str] = Field(max_length=50, default=None)
    install_date: Optional[datetime] = Field(default=None)
    install_path: Optional[str] = Field(max_length=500, default=None)
    install_method: Optional[str] = Field(max_length=50, default=None)  # 'manual', 'automated', 'image'
    installed_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    license_key: Optional[str] = Field(max_length=200, default=None)
    license_assigned_date: Optional[datetime] = Field(default=None)
    license_expiry_date: Optional[datetime] = Field(default=None)
    discovered_date: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    uninstall_date: Optional[datetime] = Field(default=None)
    uninstalled_by: Optional[int] = Field(foreign_key="employee.id", default=None)