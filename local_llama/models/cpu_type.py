from typing import Optional
from sqlmodel import SQLModel, Field


class CPUType(SQLModel, table=True):
    cpu_id: Optional[int] = Field(default=None, primary_key=True)
    cpu_name: str = Field(max_length=100)