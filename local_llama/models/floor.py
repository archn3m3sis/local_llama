from typing import Optional
from sqlmodel import SQLModel, Field


class Floor(SQLModel, table=True):
    floor_id: Optional[int] = Field(default=None, primary_key=True)
    floor_name: str = Field(max_length=100)