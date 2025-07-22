from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class NetworkInterface(SQLModel, table=True):
    """Track network interfaces and configurations for assets."""
    
    interface_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    interface_name: str = Field(max_length=50)
    mac_address: Optional[str] = Field(max_length=17, default=None)
    ip_address: Optional[str] = Field(max_length=45, default=None)  # Support IPv6
    subnet_mask: Optional[str] = Field(max_length=45, default=None)
    gateway: Optional[str] = Field(max_length=45, default=None)
    dns_primary: Optional[str] = Field(max_length=45, default=None)
    dns_secondary: Optional[str] = Field(max_length=45, default=None)
    vlan_id: Optional[int] = Field(default=None)
    is_active: bool = Field(default=True)
    last_updated: datetime = Field(default_factory=datetime.now)