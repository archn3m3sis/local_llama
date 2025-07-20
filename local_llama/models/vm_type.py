from typing import Optional
from sqlmodel import SQLModel, Field


class VMType(SQLModel, table=True):
    vmtype_id: Optional[int] = Field(default=None, primary_key=True)
    vm_type: str = Field(max_length=100)