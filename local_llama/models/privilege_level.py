from sqlmodel import Field, SQLModel
from typing import Optional


class PrivilegeLevel(SQLModel, table=True):
    priv_id: Optional[int] = Field(default=None, primary_key=True)
    priv_name: str = Field(max_length=100)
    priv_description: str = Field(max_length=255)