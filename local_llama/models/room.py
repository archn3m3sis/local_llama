from typing import Optional
from sqlmodel import SQLModel, Field


class Room(SQLModel, table=True):
    room_id: Optional[int] = Field(default=None, primary_key=True)
    room_name: str = Field(max_length=200)
    floor_id: int = Field(foreign_key="floor.floor_id")
    building_id: int = Field(foreign_key="building.building_id")