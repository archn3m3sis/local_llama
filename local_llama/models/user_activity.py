from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class UserActivity(SQLModel, table=True):
    activity_id: Optional[int] = Field(default=None, primary_key=True)
    
    # User information
    user_id: int = Field(foreign_key="appuser.id")
    employee_id: Optional[int] = Field(foreign_key="employee.id")
    
    # Activity details
    activity_type: str = Field(max_length=50)  # e.g., "vm_created", "image_captured", "log_added", "av_updated"
    activity_description: str = Field(max_length=500)
    
    # Related entity IDs (optional, depending on activity type)
    related_asset_id: Optional[int] = Field(foreign_key="asset.asset_id", default=None)
    related_project_id: Optional[int] = Field(foreign_key="project.project_id", default=None)
    related_vm_id: Optional[int] = Field(foreign_key="virtualmachine.virtmachine_id", default=None)
    related_image_id: Optional[int] = Field(foreign_key="imagecollection.imgcollection_id", default=None)
    related_log_id: Optional[int] = Field(foreign_key="logcollection.logcollection_id", default=None)
    related_dat_id: Optional[int] = Field(foreign_key="datupdate.datupdate_id", default=None)
    
    # Metadata
    activity_timestamp: datetime = Field(default_factory=datetime.now)
    ip_address: Optional[str] = Field(max_length=45, default=None)  # Support IPv6
    user_agent: Optional[str] = Field(max_length=500, default=None)
    
    # Additional context (JSON-like data stored as string)
    activity_metadata: Optional[str] = Field(default=None)  # Can store JSON for extra details