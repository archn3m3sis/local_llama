import reflex as rx
from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import Session, select
from ..models.log_collection import LogCollection
from ..models.log_type import LogType
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.app_user import AppUser
from ..models.department import Department


class LogCollectionState(rx.State):
    """State management for log collection form."""
    
    # Form fields
    selected_employee_id: Optional[int] = None
    selected_asset_id: Optional[int] = None
    selected_project_id: Optional[int] = None
    selected_logtype_id: Optional[int] = None
    selected_common_logtype: str = ""
    collection_result: str = ""
    collection_comments: str = ""
    collection_date: str = datetime.now().strftime("%Y-%m-%dT%H:%M")
    
    # Dropdown options
    employees: List[str] = []
    assets: List[str] = []
    projects: List[str] = []
    logtypes: List[str] = []
    extended_logtypes: List[str] = []
    
    # Lookup mappings
    employee_map: Dict[str, int] = {}
    asset_map: Dict[str, int] = {}
    project_map: Dict[str, int] = {}
    logtype_map: Dict[str, int] = {}
    extended_logtype_map: Dict[str, int] = {}
    
    # UI state
    is_submitting: bool = False
    submission_message: str = ""
    submission_status: str = ""  # success, error, ""
    
    # Filtered assets based on selected project
    filtered_assets: List[str] = []
    filtered_asset_map: Dict[str, int] = {}
    
    # Search/filter states
    employee_search: str = ""
    asset_search: str = ""
    logtype_search: str = ""
    
    # Reset trigger
    form_key: int = 0
    
    def load_form_data(self):
        """Load all necessary data for form dropdowns."""
        with rx.session() as session:
            # Load employees from Cybersecurity department only
            # First get the Cybersecurity department
            cybersec_dept = session.exec(
                select(Department).where(Department.dept_name == "Cybersecurity")
            ).first()
            
            if cybersec_dept:
                # Load only employees from Cybersecurity department
                employees = session.exec(
                    select(Employee)
                    .where(Employee.department_id == cybersec_dept.dept_id)
                    .order_by(Employee.last_name)
                ).all()
            else:
                # Fallback to empty list if department not found
                employees = []
                
            self.employees = []
            self.employee_map = {}
            for emp in employees:
                display_name = f"{emp.last_name}, {emp.first_name}"
                self.employees.append(display_name)
                self.employee_map[display_name] = emp.id
            
            # Load projects
            projects = session.exec(select(Project).order_by(Project.project_name)).all()
            self.projects = []
            self.project_map = {}
            for proj in projects:
                self.projects.append(proj.project_name)
                self.project_map[proj.project_name] = proj.project_id
            
            # Load all assets initially
            assets = session.exec(select(Asset).order_by(Asset.asset_name)).all()
            self.assets = []
            self.asset_map = {}
            for asset in assets:
                self.assets.append(asset.asset_name)
                self.asset_map[asset.asset_name] = asset.asset_id
            self.filtered_assets = self.assets.copy()
            self.filtered_asset_map = self.asset_map.copy()
            
            # Load log types and separate common from extended
            logtypes = session.exec(select(LogType).order_by(LogType.logtype)).all()
            
            # Common log types
            common_logs = [
                "Windows Event System Logs",
                "Windows Event Application Logs", 
                "Windows Event Security Logs"
            ]
            
            # Separate extended log types (all except common ones)
            self.extended_logtypes = []
            self.extended_logtype_map = {}
            self.logtype_map = {}
            
            for lt in logtypes:
                self.logtype_map[lt.logtype] = lt.logtype_id
                if lt.logtype not in common_logs:
                    self.extended_logtypes.append(lt.logtype)
                    self.extended_logtype_map[lt.logtype] = lt.logtype_id
    
    def filter_assets_by_project(self):
        """Filter assets based on selected project."""
        if self.selected_project_id:
            # Filter assets by project ID by re-querying the database
            with rx.session() as session:
                assets = session.exec(
                    select(Asset)
                    .where(Asset.project_id == self.selected_project_id)
                    .order_by(Asset.asset_name)
                ).all()
                self.filtered_assets = []
                self.filtered_asset_map = {}
                for asset in assets:
                    self.filtered_assets.append(asset.asset_name)
                    self.filtered_asset_map[asset.asset_name] = asset.asset_id
        else:
            self.filtered_assets = self.assets.copy()
            self.filtered_asset_map = self.asset_map.copy()
    
    def set_employee(self, value: str):
        """Set selected employee."""
        self.selected_employee_id = self.employee_map.get(value) if value else None
    
    def set_asset(self, value: str):
        """Set selected asset."""
        self.selected_asset_id = self.filtered_asset_map.get(value) if value else None
    
    def set_project(self, value: str):
        """Set selected project and filter assets."""
        self.selected_project_id = self.project_map.get(value) if value else None
        self.selected_asset_id = None  # Reset asset selection
        self.filter_assets_by_project()
    
    def set_logtype(self, value: str):
        """Set selected extended log type."""
        self.selected_logtype_id = self.extended_logtype_map.get(value) if value else None
    
    def set_common_logtype(self, value: str):
        """Set selected common log type."""
        self.selected_common_logtype = value
        # Clear extended logtype when common is selected
        if value:
            self.selected_logtype_id = None
    
    def set_result(self, value: str):
        """Set collection result."""
        self.collection_result = value
    
    def set_comments(self, value: str):
        """Set collection comments."""
        self.collection_comments = value
    
    def set_date(self, value: str):
        """Set collection date."""
        self.collection_date = value
    
    def set_employee_search(self, value: str):
        """Set employee search value."""
        self.employee_search = value
    
    def set_asset_search(self, value: str):
        """Set asset search value."""
        self.asset_search = value
    
    def set_logtype_search(self, value: str):
        """Set logtype search value."""
        self.logtype_search = value
    
    
    @rx.var
    def form_is_valid(self) -> bool:
        """Check if form has all required fields."""
        # Common logtype is required, extended logtype is optional
        return all([
            self.selected_employee_id,
            self.selected_asset_id,
            self.selected_project_id,
            self.selected_common_logtype,  # Required
            self.collection_result,
            self.collection_date
        ])
        # Note: self.selected_logtype_id (extended log type) is not required
    
    async def submit_log_collection(self):
        """Submit the log collection to database."""
        if not self.form_is_valid:
            self.submission_status = "error"
            self.submission_message = "Please fill in all required fields."
            return
        
        self.is_submitting = True
        
        try:
            with rx.session() as session:
                # Parse the datetime string
                collection_datetime = datetime.strptime(
                    self.collection_date, 
                    "%Y-%m-%dT%H:%M"
                )
                
                records_created = 0
                
                # Handle "All Common Logtypes" special case
                if self.selected_common_logtype == "All Common Logtypes":
                    common_logs = [
                        "Windows Event System Logs",
                        "Windows Event Application Logs", 
                        "Windows Event Security Logs"
                    ]
                    
                    # Create 3 separate entries for common logs
                    for log_name in common_logs:
                        logtype_id = self.logtype_map.get(log_name)
                        if logtype_id:
                            new_collection = LogCollection(
                                logcollection_date=collection_datetime,
                                employee_id=self.selected_employee_id,
                                asset_id=self.selected_asset_id,
                                project_id=self.selected_project_id,
                                logtype_id=logtype_id,
                                logcollection_result=self.collection_result,
                                logcollection_comments=self.collection_comments if self.collection_comments else None
                            )
                            session.add(new_collection)
                            records_created += 1
                
                # Handle single common logtype selection
                elif self.selected_common_logtype and self.selected_common_logtype != "All Common Logtypes":
                    logtype_id = self.logtype_map.get(self.selected_common_logtype)
                    if logtype_id:
                        new_collection = LogCollection(
                            logcollection_date=collection_datetime,
                            employee_id=self.selected_employee_id,
                            asset_id=self.selected_asset_id,
                            project_id=self.selected_project_id,
                            logtype_id=logtype_id,
                            logcollection_result=self.collection_result,
                            logcollection_comments=self.collection_comments if self.collection_comments else None
                        )
                        session.add(new_collection)
                        records_created += 1
                
                # Handle extended logtype selection (if provided in addition to common)
                if self.selected_logtype_id:
                    new_collection = LogCollection(
                        logcollection_date=collection_datetime,
                        employee_id=self.selected_employee_id,
                        asset_id=self.selected_asset_id,
                        project_id=self.selected_project_id,
                        logtype_id=self.selected_logtype_id,
                        logcollection_result=self.collection_result,
                        logcollection_comments=self.collection_comments if self.collection_comments else None
                    )
                    session.add(new_collection)
                    records_created += 1
                
                # Commit all records
                if records_created > 0:
                    session.commit()
                    self.submission_status = "success"
                    if records_created == 1:
                        self.submission_message = "Log collection recorded successfully!"
                    else:
                        self.submission_message = f"{records_created} log collection records created successfully!"
                
                    # Auto-fade handled by JavaScript in the component
                
                # Reset form
                self.reset_form()
                
                # Refresh the table to show new records
                from .log_collection_table_state import LogCollectionTableState
                table_state = await self.get_state(LogCollectionTableState)
                table_state.load_collections()
                
        except Exception as e:
            self.submission_status = "error"
            self.submission_message = f"Error submitting log collection: {str(e)}"
        finally:
            self.is_submitting = False
    
    def reset_form(self):
        """Reset form to initial state."""
        self.selected_employee_id = None
        self.selected_asset_id = None
        self.selected_project_id = None
        self.selected_logtype_id = None
        self.selected_common_logtype = ""
        self.collection_result = ""
        self.collection_comments = ""
        self.collection_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
        self.employee_search = ""
        self.asset_search = ""
        self.logtype_search = ""
        self.filter_assets_by_project()
        # Increment form key to force re-render
        self.form_key += 1
    
    def clear_message(self):
        """Clear submission message."""
        self.submission_message = ""
        self.submission_status = ""
    
