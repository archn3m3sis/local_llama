from typing import Optional
from sqlmodel import SQLModel, Field


class Building(SQLModel, table=True):
    building_id: Optional[int] = Field(default=None, primary_key=True)
    building_name: str = Field(max_length=100)