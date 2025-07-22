from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ConfigurationBaseline(SQLModel, table=True):
    """Define standard configuration baselines for different asset types."""
    
    baseline_id: Optional[int] = Field(default=None, primary_key=True)
    baseline_name: str = Field(max_length=100)
    baseline_version: str = Field(max_length=20, default="1.0")
    systype_id: int = Field(foreign_key="systype.systype_id")
    description: Optional[str] = Field(default=None)
    config_template: str = Field()  # JSON configuration template
    created_date: datetime = Field(default_factory=datetime.now)
    created_by: int = Field(foreign_key="employee.id")
    approved_date: Optional[datetime] = Field(default=None)
    approved_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    effective_date: Optional[datetime] = Field(default=None)
    expiration_date: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)
    is_mandatory: bool = Field(default=False)
    compliance_level: str = Field(max_length=20, default="recommended")  # 'mandatory', 'recommended', 'optional'
    parent_baseline_id: Optional[int] = Field(foreign_key="configurationbaseline.baseline_id", default=None)