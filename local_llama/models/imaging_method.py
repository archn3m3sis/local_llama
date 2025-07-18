from typing import Optional
from sqlmodel import SQLModel, Field


class ImagingMethod(SQLModel, table=True):
    imgmethod_id: Optional[int] = Field(default=None, primary_key=True)
    img_method: str = Field(max_length=100)