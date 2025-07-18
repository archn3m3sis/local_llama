from typing import Optional
from sqlmodel import SQLModel, Field


class OSVersion(SQLModel, table=True):
    osversion_id: Optional[int] = Field(default=None, primary_key=True)
    os_id: int = Field(foreign_key="operatingsystem.os_id")
    osedition_id: int = Field(foreign_key="osedition.osedition_id")
    osversion_name: str = Field(max_length=100)