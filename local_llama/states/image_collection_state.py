import reflex as rx
from typing import List, Dict, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.image_collection import ImageCollection
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.imaging_method import ImagingMethod
from ..models.department import Department


class ImageCollectionState(rx.State):
    """State management for image collection form and submission."""
    
    # Form fields
    selected_employee_id: str = ""
    selected_asset_id: str = ""
    selected_project_id: str = ""
    selected_imaging_method_id: str = ""
    image_size_mb: str = ""
    imaging_result: str = ""
    imaging_comments: str = ""
    collection_date: str = ""
    
    # Form validation and submission
    is_submitting: bool = False
    form_key: int = 0
    submission_message: str = ""
    submission_status: str = ""  # success, error, ""
    
    # Dropdown data
    employees: List[str] = []
    assets: List[str] = []
    projects: List[str] = []
    imaging_methods: List[str] = []
    
    # Hidden mappings for value lookups
    employee_map: Dict[str, str] = {}
    asset_map: Dict[str, str] = {}
    project_map: Dict[str, str] = {}
    imaging_method_map: Dict[str, str] = {}
    
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
            bool(self.selected_imaging_method_id) and
            bool(self.imaging_result) and
            bool(self.collection_date)
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
                
                # Load imaging methods
                methods = session.exec(select(ImagingMethod).order_by(ImagingMethod.img_method)).all()
                self.imaging_methods = [method.img_method for method in methods]
                self.imaging_method_map = {method.img_method: str(method.imgmethod_id) for method in methods}
                
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
    
    async def submit_image_collection(self):
        """Submit the image collection to the database."""
        if not self.form_is_valid:
            self.submission_status = "error"
            self.submission_message = "Please fill in all required fields."
            return
            
        self.is_submitting = True
        
        try:
            with rx.session() as session:
                # Convert image size to float if provided
                size_mb = None
                if self.image_size_mb.strip():
                    try:
                        size_mb = float(self.image_size_mb.strip())
                    except ValueError:
                        print("Invalid image size format")
                        self.is_submitting = False
                        return
                
                # Get IDs from mappings
                employee_id = self.employee_map.get(self.selected_employee_id)
                asset_id = self.asset_map.get(self.selected_asset_id)
                project_id = self.project_map.get(self.selected_project_id)
                imaging_method_id = self.imaging_method_map.get(self.selected_imaging_method_id)
                
                if not all([employee_id, asset_id, project_id, imaging_method_id]):
                    print("Missing required IDs for submission")
                    self.is_submitting = False
                    return
                
                # Parse the collection date
                collection_datetime = datetime.fromisoformat(self.collection_date) if self.collection_date else datetime.now()
                
                # Create new image collection record
                new_collection = ImageCollection(
                    imgcollection_date=collection_datetime,
                    employee_id=int(employee_id),
                    asset_id=int(asset_id),
                    project_id=int(project_id),
                    imgmethod_id=int(imaging_method_id),
                    img_size_mb=size_mb,
                    imaging_result=self.imaging_result,
                    imaging_comments=self.imaging_comments.strip() if self.imaging_comments.strip() else None
                )
                
                session.add(new_collection)
                session.commit()
                
                print(f"Successfully submitted image collection: {new_collection.imgcollection_id}")
                
                # Set success message
                self.submission_status = "success"
                self.submission_message = "Image collection recorded successfully!"
                
                # Refresh the table to show the new entry
                from .image_collection_table_state import ImageCollectionTableState
                table_state = await self.get_state(ImageCollectionTableState)
                table_state.load_collections()
                
                # Reset form
                self.reset_form()
                
                # Auto-fade handled by JavaScript in the component
                
        except Exception as e:
            print(f"Error submitting image collection: {str(e)}")
            self.submission_status = "error"
            self.submission_message = f"Error submitting image collection: {str(e)}"
        finally:
            self.is_submitting = False
    
    def reset_form(self):
        """Reset the form to initial state."""
        self.selected_employee_id = ""
        self.selected_asset_id = ""
        self.selected_project_id = ""
        self.selected_imaging_method_id = ""
        self.image_size_mb = ""
        self.imaging_result = ""
        self.imaging_comments = ""
        self.collection_date = ""
        self.assets = []
        self.form_key += 1  # Force form re-render
    
    def clear_message(self):
        """Clear submission message."""
        self.submission_message = ""
        self.submission_status = ""
    
