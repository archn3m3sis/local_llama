from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class AppUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True, max_length=100)
    phone: Optional[str] = Field(max_length=20, default=None)
    department: str = Field(max_length=50)
    priv_level: str = Field(max_length=20)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)