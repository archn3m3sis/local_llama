from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class TEMTicket(SQLModel, table=True):
    temticket_id: Optional[int] = Field(default=None, primary_key=True)
    submission_date: datetime = Field(default_factory=datetime.now)
    global_ticket_id: str = Field(max_length=100)
    asset_id: int = Field(foreign_key="asset.asset_id")
    project_id: int = Field(foreign_key="project.project_id")
    submission_emp: int = Field(foreign_key="employee.id")
    submission_description: str = Field(max_length=1000)
    response_date: Optional[datetime] = Field(default=None)
    response_emp: Optional[int] = Field(foreign_key="employee.id", default=None)
    response_reference_link: Optional[str] = Field(max_length=500, default=None)
    response_result: Optional[str] = Field(max_length=50, default=None)  # success, fail, or undetermined
    response_comments: Optional[str] = Field(max_length=1000, default=None)
    status: str = Field(max_length=20, default="open")  # open, closed, or cancelled
    resolution_date: Optional[datetime] = Field(default=None)
    time_to_respond: Optional[int] = Field(default=None)  # time in minutes/hours between submission_date and response_date
    time_to_resolve: Optional[int] = Field(default=None)  # time in minutes/hours between submission_date and resolution_date