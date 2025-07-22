from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class CIRelationship(SQLModel, table=True):
    """Track relationships between configuration items."""
    
    relationship_id: Optional[int] = Field(default=None, primary_key=True)
    parent_ci_id: int = Field(foreign_key="configurationitem.ci_id")
    child_ci_id: int = Field(foreign_key="configurationitem.ci_id")
    relationship_type: str = Field(max_length=50)  # 'depends_on', 'contains', 'connects_to', 'runs_on'
    relationship_status: str = Field(max_length=20, default="active")  # 'active', 'inactive', 'planned'
    description: Optional[str] = Field(default=None)
    created_date: datetime = Field(default_factory=datetime.now)
    created_by: int = Field(foreign_key="employee.id")
    validated_date: Optional[datetime] = Field(default=None)
    validated_by: Optional[int] = Field(foreign_key="employee.id", default=None)