from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class SoftwareVersion(SQLModel, table=True):
    """Track different versions of software in the catalog."""
    
    version_id: Optional[int] = Field(default=None, primary_key=True)
    software_catalog_id: int = Field(foreign_key="softwarecatalog.software_catalog_id")
    version_number: str = Field(max_length=50)
    release_date: Optional[datetime] = Field(default=None)
    end_support_date: Optional[datetime] = Field(default=None)
    is_current: bool = Field(default=False)  # Is this the current/latest version
    is_supported: bool = Field(default=True)  # Is this version still supported
    is_vulnerable: bool = Field(default=False)  # Known vulnerabilities
    vulnerability_cves: Optional[str] = Field(default=None)  # CSV list of CVEs
    min_os_version: Optional[str] = Field(max_length=50, default=None)
    max_os_version: Optional[str] = Field(max_length=50, default=None)
    release_notes: Optional[str] = Field(default=None)
    download_url: Optional[str] = Field(max_length=500, default=None)
    checksum: Optional[str] = Field(max_length=128, default=None)  # SHA hash
    file_size_mb: Optional[int] = Field(default=None)