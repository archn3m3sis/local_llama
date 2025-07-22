from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ConfigurationItem(SQLModel, table=True):
    """Track individual configuration items and their relationships."""
    
    ci_id: Optional[int] = Field(default=None, primary_key=True)
    ci_name: str = Field(max_length=200)
    ci_type: str = Field(max_length=50)  # 'hardware', 'software', 'network', 'service', 'document'
    ci_category: str = Field(max_length=50)  # 'server', 'application', 'database', 'storage', 'security'
    ci_status: str = Field(max_length=20, default="active")  # 'active', 'inactive', 'retired', 'planned'
    asset_id: Optional[int] = Field(foreign_key="asset.asset_id", default=None)
    serial_number: Optional[str] = Field(max_length=100, default=None)
    version: Optional[str] = Field(max_length=50, default=None)
    owner_id: int = Field(foreign_key="employee.id")
    custodian_id: Optional[int] = Field(foreign_key="employee.id", default=None)
    location: Optional[str] = Field(max_length=200, default=None)
    criticality: int = Field(default=3)  # 1-5 scale
    environment: Optional[str] = Field(max_length=20, default=None)  # 'production', 'staging', 'development', 'test'
    acquisition_date: Optional[datetime] = Field(default=None)
    warranty_expiry: Optional[datetime] = Field(default=None)
    last_audit_date: Optional[datetime] = Field(default=None)
    next_audit_date: Optional[datetime] = Field(default=None)
    configuration_data: Optional[str] = Field(default=None)  # JSON additional attributes
    created_date: datetime = Field(default_factory=datetime.now)
    modified_date: datetime = Field(default_factory=datetime.now)