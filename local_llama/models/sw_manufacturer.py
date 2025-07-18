from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class SWManufacturer(SQLModel, table=True):
    swmanu_id: Optional[int] = Field(default=None, primary_key=True)
    swmanu_name: str = Field(max_length=100)
    swmanu_contact: Optional[str] = Field(max_length=100, default=None)
    weblink: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)