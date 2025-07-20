from typing import Optional
from sqlmodel import SQLModel, Field


class VirtualizationSource(SQLModel, table=True):
    virtsource_id: Optional[int] = Field(default=None, primary_key=True)
    virt_source: str = Field(max_length=100)