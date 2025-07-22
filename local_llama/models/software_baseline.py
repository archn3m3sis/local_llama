from typing import Optional
from sqlmodel import SQLModel, Field


class SoftwareBaseline(SQLModel, table=True):
    """Define required software baselines for different system types."""
    
    baseline_id: Optional[int] = Field(default=None, primary_key=True)
    systype_id: int = Field(foreign_key="systype.systype_id")
    sw_name: str = Field(max_length=200)
    required_version: Optional[str] = Field(max_length=50, default=None)
    min_version: Optional[str] = Field(max_length=50, default=None)  # Minimum acceptable version
    max_version: Optional[str] = Field(max_length=50, default=None)  # Maximum acceptable version
    is_mandatory: bool = Field(default=True)
    compliance_category: Optional[str] = Field(max_length=50, default=None)  # 'security', 'productivity', 'monitoring'
    description: Optional[str] = Field(default=None)