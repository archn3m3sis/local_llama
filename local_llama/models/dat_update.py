from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class DatUpdate(SQLModel, table=True):
    datupdate_id: Optional[int] = Field(default=None, primary_key=True)
    date_of_update: datetime = Field(default_factory=datetime.now)
    employee_id: int = Field(foreign_key="employee.id")
    datversion_id: int = Field(foreign_key="datversion.datversion_id")
    asset_id: int = Field(foreign_key="asset.asset_id")
    project_id: int = Field(foreign_key="project.project_id")
    datfile_name: str = Field(max_length=255)
    update_result: str = Field(max_length=255)
    update_comments: Optional[str] = Field(max_length=500, default=None)