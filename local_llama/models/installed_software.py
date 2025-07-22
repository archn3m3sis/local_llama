from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class InstalledSoftware(SQLModel, table=True):
    """Track installed software on assets."""
    
    software_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    sw_name: str = Field(max_length=200)
    sw_version: Optional[str] = Field(max_length=50, default=None)
    sw_vendor: Optional[int] = Field(foreign_key="swmanufacturer.swmanu_id", default=None)
    install_date: Optional[datetime] = Field(default=None)
    install_path: Optional[str] = Field(max_length=500, default=None)
    license_key: Optional[str] = Field(max_length=200, default=None)
    license_type: Optional[str] = Field(max_length=50, default=None)  # 'perpetual', 'subscription', 'trial'
    license_expiry: Optional[datetime] = Field(default=None)
    discovered_date: datetime = Field(default_factory=datetime.now)
    last_seen: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    is_approved: bool = Field(default=True)  # For tracking unauthorized software