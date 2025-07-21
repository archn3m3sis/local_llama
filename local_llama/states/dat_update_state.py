import reflex as rx
from typing import List, Dict, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.dat_update import DatUpdate
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.dat_version import DatVersion
from ..models.av_version import AVVersion
from ..models.department import Department
from ..services.activity_tracker import ActivityTracker


class DatUpdateState(rx.State):
    """State management for DAT update form and submission."""
    
    # Form fields
    selected_employee_id: str = ""
    selected_asset_id: str = ""
    selected_project_id: str = ""
    selected_datversion_id: str = ""
    datfile_name: str = ""
    update_result: str = ""
    update_comments: str = ""
    update_date: str = ""
    
    # Form validation and submission
    is_submitting: bool = False
    form_key: int = 0
    submission_message: str = ""
    submission_status: str = ""  # success, error, ""
    
    # Dropdown data
    employees: List[str] = []
    assets: List[str] = []
    projects: List[str] = []
    dat_versions: List[str] = []
    
    # Hidden mappings for value lookups
    employee_map: Dict[str, str] = {}
    asset_map: Dict[str, str] = {}
    project_map: Dict[str, str] = {}
    datversion_map: Dict[str, str] = {}
    
    # Result options
    result_options: List[str] = [
        "Success",
        "Failed",
        "Partial Success",
        "In Progress",
        "Cancelled"
    ]
    
    @rx.var
    def form_is_valid(self) -> bool:
        """Check if the form has all required fields filled."""
        return (
            bool(self.selected_employee_id) and
            bool(self.selected_asset_id) and
            bool(self.selected_project_id) and
            bool(self.selected_datversion_id) and
            bool(self.datfile_name.strip()) and
            bool(self.update_result) and
            bool(self.update_date)
        )
    
    def load_form_data(self):
        """Load dropdown data for the form."""
        try:
            with rx.session() as session:
                # Load employees from Cybersecurity department only
                cybersec_dept = session.exec(
                    select(Department).where(Department.dept_name == "Cybersecurity")
                ).first()
                
                if cybersec_dept:
                    employees = session.exec(
                        select(Employee)
                        .where(Employee.department_id == cybersec_dept.dept_id)
                        .order_by(Employee.last_name)
                    ).all()
                    
                    self.employees = [f"{emp.last_name}, {emp.first_name}" for emp in employees]
                    self.employee_map = {f"{emp.last_name}, {emp.first_name}": str(emp.id) for emp in employees}
                
                # Load projects
                projects = session.exec(select(Project).order_by(Project.project_name)).all()
                self.projects = [proj.project_name for proj in projects]
                self.project_map = {proj.project_name: str(proj.project_id) for proj in projects}
                
                # Load DAT versions with AV version info
                dat_versions = session.exec(
                    select(DatVersion, AVVersion)
                    .join(AVVersion, DatVersion.avversion_id == AVVersion.avversion_id)
                    .where(DatVersion.is_active == True)
                    .order_by(DatVersion.datversion_name)
                ).all()
                
                self.dat_versions = [f"{dat.datversion_name} (AV: {av.av_version})" for dat, av in dat_versions]
                self.datversion_map = {f"{dat.datversion_name} (AV: {av.av_version})": str(dat.datversion_id) for dat, av in dat_versions}
                
        except Exception as e:
            print(f"Error loading form data: {str(e)}")
    
    def load_assets_for_project(self):
        """Load assets filtered by selected project."""
        if not self.selected_project_id:
            self.assets = []
            self.asset_map = {}
            return
            
        try:
            # Get project_id from the mapping
            project_id = self.project_map.get(self.selected_project_id)
            if not project_id:
                return
                
            with rx.session() as session:
                assets = session.exec(
                    select(Asset)
                    .where(Asset.project_id == int(project_id))
                    .order_by(Asset.asset_name)
                ).all()
                
                self.assets = [asset.asset_name for asset in assets]
                self.asset_map = {asset.asset_name: str(asset.asset_id) for asset in assets}
                
                # Clear asset selection if it's no longer valid
                if self.selected_asset_id and self.selected_asset_id not in self.assets:
                    self.selected_asset_id = ""
                        
        except Exception as e:
            print(f"Error loading assets: {str(e)}")
            self.assets = []
            self.asset_map = {}
    
    def set_selected_project_id(self, project_id: str):
        """Handle project selection change."""
        self.selected_project_id = project_id
        self.selected_asset_id = ""  # Reset asset selection
        self.load_assets_for_project()
    
    async def submit_dat_update(self):
        """Submit the DAT update to the database."""
        if not self.form_is_valid:
            self.submission_status = "error"
            self.submission_message = "Please fill in all required fields."
            return
            
        self.is_submitting = True
        
        try:
            with rx.session() as session:
                # Get IDs from mappings
                employee_id = self.employee_map.get(self.selected_employee_id)
                asset_id = self.asset_map.get(self.selected_asset_id)
                project_id = self.project_map.get(self.selected_project_id)
                datversion_id = self.datversion_map.get(self.selected_datversion_id)
                
                if not all([employee_id, asset_id, project_id, datversion_id]):
                    print("Missing required IDs for submission")
                    self.is_submitting = False
                    return
                
                # Parse the update date
                update_datetime = datetime.fromisoformat(self.update_date) if self.update_date else datetime.now()
                
                # Create new DAT update record
                new_update = DatUpdate(
                    date_of_update=update_datetime,
                    employee_id=int(employee_id),
                    asset_id=int(asset_id),
                    project_id=int(project_id),
                    datversion_id=int(datversion_id),
                    datfile_name=self.datfile_name.strip(),
                    update_result=self.update_result,
                    update_comments=self.update_comments.strip() if self.update_comments.strip() else None
                )
                
                session.add(new_update)
                session.commit()
                
                print(f"Successfully submitted DAT update: {new_update.datupdate_id}")
                
                # Track activity
                dat_version_name = self.selected_datversion_id
                ActivityTracker.track_dat_update(
                    dat_id=new_update.datupdate_id,
                    asset_id=asset_id,
                    project_id=project_id,
                    employee_id=employee_id,
                    dat_version=dat_version_name
                )
                
                # Set success message
                self.submission_status = "success"
                self.submission_message = "DAT update recorded successfully!"
                
                # Refresh the table to show the new entry
                from .dat_update_table_state import DatUpdateTableState
                table_state = await self.get_state(DatUpdateTableState)
                table_state.load_updates()
                
                # Reset form
                self.reset_form()
                
                # Auto-fade handled by JavaScript in the component
                
        except Exception as e:
            print(f"Error submitting DAT update: {str(e)}")
            self.submission_status = "error"
            self.submission_message = f"Error submitting DAT update: {str(e)}"
        finally:
            self.is_submitting = False
    
    def reset_form(self):
        """Reset the form to initial state."""
        self.selected_employee_id = ""
        self.selected_asset_id = ""
        self.selected_project_id = ""
        self.selected_datversion_id = ""
        self.datfile_name = ""
        self.update_result = ""
        self.update_comments = ""
        self.update_date = ""
        self.assets = []
        self.form_key += 1  # Force form re-render
    
    def clear_message(self):
        """Clear submission message."""
        self.submission_message = ""
        self.submission_status = ""