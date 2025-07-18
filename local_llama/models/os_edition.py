from typing import Optional
from sqlmodel import SQLModel, Field


class OSEdition(SQLModel, table=True):
    osedition_id: Optional[int] = Field(default=None, primary_key=True)
    osedition_name: str = Field(max_length=100)