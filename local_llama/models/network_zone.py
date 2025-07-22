from typing import Optional
from sqlmodel import SQLModel, Field


class NetworkZone(SQLModel, table=True):
    """Define network zones and security segments."""
    
    zone_id: Optional[int] = Field(default=None, primary_key=True)
    zone_name: str = Field(max_length=100)
    zone_description: Optional[str] = Field(default=None)
    security_level: int = Field(default=3)  # 1-5 scale (1=highest security)
    vlan_range: Optional[str] = Field(max_length=50, default=None)  # e.g., "100-199"
    subnet_range: Optional[str] = Field(max_length=100, default=None)  # e.g., "10.0.0.0/16"
    firewall_policy: Optional[str] = Field(max_length=100, default=None)
    access_requirements: Optional[str] = Field(default=None)  # Description of access requirements
    is_dmz: bool = Field(default=False)
    is_isolated: bool = Field(default=False)
    parent_zone_id: Optional[int] = Field(foreign_key="networkzone.zone_id", default=None)