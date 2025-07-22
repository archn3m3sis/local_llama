from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ServiceDependency(SQLModel, table=True):
    """Track relationships and dependencies between assets."""
    
    dependency_id: Optional[int] = Field(default=None, primary_key=True)
    parent_asset_id: int = Field(foreign_key="asset.asset_id")
    child_asset_id: int = Field(foreign_key="asset.asset_id")
    dependency_type: str = Field(max_length=50)  # 'application', 'database', 'service', 'network', 'storage'
    dependency_direction: str = Field(max_length=20, default="downstream")  # 'upstream', 'downstream', 'bidirectional'
    criticality: int = Field(default=3)  # 1-5 scale (1=most critical)
    description: Optional[str] = Field(default=None)
    port_number: Optional[int] = Field(default=None)  # Network port if applicable
    protocol: Optional[str] = Field(max_length=20, default=None)  # 'TCP', 'UDP', 'HTTP', 'HTTPS'
    discovered_date: datetime = Field(default_factory=datetime.now)
    discovered_method: Optional[str] = Field(max_length=50, default=None)  # 'manual', 'auto-discovery', 'import'
    validated_date: Optional[datetime] = Field(default=None)
    validated_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    is_active: bool = Field(default=True)
    impact_description: Optional[str] = Field(default=None)  # What happens if parent fails