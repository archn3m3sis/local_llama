from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ImageCollection(SQLModel, table=True):
    imgcollection_id: Optional[int] = Field(default=None, primary_key=True)
    imgcollection_date: datetime = Field(default_factory=datetime.now)
    employee_id: int = Field(foreign_key="employee.id")
    asset_id: int = Field(foreign_key="asset.asset_id")
    project_id: int = Field(foreign_key="project.project_id")
    img_size_mb: Optional[float] = Field(default=None)
    imgmethod_id: int = Field(foreign_key="imagingmethod.imgmethod_id")
    imaging_result: str = Field(max_length=255)
    imaging_comments: Optional[str] = Field(max_length=500, default=None)