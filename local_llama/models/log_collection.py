from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class LogCollection(SQLModel, table=True):
    logcollection_id: Optional[int] = Field(default=None, primary_key=True)
    logcollection_date: datetime = Field(default_factory=datetime.now)
    employee_id: int = Field(foreign_key="employee.id")
    asset_id: int = Field(foreign_key="asset.asset_id")
    project_id: int = Field(foreign_key="project.project_id")
    logtype_id: int = Field(foreign_key="logtype.logtype_id")
    logcollection_result: str = Field(max_length=255)
    logcollection_comments: Optional[str] = Field(max_length=500, default=None)