from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class SysArchitecture(SQLModel, table=True):
    sysarchitecture_id: Optional[int] = Field(default=None, primary_key=True)
    sys_architecture: str = Field(max_length=100)
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)