from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime


class DatVersion(SQLModel, table=True):
    __tablename__ = "datversion"
    
    datversion_id: Optional[int] = Field(default=None, primary_key=True)
    datversion_name: str = Field(max_length=100)
    avversion_id: int = Field(foreign_key="avversion.avversion_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationship to AVVersion
    av_version: Optional["AVVersion"] = Relationship(back_populates="dat_versions")