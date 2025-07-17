from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime


class AVVersion(SQLModel, table=True):
    __tablename__ = "avversion"
    
    avversion_id: Optional[int] = Field(default=None, primary_key=True)
    av_version: str = Field(max_length=50)
    av_description: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    
    # Relationship to DatVersion
    dat_versions: List["DatVersion"] = Relationship(back_populates="av_version")