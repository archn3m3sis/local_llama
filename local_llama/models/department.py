from sqlmodel import Field, SQLModel
from typing import Optional


class Department(SQLModel, table=True):
    dept_id: Optional[int] = Field(default=None, primary_key=True)
    dept_name: str = Field(max_length=100)
    dept_description: str = Field(max_length=255)