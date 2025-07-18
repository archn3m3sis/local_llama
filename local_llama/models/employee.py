from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, max_length=100)
    department_id: Optional[int] = Field(default=None, foreign_key="department.dept_id")
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    is_active: bool = Field(default=True)