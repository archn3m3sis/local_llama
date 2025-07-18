from typing import Optional
from sqlmodel import SQLModel, Field


class GPUType(SQLModel, table=True):
    gpu_id: Optional[int] = Field(default=None, primary_key=True)
    gpu_name: str = Field(max_length=100)