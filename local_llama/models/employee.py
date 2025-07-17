from sqlmodel import Field, SQLModel
from typing import Optional


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, max_length=100)
    department: str = Field(max_length=50)