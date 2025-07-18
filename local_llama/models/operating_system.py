from typing import Optional
from sqlmodel import SQLModel, Field


class OperatingSystem(SQLModel, table=True):
    os_id: Optional[int] = Field(default=None, primary_key=True)
    os_name: str = Field(max_length=100)