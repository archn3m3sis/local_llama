from typing import Optional
from sqlmodel import SQLModel, Field


class SysType(SQLModel, table=True):
    systype_id: Optional[int] = Field(default=None, primary_key=True)
    systype_name: str = Field(max_length=100)