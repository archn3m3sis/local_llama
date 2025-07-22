from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class AssetConfiguration(SQLModel, table=True):
    """Point-in-time configuration snapshots for assets."""
    
    config_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    snapshot_date: datetime = Field(default_factory=datetime.now)
    config_data: str = Field()  # JSON configuration data
    config_hash: str = Field(max_length=64)  # SHA-256 hash for change detection
    created_by: int = Field(foreign_key="employee.id")
    is_baseline: bool = Field(default=False)  # Mark as baseline configuration
    baseline_name: Optional[str] = Field(max_length=100, default=None)
    notes: Optional[str] = Field(default=None)