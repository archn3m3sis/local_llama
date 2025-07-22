from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ConfigurationChange(SQLModel, table=True):
    """Track all configuration changes to assets with full audit trail."""
    
    change_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    change_date: datetime = Field(default_factory=datetime.now)
    employee_id: int = Field(foreign_key="employee.id")
    change_type: str = Field(max_length=50)  # 'hardware', 'software', 'network', 'system'
    field_name: str = Field(max_length=100)
    old_value: Optional[str] = Field(default=None)
    new_value: Optional[str] = Field(default=None)
    change_reason: Optional[str] = Field(default=None)
    ticket_id: Optional[int] = Field(foreign_key="temticket.ticket_id", default=None)
    approved_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    approval_date: Optional[datetime] = Field(default=None)