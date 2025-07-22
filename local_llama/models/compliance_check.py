from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ComplianceCheck(SQLModel, table=True):
    """Track compliance status and audit results for assets."""
    
    check_id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.asset_id")
    check_date: datetime = Field(default_factory=datetime.now)
    compliance_standard: str = Field(max_length=100)  # 'STIG', 'CIS', 'NIST', 'Custom'
    standard_version: Optional[str] = Field(max_length=50, default=None)
    scan_type: str = Field(max_length=50, default="automated")  # 'automated', 'manual', 'hybrid'
    total_checks: int = Field(default=0)
    passed_checks: int = Field(default=0)
    failed_checks: int = Field(default=0)
    warning_checks: int = Field(default=0)
    not_applicable: int = Field(default=0)
    compliance_score: float = Field(default=0.0)  # Percentage (0-100)
    severity_high: int = Field(default=0)  # Count of high severity failures
    severity_medium: int = Field(default=0)  # Count of medium severity failures
    severity_low: int = Field(default=0)  # Count of low severity failures
    report_data: Optional[str] = Field(default=None)  # JSON detailed results
    report_file_path: Optional[str] = Field(max_length=500, default=None)
    performed_by: int = Field(foreign_key="employee.id")
    approved_by: Optional[int] = Field(foreign_key="employee.id", default=None)
    approval_date: Optional[datetime] = Field(default=None)
    next_check_date: Optional[datetime] = Field(default=None)
    remediation_required: bool = Field(default=False)
    remediation_ticket_id: Optional[int] = Field(foreign_key="temticket.ticket_id", default=None)