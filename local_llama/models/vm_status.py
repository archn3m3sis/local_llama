from typing import Optional
from sqlmodel import SQLModel, Field


class VMStatus(SQLModel, table=True):
    vmstatus_id: Optional[int] = Field(default=None, primary_key=True)
    vm_status: str = Field(max_length=150)