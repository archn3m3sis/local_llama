from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class PatchHistory(SQLModel, table=True):
    """Track patches and updates applied to assets."""
    
    patch_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    patch_name: str = Field(max_length=200)
    patch_kb: Optional[str] = Field(max_length=50, default=None)  # KB number for Windows
    patch_category: Optional[str] = Field(max_length=50, default=None)  # 'Security', 'Critical', 'Feature'
    patch_severity: Optional[str] = Field(max_length=20, default=None)  # 'Critical', 'Important', 'Moderate', 'Low'
    install_date: datetime = Field(default_factory=datetime.now)
    install_status: str = Field(max_length=20)  # 'Success', 'Failed', 'Pending', 'Rolled Back'
    install_method: Optional[str] = Field(max_length=50, default=None)  # 'Manual', 'WSUS', 'SCCM', 'Script'
    installed_by: int = Field(foreign_key="employee.id")
    reboot_required: bool = Field(default=False)
    reboot_completed: Optional[datetime] = Field(default=None)
    rollback_date: Optional[datetime] = Field(default=None)
    rollback_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    rollback_reason: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)