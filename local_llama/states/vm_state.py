import reflex as rx
from typing import List, Dict, Optional
from sqlmodel import Session, select, func, and_, or_
from datetime import datetime, timedelta
from ..models.virtual_machine import VirtualMachine
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.image_collection import ImageCollection
from ..models.virt_source import VirtualizationSource
from ..models.vm_type import VMType
from ..models.vm_status import VMStatus


class VMState(rx.State):
    """State management for VM creation form and submission."""
    
    # Form fields
    selected_asset_id: str = ""
    selected_project_id: str = ""
    selected_imgcollection_id: str = ""
    selected_virtsource_id: str = ""
    selected_creator_employee_id: str = ""
    selected_vmtype_id: str = ""
    selected_vmstatus_id: str = ""
    
    # VM Specifications
    ram_gb: str = ""
    cpu_cores: str = ""
    disk_size_gb: str = ""
    
    # Scan Status
    acas_scan_completed: bool = False
    scap_scan_completed: bool = False
    
    # Form validation and submission
    is_submitting: bool = False
    form_key: int = 0
    submission_message: str = ""
    submission_status: str = ""  # success, error, ""
    
    # Dropdown data
    assets: List[str] = []
    projects: List[str] = []
    image_collections: List[str] = []
    virtualization_sources: List[str] = []
    employees: List[str] = []
    vm_types: List[str] = []
    vm_statuses: List[str] = []
    
    # Hidden mappings for value lookups
    asset_map: Dict[str, str] = {}
    project_map: Dict[str, str] = {}
    imgcollection_map: Dict[str, str] = {}
    virtsource_map: Dict[str, str] = {}
    employee_map: Dict[str, str] = {}
    vmtype_map: Dict[str, str] = {}
    vmstatus_map: Dict[str, str] = {}
    
    # Table data and pagination
    virtual_machines: List[Dict] = []
    current_page: int = 1
    total_pages: int = 1
    items_per_page: int = 20
    total_vms: int = 0
    
    @rx.event
    async def load_form_data(self):
        """Load dropdown data for the form."""
        try:
            with rx.session() as session:
                # Load Assets
                assets = session.exec(select(Asset)).all()
                self.assets = [f"{asset.asset_name} (ID: {asset.asset_id})" for asset in assets]
                self.asset_map = {f"{asset.asset_name} (ID: {asset.asset_id})": str(asset.asset_id) for asset in assets}
                
                # Load Projects
                projects = session.exec(select(Project)).all()
                self.projects = [project.project_name for project in projects]
                self.project_map = {project.project_name: str(project.project_id) for project in projects}
                
                # Load Image Collections
                image_collections = session.exec(select(ImageCollection)).all()
                self.image_collections = [f"Image {img.imgcollection_id} - {img.imgcollection_date.strftime('%Y-%m-%d')}" for img in image_collections]
                self.imgcollection_map = {f"Image {img.imgcollection_id} - {img.imgcollection_date.strftime('%Y-%m-%d')}": str(img.imgcollection_id) for img in image_collections}
                
                # Load Virtualization Sources
                virt_sources = session.exec(select(VirtualizationSource)).all()
                self.virtualization_sources = [source.virt_source for source in virt_sources]
                self.virtsource_map = {source.virt_source: str(source.virtsource_id) for source in virt_sources}
                
                # Load Employees
                employees = session.exec(select(Employee)).all()
                self.employees = [f"{emp.first_name} {emp.last_name}" for emp in employees]
                self.employee_map = {f"{emp.first_name} {emp.last_name}": str(emp.id) for emp in employees}
                
                # Load VM Types
                vm_types = session.exec(select(VMType)).all()
                self.vm_types = [vmtype.vm_type for vmtype in vm_types]
                self.vmtype_map = {vmtype.vm_type: str(vmtype.vmtype_id) for vmtype in vm_types}
                
                # Load VM Statuses
                vm_statuses = session.exec(select(VMStatus)).all()
                self.vm_statuses = [status.vm_status for status in vm_statuses]
                self.vmstatus_map = {status.vm_status: str(status.vmstatus_id) for status in vm_statuses}
                
        except Exception as e:
            print(f"Error loading form data: {e}")

    @rx.var
    def form_is_valid(self) -> bool:
        """Check if form has all required fields."""
        return all([
            self.selected_asset_id,
            self.selected_project_id,
            self.selected_imgcollection_id,
            self.selected_virtsource_id,
            self.selected_creator_employee_id,
            self.selected_vmtype_id,
            self.selected_vmstatus_id,
        ])

    @rx.event
    async def create_vm(self):
        """Create new virtual machine record."""
        if not self.form_is_valid:
            return
            
        self.is_submitting = True
        
        try:
            with rx.session() as session:
                # Convert string values to integers
                ram_gb_int = int(self.ram_gb) if self.ram_gb else None
                cpu_cores_int = int(self.cpu_cores) if self.cpu_cores else None
                disk_size_gb_int = int(self.disk_size_gb) if self.disk_size_gb else None
                
                # Create new VM record
                new_vm = VirtualMachine(
                    asset_id=int(self.selected_asset_id),
                    project_id=int(self.selected_project_id),
                    imgcollection_id=int(self.selected_imgcollection_id),
                    virtsource_id=int(self.selected_virtsource_id),
                    creator_employee_id=int(self.selected_creator_employee_id),
                    vmtype_id=int(self.selected_vmtype_id),
                    vmstatus_id=int(self.selected_vmstatus_id),
                    ram_gb=ram_gb_int,
                    cpu_cores=cpu_cores_int,
                    disk_size_gb=disk_size_gb_int,
                    acas_scan_completed=self.acas_scan_completed,
                    scap_scan_completed=self.scap_scan_completed
                )
                
                session.add(new_vm)
                session.commit()
                
                self.submission_status = "success"
                self.submission_message = "Virtual machine created successfully!"
                
                # Reset form
                await self.reset_form()
                
                # Refresh VM table
                await self.load_virtual_machines()
                
        except Exception as e:
            self.submission_status = "error"
            self.submission_message = f"Error creating VM: {str(e)}"
            print(f"VM creation error: {e}")
        
        finally:
            self.is_submitting = False

    @rx.event
    async def reset_form(self):
        """Reset all form fields."""
        self.selected_asset_id = ""
        self.selected_project_id = ""
        self.selected_imgcollection_id = ""
        self.selected_virtsource_id = ""
        self.selected_creator_employee_id = ""
        self.selected_vmtype_id = ""
        self.selected_vmstatus_id = ""
        self.ram_gb = ""
        self.cpu_cores = ""
        self.disk_size_gb = ""
        self.acas_scan_completed = False
        self.scap_scan_completed = False
        self.form_key += 1

    @rx.event
    async def load_virtual_machines(self):
        """Load virtual machines with pagination."""
        try:
            with rx.session() as session:
                # Calculate offset
                offset = (self.current_page - 1) * self.items_per_page
                
                # Get total count
                total_count = session.exec(select(func.count(VirtualMachine.virtmachine_id))).first()
                self.total_vms = total_count or 0
                self.total_pages = max(1, (self.total_vms + self.items_per_page - 1) // self.items_per_page)
                
                # Query with joins for display data - order by newest first
                query = select(VirtualMachine).offset(offset).limit(self.items_per_page).order_by(VirtualMachine.virtmachine_id.desc())
                virtual_machines = session.exec(query).all()
                
                # Format data for table display
                vm_data = []
                for vm in virtual_machines:
                    # Get related data
                    asset = session.get(Asset, vm.asset_id)
                    project = session.get(Project, vm.project_id)
                    img_collection = session.get(ImageCollection, vm.imgcollection_id)
                    virt_source = session.get(VirtualizationSource, vm.virtsource_id)
                    creator = session.get(Employee, vm.creator_employee_id)
                    vm_type = session.get(VMType, vm.vmtype_id)
                    vm_status = session.get(VMStatus, vm.vmstatus_id)
                    
                    vm_data.append({
                        "virtmachine_id": vm.virtmachine_id,
                        "asset_name": asset.asset_name if asset else "Unknown",
                        "project_name": project.project_name if project else "Unknown",
                        "image_date": img_collection.imgcollection_date.strftime('%Y-%m-%d') if img_collection else "Unknown",
                        "virt_source": virt_source.virt_source if virt_source else "Unknown",
                        "creator_name": f"{creator.first_name} {creator.last_name}" if creator else "Unknown",
                        "vm_type": vm_type.vm_type if vm_type else "Unknown",
                        "vm_status": vm_status.vm_status if vm_status else "Unknown",
                        "ram_gb": vm.ram_gb,
                        "cpu_cores": vm.cpu_cores,
                        "disk_size_gb": vm.disk_size_gb,
                        "acas_scan": vm.acas_scan_completed,
                        "scap_scan": vm.scap_scan_completed,
                    })
                
                self.virtual_machines = vm_data
                
        except Exception as e:
            print(f"Error loading virtual machines: {e}")

    @rx.event
    async def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.load_virtual_machines()

    @rx.event
    async def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            await self.load_virtual_machines()

    @rx.event
    async def goto_page(self, page: int):
        """Go to specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            await self.load_virtual_machines()

    # Form field setters
    def set_asset(self, value: str):
        self.selected_asset_id = self.asset_map.get(value, "")

    def set_project(self, value: str):
        self.selected_project_id = self.project_map.get(value, "")

    def set_imgcollection(self, value: str):
        self.selected_imgcollection_id = self.imgcollection_map.get(value, "")

    def set_virtsource(self, value: str):
        self.selected_virtsource_id = self.virtsource_map.get(value, "")

    def set_creator_employee(self, value: str):
        self.selected_creator_employee_id = self.employee_map.get(value, "")

    def set_vmtype(self, value: str):
        self.selected_vmtype_id = self.vmtype_map.get(value, "")

    def set_vmstatus(self, value: str):
        self.selected_vmstatus_id = self.vmstatus_map.get(value, "")

    def set_ram_gb(self, value: str):
        self.ram_gb = value

    def set_cpu_cores(self, value: str):
        self.cpu_cores = value

    def set_disk_size_gb(self, value: str):
        self.disk_size_gb = value

    def set_acas_scan(self, checked: bool):
        self.acas_scan_completed = checked

    def set_scap_scan(self, checked: bool):
        self.scap_scan_completed = checked