from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Project(SQLModel, table=True):
    project_id: Optional[int] = Field(default=None, primary_key=True)
    project_name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)