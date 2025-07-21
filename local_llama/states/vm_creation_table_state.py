"""State management for Virtual Machine Creation Table."""
import reflex as rx
from datetime import datetime, timedelta
from sqlmodel import select, Session, func, and_, text
from ..models.virtual_machine import VirtualMachine
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.virt_source import VirtualizationSource
from ..models.vm_type import VMType
from ..models.vm_status import VMStatus
from ..models.virtual_machine import VirtualMachine

class VMCreationTableState(rx.State):
    """State for VM Creation table."""
    
    # Table data
    vm_records: list[dict] = []
    filtered_records: list[dict] = []
    
    # Pagination
    current_page: int = 1
    page_size: int = 20
    total_records: int = 0
    
    # Sorting
    sort_column: str = "virtmachine_id"
    sort_order: str = "desc"
    
    # Loading state
    loading: bool = False
    
    # Edit modal state
    show_edit_modal: bool = False
    editing_vm_id: int = 0
    edit_vm_status: str = ""
    edit_ram_gb: str = ""
    edit_cpu_cores: str = ""
    edit_disk_size_gb: str = ""
    edit_acas_scan: bool = False
    edit_scap_scan: bool = False
    
    # Dropdown data for edit modal
    vm_statuses: list[str] = []
    vm_status_map: dict[str, int] = {}
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        return max(1, (self.total_records + self.page_size - 1) // self.page_size)
    
    @rx.var
    def current_page_records(self) -> list[dict]:
        """Get records for current page."""
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_records[start:end]
    
    @rx.var
    def current_page_start(self) -> int:
        """Calculate starting record number for current page."""
        if self.total_records == 0:
            return 0
        return (self.current_page - 1) * self.page_size + 1
    
    @rx.var
    def current_page_end(self) -> int:
        """Calculate ending record number for current page."""
        end = self.current_page * self.page_size
        return min(end, self.total_records)
    
    async def load_vm_records(self):
        """Load VM records from database."""
        self.loading = True
        yield
        
        try:
            with rx.session() as session:
                # Build query with joins
                query = (
                    select(
                        VirtualMachine.virtmachine_id,
                        VirtualMachine.ram_gb,
                        VirtualMachine.cpu_cores,
                        VirtualMachine.disk_size_gb,
                        VirtualMachine.acas_scan_completed,
                        VirtualMachine.scap_scan_completed,
                        Employee.first_name,
                        Employee.last_name,
                        Employee.id.label("employee_id"),
                        Asset.asset_name,
                        Asset.letterkenny_barcode,
                        Project.project_name,
                        VirtualizationSource.virt_source,
                        VMType.vm_type,
                        VMStatus.vm_status
                    )
                    .join(Employee, VirtualMachine.creator_employee_id == Employee.id)
                    .join(Asset, VirtualMachine.asset_id == Asset.asset_id)
                    .join(Project, VirtualMachine.project_id == Project.project_id)
                    .join(VirtualizationSource, VirtualMachine.virtsource_id == VirtualizationSource.virtsource_id)
                    .join(VMType, VirtualMachine.vmtype_id == VMType.vmtype_id)
                    .join(VMStatus, VirtualMachine.vmstatus_id == VMStatus.vmstatus_id)
                )
                
                results = session.exec(query).all()
                
                # Process results
                self.vm_records = []
                for row in results:
                    # Determine status color
                    status_color = "green"
                    if "Fully Functional" in row.vm_status:
                        status_color = "green"
                    elif "Testing" in row.vm_status or "Machine Created" in row.vm_status:
                        status_color = "yellow"
                    else:
                        status_color = "red"
                    
                    self.vm_records.append({
                        "virtmachine_id": row.virtmachine_id,
                        "creator": f"{row.first_name} {row.last_name}",
                        "employee_id": row.employee_id,
                        "asset_name": row.asset_name,
                        "barcode": row.letterkenny_barcode or "N/A",
                        "project_name": row.project_name,
                        "virt_source": row.virt_source,
                        "vm_type": row.vm_type,
                        "vm_status": row.vm_status,
                        "status_color": status_color,
                        "ram_gb": row.ram_gb or "N/A",
                        "cpu_cores": row.cpu_cores or "N/A",
                        "disk_size_gb": row.disk_size_gb or "N/A",
                        "acas_scan": row.acas_scan_completed,
                        "scap_scan": row.scap_scan_completed,
                        "is_recent": False,  # Will be set later
                        "is_duplicate": False,  # Will be set later
                        "is_ready": "Fully Functional" in row.vm_status or row.vm_status == "Machine Created | Ready For Use"  # Check if ready
                    })
                
                # Mark 10 most recent entries
                if self.vm_records:
                    sorted_by_id = sorted(self.vm_records, key=lambda x: x["virtmachine_id"], reverse=True)
                    for i in range(min(10, len(sorted_by_id))):
                        sorted_by_id[i]["is_recent"] = True
                
                # Mark duplicate VMs (same asset, project, and VM type)
                # Since we don't have timestamps, we'll consider duplicates based on key fields
                seen_combinations = {}
                for record in self.vm_records:
                    # Create a key from the combination of fields that define a duplicate
                    key = (
                        record["asset_name"],
                        record["project_name"],
                        record["vm_type"]
                    )
                    
                    if key in seen_combinations:
                        # This is a duplicate
                        record["is_duplicate"] = True
                    else:
                        # First occurrence
                        seen_combinations[key] = record["virtmachine_id"]
                
                # Load VM statuses for edit modal
                vm_statuses = session.exec(select(VMStatus)).all()
                self.vm_statuses = []
                self.vm_status_map = {}
                for vs in vm_statuses:
                    if vs.vm_status:
                        self.vm_statuses.append(vs.vm_status)
                        self.vm_status_map[vs.vm_status] = vs.vmstatus_id
                
                # Apply initial sorting
                yield self.sort_records(self.sort_column, self.sort_order)
                
        except Exception as e:
            print(f"Error loading VM records: {e}")
            self.vm_records = []
            self.filtered_records = []
            self.total_records = 0
        finally:
            self.loading = False
            yield
    
    def sort_records(self, column: str, order: str = None):
        """Sort records by specified column."""
        if order is None:
            # Toggle sort order if same column
            if column == self.sort_column:
                order = "asc" if self.sort_order == "desc" else "desc"
            else:
                order = "asc"
        
        self.sort_column = column
        self.sort_order = order
        
        # Define sort key functions
        sort_keys = {
            "virtmachine_id": lambda x: x["virtmachine_id"],
            "creator": lambda x: x["creator"],
            "asset_name": lambda x: x["asset_name"],
            "project_name": lambda x: x["project_name"],
            "virt_source": lambda x: x["virt_source"],
            "vm_type": lambda x: x["vm_type"],
            "vm_status": lambda x: x["vm_status"],
            "ram_gb": lambda x: int(x["ram_gb"]) if x["ram_gb"] != "N/A" else 0,
            "cpu_cores": lambda x: int(x["cpu_cores"]) if x["cpu_cores"] != "N/A" else 0,
            "disk_size_gb": lambda x: int(x["disk_size_gb"]) if x["disk_size_gb"] != "N/A" else 0
        }
        
        if column in sort_keys:
            self.filtered_records = sorted(
                self.vm_records,
                key=sort_keys[column],
                reverse=(order == "desc")
            )
            self.total_records = len(self.filtered_records)
            self.current_page = 1
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
    
    def go_to_page(self, page: int):
        """Go to specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
    
    def open_edit_modal(self, vm_id: int):
        """Open edit modal for a specific VM."""
        self.editing_vm_id = vm_id
        
        # Find the VM record
        vm_record = next((vm for vm in self.vm_records if vm["virtmachine_id"] == vm_id), None)
        if vm_record:
            self.edit_vm_status = vm_record["vm_status"]
            self.edit_ram_gb = str(vm_record["ram_gb"]) if vm_record["ram_gb"] != "N/A" else ""
            self.edit_cpu_cores = str(vm_record["cpu_cores"]) if vm_record["cpu_cores"] != "N/A" else ""
            self.edit_disk_size_gb = str(vm_record["disk_size_gb"]) if vm_record["disk_size_gb"] != "N/A" else ""
            self.edit_acas_scan = vm_record["acas_scan"]
            self.edit_scap_scan = vm_record["scap_scan"]
            self.show_edit_modal = True
    
    def close_edit_modal(self):
        """Close the edit modal."""
        self.show_edit_modal = False
        self.editing_vm_id = 0
        self.edit_vm_status = ""
        self.edit_ram_gb = ""
        self.edit_cpu_cores = ""
        self.edit_disk_size_gb = ""
        self.edit_acas_scan = False
        self.edit_scap_scan = False
    
    def set_edit_vm_status(self, value: str):
        """Set VM status in edit modal."""
        self.edit_vm_status = value
    
    def set_edit_ram_gb(self, value: str):
        """Set RAM GB in edit modal."""
        self.edit_ram_gb = value
    
    def set_edit_cpu_cores(self, value: str):
        """Set CPU cores in edit modal."""
        self.edit_cpu_cores = value
    
    def set_edit_disk_size_gb(self, value: str):
        """Set disk size in edit modal."""
        self.edit_disk_size_gb = value
    
    def toggle_edit_acas_scan(self, value: bool):
        """Toggle ACAS scan in edit modal."""
        self.edit_acas_scan = value
    
    def toggle_edit_scap_scan(self, value: bool):
        """Toggle SCAP scan in edit modal."""
        self.edit_scap_scan = value
    
    async def update_vm(self):
        """Update the VM in the database."""
        try:
            with rx.session() as session:
                # Get the VM
                vm = session.exec(
                    select(VirtualMachine).where(VirtualMachine.virtmachine_id == self.editing_vm_id)
                ).first()
                
                if vm:
                    # Update VM status
                    if self.edit_vm_status:
                        vm_status_id = self.vm_status_map.get(self.edit_vm_status)
                        if vm_status_id:
                            vm.vmstatus_id = vm_status_id
                    
                    # Update specs
                    vm.ram_gb = int(self.edit_ram_gb) if self.edit_ram_gb else None
                    vm.cpu_cores = int(self.edit_cpu_cores) if self.edit_cpu_cores else None
                    vm.disk_size_gb = int(self.edit_disk_size_gb) if self.edit_disk_size_gb else None
                    
                    # Update scans
                    vm.acas_scan_completed = self.edit_acas_scan
                    vm.scap_scan_completed = self.edit_scap_scan
                    
                    session.commit()
                    
                    # Close modal
                    self.close_edit_modal()
                    
                    # Show success message
                    yield rx.window_alert("Virtual Machine updated successfully!")
                    
                    # Refresh the page to reload the table
                    yield rx.call_script("window.location.reload()")
                
        except Exception as e:
            print(f"Error updating VM: {e}")
            yield rx.window_alert(f"Error updating VM: {str(e)}")