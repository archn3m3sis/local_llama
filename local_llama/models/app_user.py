from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class AppUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, max_length=100)
    phone: Optional[str] = Field(max_length=20, default=None)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    department_id: int = Field(foreign_key="department.dept_id")
    priv_level_id: int = Field(foreign_key="privilegelevel.priv_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)