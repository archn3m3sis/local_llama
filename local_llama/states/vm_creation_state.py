"""State management for Virtual Machine Creation."""
import reflex as rx
from datetime import datetime
from sqlmodel import select, Session
from ..models.employee import Employee
from ..models.app_user import AppUser
from ..models.asset import Asset
from ..models.project import Project
from ..models.image_collection import ImageCollection
from ..models.virt_source import VirtualizationSource
from ..models.vm_type import VMType
from ..models.vm_status import VMStatus
from ..models.virtual_machine import VirtualMachine
from ..models.department import Department
from ..models.imaging_method import ImagingMethod
from ..services.activity_tracker import ActivityTracker

class VMCreationState(rx.State):
    """State for VM Creation form."""
    
    # Form fields
    selected_employee: str = ""
    selected_asset: str = ""
    selected_project: str = ""
    selected_image_collection: str = ""
    selected_virt_source: str = ""
    selected_vm_type: str = ""
    selected_vm_status: str = ""
    ram_mb: str = ""
    cpu_cores: str = ""
    disk_size_mb: str = ""
    acas_scan_completed: bool = False
    scap_scan_completed: bool = False
    
    # Dropdown data
    employees: list[str] = []
    assets: list[str] = []
    projects: list[str] = []
    image_collections: list[str] = []
    virt_sources: list[str] = []
    vm_types: list[str] = []
    vm_statuses: list[str] = []
    
    # Lookup mappings
    employee_map: dict[str, int] = {}
    asset_map: dict[str, int] = {}
    project_map: dict[str, int] = {}
    image_collection_map: dict[str, int] = {}
    virt_source_map: dict[str, int] = {}
    vm_type_map: dict[str, int] = {}
    vm_status_map: dict[str, int] = {}
    
    # Additional asset data for filtering
    asset_project_map: dict[int, int] = {}
    image_collection_asset_map: dict[int, int] = {}
    
    # UI state
    loading: bool = False
    form_key: str = "initial"
    submission_message: str = ""
    submission_status: str = ""  # success, error, ""
    
    # Slider dialog state
    show_ram_dialog: bool = False
    temp_ram_mb: str = ""
    show_disk_dialog: bool = False
    temp_disk_mb: str = ""
    
    @rx.var
    def slider_ram_value(self) -> list[int]:
        """Get the RAM value for the slider as a list."""
        try:
            if self.temp_ram_mb and self.temp_ram_mb.isdigit():
                return [int(self.temp_ram_mb)]
        except:
            pass
        return [8192]
    
    @rx.var
    def slider_disk_value(self) -> list[int]:
        """Get the Disk value for the slider as a list."""
        try:
            if self.temp_disk_mb and self.temp_disk_mb.isdigit():
                return [int(self.temp_disk_mb)]
        except:
            pass
        return [262144]  # 256 GB default
    
    @rx.var
    def is_form_valid(self) -> bool:
        """Check if form is valid for submission."""
        # Required fields
        required_fields = [
            self.selected_employee,
            self.selected_asset,
            self.selected_project,
            self.selected_image_collection,
            self.selected_virt_source,
            self.selected_vm_type,
            self.selected_vm_status
        ]
        
        # Check all required fields are filled
        if not all(required_fields):
            return False
        
        # Check optional numeric fields are valid if provided
        if self.ram_mb and not self.ram_mb.isdigit():
            return False
        if self.cpu_cores and not self.cpu_cores.isdigit():
            return False
        if self.disk_size_mb and not self.disk_size_mb.isdigit():
            return False
        
        return True
    
    @rx.var
    def filtered_assets(self) -> list[str]:
        """Filter assets based on selected project."""
        if not self.selected_project:
            return self.assets
        
        # Get project ID from selected name
        project_id = self.project_map.get(self.selected_project)
        if not project_id:
            return self.assets if self.assets else []
        
        # Filter assets by project
        filtered = []
        for asset_display, asset_id in self.asset_map.items():
            if self.asset_project_map.get(asset_id) == project_id:
                filtered.append(asset_display)
        return filtered if filtered else []
    
    @rx.var
    def filtered_image_collections(self) -> list[str]:
        """Filter image collections based on selected asset."""
        if not self.selected_asset:
            return self.image_collections
        
        # Get asset ID from selected name
        asset_id = self.asset_map.get(self.selected_asset)
        if not asset_id:
            return self.image_collections if self.image_collections else []
        
        # Filter image collections by asset
        filtered = []
        for img_display, img_id in self.image_collection_map.items():
            if self.image_collection_asset_map.get(img_id) == asset_id:
                filtered.append(img_display)
        return filtered if filtered else []
    
    async def load_dropdowns(self):
        """Load all dropdown data from database."""
        self.loading = True
        yield
        
        
        try:
            with rx.session() as session:
                # Load employees from Cybersecurity department only
                cyber_dept = session.exec(
                    select(Department).where(Department.dept_name == "Cybersecurity")
                ).first()
                
                if cyber_dept:
                    employees_query = select(Employee).where(Employee.department_id == cyber_dept.dept_id)
                    employees = session.exec(employees_query).all()
                    self.employees = []
                    self.employee_map = {}
                    for emp in employees:
                        display_name = f"{emp.first_name} {emp.last_name}"
                        self.employees.append(display_name)
                        self.employee_map[display_name] = emp.id
                
                # Load projects
                projects = session.exec(select(Project)).all()
                self.projects = []
                self.project_map = {}
                for p in projects:
                    if p.project_name:  # Only add non-empty project names
                        self.projects.append(p.project_name)
                        self.project_map[p.project_name] = p.project_id
                
                # Load assets
                assets = session.exec(select(Asset)).all()
                self.assets = []
                self.asset_map = {}
                self.asset_project_map = {}
                for a in assets:
                    if a.asset_name:  # Only add assets with names
                        barcode = a.letterkenny_barcode or "No Barcode"
                        display_name = f"{a.asset_name} ({barcode})"
                        self.assets.append(display_name)
                        self.asset_map[display_name] = a.asset_id
                        self.asset_project_map[a.asset_id] = a.project_id
                
                # Load image collections
                img_collections = session.exec(select(ImageCollection)).all()
                self.image_collections = []
                self.image_collection_map = {}
                self.image_collection_asset_map = {}
                for img in img_collections:
                    date_str = img.imgcollection_date.strftime("%Y-%m-%d %H:%M") if img.imgcollection_date else "Unknown Date"
                    display_name = f"{date_str} - {img.imaging_result}"
                    self.image_collections.append(display_name)
                    self.image_collection_map[display_name] = img.imgcollection_id
                    self.image_collection_asset_map[img.imgcollection_id] = img.asset_id
                
                # Load virtualization sources
                virt_sources = session.exec(select(VirtualizationSource)).all()
                self.virt_sources = []
                self.virt_source_map = {}
                for vs in virt_sources:
                    if vs.virt_source:  # Only add non-empty sources
                        self.virt_sources.append(vs.virt_source)
                        self.virt_source_map[vs.virt_source] = vs.virtsource_id
                
                # Load VM types
                vm_types = session.exec(select(VMType)).all()
                self.vm_types = []
                self.vm_type_map = {}
                for vt in vm_types:
                    if vt.vm_type:  # Only add non-empty VM types
                        self.vm_types.append(vt.vm_type)
                        self.vm_type_map[vt.vm_type] = vt.vmtype_id
                
                # Load VM statuses
                vm_statuses = session.exec(select(VMStatus)).all()
                self.vm_statuses = []
                self.vm_status_map = {}
                for vs in vm_statuses:
                    if vs.vm_status:  # Only add non-empty statuses
                        self.vm_statuses.append(vs.vm_status)
                        self.vm_status_map[vs.vm_status] = vs.vmstatus_id
        
        except Exception as e:
            print(f"Error loading dropdowns: {e}")
            self.employees = []
            self.projects = []
            self.assets = []
            self.image_collections = []
            self.virt_sources = []
            self.vm_types = []
            self.vm_statuses = []
        finally:
            self.loading = False
            yield
    
    def set_employee(self, value: str):
        """Set selected employee."""
        self.selected_employee = value
    
    def set_asset(self, value: str):
        """Set selected asset and clear dependent fields."""
        self.selected_asset = value
        self.selected_image_collection = ""
    
    def set_project(self, value: str):
        """Set selected project and clear dependent fields."""
        self.selected_project = value
        self.selected_asset = ""
        self.selected_image_collection = ""
    
    def set_image_collection(self, value: str):
        """Set selected image collection."""
        self.selected_image_collection = value
    
    def set_virt_source(self, value: str):
        """Set selected virtualization source."""
        self.selected_virt_source = value
    
    def set_vm_type(self, value: str):
        """Set selected VM type."""
        self.selected_vm_type = value
    
    def set_vm_status(self, value: str):
        """Set selected VM status."""
        self.selected_vm_status = value
    
    def set_ram_mb(self, value: str):
        """Set RAM MB value."""
        self.ram_mb = value
    
    def set_cpu_cores(self, value: str):
        """Set CPU cores value."""
        self.cpu_cores = value
    
    def set_disk_size_mb(self, value: str):
        """Set disk size MB value."""
        self.disk_size_mb = value
    
    def toggle_acas_scan(self, value: bool):
        """Toggle ACAS scan completed status."""
        self.acas_scan_completed = value
    
    def toggle_scap_scan(self, value: bool):
        """Toggle SCAP scan completed status."""
        self.scap_scan_completed = value
    
    async def submit_vm_creation(self):
        """Submit VM creation to database."""
        if not self.is_form_valid:
            self.submission_status = "error"
            self.submission_message = "Please fill in all required fields."
            return
        
        try:
            with rx.session() as session:
                # Get IDs from mappings
                employee_id = self.employee_map.get(self.selected_employee)
                project_id = self.project_map.get(self.selected_project)
                asset_id = self.asset_map.get(self.selected_asset)
                image_collection_id = self.image_collection_map.get(self.selected_image_collection)
                virt_source_id = self.virt_source_map.get(self.selected_virt_source)
                vm_type_id = self.vm_type_map.get(self.selected_vm_type)
                vm_status_id = self.vm_status_map.get(self.selected_vm_status)
                
                # Validation: Check if status is "Fully Functional" but scans are not completed
                status_was_overridden = False
                if ("Fully Functional" in self.selected_vm_status and 
                    "Ready For Use" in self.selected_vm_status and
                    (not self.acas_scan_completed or not self.scap_scan_completed)):
                    # Override status to "Fully Functional | Waiting For Scans"
                    waiting_status = "Fully Functional | Waiting For Scans"
                    vm_status_id = self.vm_status_map.get(waiting_status)
                    status_was_overridden = True
                    if not vm_status_id:
                        # Fallback if status doesn't exist - shouldn't happen with proper seeding
                        self.submission_status = "error"
                        self.submission_message = "Error: 'Fully Functional | Waiting For Scans' status not found in database."
                        return
                
                # Create new VirtualMachine record
                new_vm = VirtualMachine(
                    asset_id=asset_id,
                    project_id=project_id,
                    imgcollection_id=image_collection_id,
                    virtsource_id=virt_source_id,
                    creator_employee_id=employee_id,
                    vmtype_id=vm_type_id,
                    vmstatus_id=vm_status_id,
                    ram_mb=int(self.ram_mb) if self.ram_mb else None,
                    cpu_cores=int(self.cpu_cores) if self.cpu_cores else None,
                    disk_size_mb=int(self.disk_size_mb) if self.disk_size_mb else None,
                    acas_scan_completed=self.acas_scan_completed,
                    scap_scan_completed=self.scap_scan_completed
                )
                
                session.add(new_vm)
                session.commit()
                
                # Track activity
                vm_type_name = self.selected_vm_type
                ActivityTracker.track_vm_creation(
                    vm_id=new_vm.virtmachine_id,
                    asset_id=asset_id,
                    project_id=project_id,
                    employee_id=employee_id,
                    vm_type=vm_type_name
                )
                
                # Success notification
                self.submission_status = "success"
                if status_was_overridden:
                    self.submission_message = "Virtual Machine created successfully! Note: Status was automatically set to 'Fully Functional | Waiting For Scans' because ACAS/SCAP scans are not complete."
                else:
                    self.submission_message = "Virtual Machine created successfully!"
                
                # Reset form
                self.reset_form()
                
                # Refresh the table to show new records
                from .vm_creation_table_state import VMCreationTableState
                table_state = await self.get_state(VMCreationTableState)
                table_state.load_vm_records()
        
        except Exception as e:
            print(f"Error creating VM: {e}")
            self.submission_status = "error"
            self.submission_message = f"Error creating VM: {str(e)}"
    
    def reset_form(self):
        """Reset all form fields."""
        self.selected_employee = ""
        self.selected_asset = ""
        self.selected_project = ""
        self.selected_image_collection = ""
        self.selected_virt_source = ""
        self.selected_vm_type = ""
        self.selected_vm_status = ""
        self.ram_mb = ""
        self.cpu_cores = ""
        self.disk_size_mb = ""
        self.acas_scan_completed = False
        self.scap_scan_completed = False
        self.form_key = f"reset-{datetime.now().timestamp()}"
    
    def clear_message(self):
        """Clear submission message."""
        self.submission_message = ""
        self.submission_status = ""
    
    def open_ram_dialog(self):
        """Open the RAM slider dialog."""
        self.temp_ram_mb = self.ram_mb or "8192"
        self.show_ram_dialog = True
    
    def close_ram_dialog(self):
        """Close the RAM slider dialog without saving."""
        self.show_ram_dialog = False
        self.temp_ram_mb = ""
    
    def cancel_ram_dialog(self):
        """Cancel and close the RAM slider dialog."""
        self.close_ram_dialog()
    
    def apply_ram_dialog(self):
        """Apply the selected RAM value and close dialog."""
        if self.temp_ram_mb and self.temp_ram_mb.isdigit():
            self.ram_mb = self.temp_ram_mb
        self.close_ram_dialog()
    
    def set_temp_ram_mb(self, value: str):
        """Set temporary RAM MB value in dialog from text input."""
        if value and (value.isdigit() or value == ""):
            self.temp_ram_mb = value
    
    def set_temp_ram_mb_from_slider(self, value: list[int | float]):
        """Set temporary RAM MB value from slider."""
        if value and len(value) > 0:
            self.temp_ram_mb = str(int(value[0]))
    
    def open_disk_dialog(self):
        """Open the Disk slider dialog."""
        self.temp_disk_mb = self.disk_size_mb or "262144"
        self.show_disk_dialog = True
    
    def close_disk_dialog(self):
        """Close the Disk slider dialog without saving."""
        self.show_disk_dialog = False
        self.temp_disk_mb = ""
    
    def cancel_disk_dialog(self):
        """Cancel and close the Disk slider dialog."""
        self.close_disk_dialog()
    
    def apply_disk_dialog(self):
        """Apply the selected Disk value and close dialog."""
        if self.temp_disk_mb and self.temp_disk_mb.isdigit():
            self.disk_size_mb = self.temp_disk_mb
        self.close_disk_dialog()
    
    def set_temp_disk_mb(self, value: str):
        """Set temporary Disk MB value in dialog from text input."""
        if value and (value.isdigit() or value == ""):
            self.temp_disk_mb = value
    
    def set_temp_disk_mb_from_slider(self, value: list[int | float]):
        """Set temporary Disk MB value from slider."""
        if value and len(value) > 0:
            self.temp_disk_mb = str(int(value[0]))