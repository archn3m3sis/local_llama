from typing import Optional
from sqlmodel import SQLModel, Field


class LogType(SQLModel, table=True):
    logtype_id: Optional[int] = Field(default=None, primary_key=True)
    logtype: str = Field(max_length=100)