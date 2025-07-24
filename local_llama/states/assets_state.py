"""State management for Assets page."""
import reflex as rx
from sqlmodel import select, func, or_, and_
from typing import List, Dict, Any
from datetime import datetime
import os
from ..models.asset import Asset
from ..models.project import Project
from ..models.building import Building
from ..models.floor import Floor
from ..models.room import Room
from ..models.sys_type import SysType
from ..models.operating_system import OperatingSystem
from ..models.hardware_manufacturer import HardwareManufacturer
from ..models.employee import Employee


class AssetsState(rx.State):
    """State for Assets page with advanced table functionality."""
    
    # Data
    assets: List[Dict[str, Any]] = []
    filtered_assets: List[Dict[str, Any]] = []
    
    # Table state
    is_loading: bool = False
    selected_rows: List[str] = []
    select_all: bool = False
    
    # Pagination
    page: int = 1
    page_size: int = 25
    total_pages: int = 1
    total_count: int = 0
    
    # Sorting
    sort_column: str = "asset_id"
    sort_direction: str = "asc"
    
    # Filtering
    search_query: str = ""
    filter_project: str = "All Projects"
    filter_building: str = "All Buildings"
    filter_systype: str = "All System Types"
    filter_os: str = "All Operating Systems"
    
    # Dropdowns data - lists of display strings
    projects: List[str] = []
    buildings: List[str] = []
    systypes: List[str] = []
    operating_systems: List[str] = []
    floors: List[str] = []
    
    # Edit dropdowns without "All" options
    edit_projects: List[str] = []
    edit_buildings: List[str] = []
    edit_systypes: List[str] = []
    edit_operating_systems: List[str] = []
    
    # Mappings from display string to database ID (str since some are "all")
    project_map: Dict[str, str] = {}
    building_map: Dict[str, str] = {}
    systype_map: Dict[str, str] = {}
    os_map: Dict[str, str] = {}
    floor_map: Dict[str, str] = {}
    
    # Edit modal state
    edit_modal_open: bool = False
    edit_asset_id: str = ""
    edit_asset_name: str = ""
    edit_project: str = ""
    edit_building: str = ""
    edit_floor: str = ""
    edit_systype: str = ""
    edit_os: str = ""
    edit_serial_no: str = ""
    edit_barcode: str = ""
    
    # Inline editing state
    editing_asset_id: str = ""
    
    # View details modal state
    view_modal_open: bool = False
    view_asset_id: str = ""
    view_asset_name: str = ""
    recent_actions: List[Dict[str, Any]] = []
    
    # Delete confirmation modal state
    delete_modal_open: bool = False
    delete_asset_id: str = ""
    delete_asset_name: str = ""
    delete_confirmation_text: str = ""
    
    # UI state
    show_export_menu: bool = False
    show_column_selector: bool = False
    visible_columns: List[str] = [
        "asset_id", "asset_name", "project", "building", "floor", 
        "systype", "os", "serial_no", "barcode", "actions"
    ]
    
    # Analytics
    assets_by_project: Dict[str, int] = {}
    assets_by_building: Dict[str, int] = {}
    assets_by_systype: Dict[str, int] = {}
    assets_by_os: Dict[str, int] = {}
    
    # Computed properties for counts
    @rx.var
    def project_count(self) -> int:
        """Get count of projects with assets."""
        return len(self.assets_by_project)
    
    @rx.var
    def building_count(self) -> int:
        """Get count of buildings with assets."""
        return len(self.assets_by_building)
    
    @rx.var
    def systype_count(self) -> int:
        """Get count of system types."""
        return len(self.assets_by_systype)
    
    @rx.var
    def os_count(self) -> int:
        """Get count of operating systems."""
        return len(self.assets_by_os)
    
    @rx.var
    def paginated_assets(self) -> List[Dict[str, Any]]:
        """Get paginated subset of filtered assets."""
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_assets[start:end]
    
    @rx.var
    def is_current_page_selected(self) -> bool:
        """Check if all items on current page are selected."""
        if not self.paginated_assets:
            return False
        current_page_ids = [str(asset["asset_id"]) for asset in self.paginated_assets]
        return all(asset_id in self.selected_rows for asset_id in current_page_ids)
    
    async def load_assets_data(self):
        """Load all assets data with relationships."""
        self.is_loading = True
        yield
        
        try:
            with rx.session() as session:
                # Load filter options - display strings with mappings
                # Projects
                self.projects = ["All Projects"]
                self.edit_projects = []
                self.project_map = {"All Projects": "all"}
                projects = session.exec(select(Project).order_by(Project.project_name)).all()
                for p in projects:
                    self.projects.append(p.project_name)
                    self.edit_projects.append(p.project_name)
                    self.project_map[p.project_name] = str(p.project_id)
                
                # Buildings - for filter dropdown, only show buildings that are in use
                self.buildings = ["All Buildings"]
                self.edit_buildings = []
                self.building_map = {"All Buildings": "all"}
                
                # Get distinct building IDs that are actually used by assets
                used_building_ids = session.exec(
                    select(Asset.building_id).distinct()
                    .where(Asset.building_id.isnot(None))
                ).all()
                
                # Get all buildings
                all_buildings = session.exec(select(Building).order_by(Building.building_name)).all()
                for b in all_buildings:
                    # Add to edit dropdown (all buildings available)
                    self.edit_buildings.append(b.building_name)
                    self.building_map[b.building_name] = str(b.building_id)
                    
                    # Only add to filter dropdown if it's in use
                    if b.building_id in used_building_ids:
                        self.buildings.append(b.building_name)
                
                # System Types - for filter dropdown, only show system types that are in use
                self.systypes = ["All System Types"]
                self.edit_systypes = []
                self.systype_map = {"All System Types": "all"}
                
                # Get distinct system type IDs that are actually used by assets
                used_systype_ids = session.exec(
                    select(Asset.systype_id).distinct()
                    .where(Asset.systype_id.isnot(None))
                ).all()
                
                # Get all system types
                all_systypes = session.exec(select(SysType).order_by(SysType.systype_name)).all()
                for s in all_systypes:
                    # Add to edit dropdown (all system types available)
                    self.edit_systypes.append(s.systype_name)
                    self.systype_map[s.systype_name] = str(s.systype_id)
                    
                    # Only add to filter dropdown if it's in use
                    if s.systype_id in used_systype_ids:
                        self.systypes.append(s.systype_name)
                
                # Operating Systems - for filter dropdown, only show OS that are in use
                self.operating_systems = ["All Operating Systems"]
                self.edit_operating_systems = []
                self.os_map = {"All Operating Systems": "all"}
                
                # Get distinct OS IDs that are actually used by assets
                used_os_ids = session.exec(
                    select(Asset.os_id).distinct()
                    .where(Asset.os_id.isnot(None))
                ).all()
                
                # Get all OS for edit dropdown
                all_oses = session.exec(select(OperatingSystem).order_by(OperatingSystem.os_name)).all()
                for os in all_oses:
                    # Add to edit dropdown (all OS available)
                    self.edit_operating_systems.append(os.os_name)
                    self.os_map[os.os_name] = str(os.os_id)
                    
                    # Only add to filter dropdown if it's in use
                    if os.os_id in used_os_ids:
                        self.operating_systems.append(os.os_name)
                
                # Floors
                self.floors = []
                self.floor_map = {}
                floors = session.exec(select(Floor).order_by(Floor.floor_name)).all()
                for f in floors:
                    self.floors.append(f.floor_name)
                    self.floor_map[f.floor_name] = str(f.floor_id)
                
                # Build query with filters
                query = select(Asset)
                
                # Apply filters using mappings
                project_id = self.project_map.get(self.filter_project)
                if project_id and project_id != "all":
                    query = query.where(Asset.project_id == int(project_id))
                
                building_id = self.building_map.get(self.filter_building)
                if building_id and building_id != "all":
                    query = query.where(Asset.building_id == int(building_id))
                
                systype_id = self.systype_map.get(self.filter_systype)
                if systype_id and systype_id != "all":
                    query = query.where(Asset.systype_id == int(systype_id))
                
                os_id = self.os_map.get(self.filter_os)
                if os_id and os_id != "all":
                    query = query.where(Asset.os_id == int(os_id))
                
                # Get total count
                count_query = select(func.count()).select_from(query.subquery())
                self.total_count = session.exec(count_query).one()
                self.total_pages = max(1, (self.total_count + self.page_size - 1) // self.page_size)
                
                # Apply sorting
                if hasattr(Asset, self.sort_column):
                    order_col = getattr(Asset, self.sort_column)
                    if self.sort_direction == "desc":
                        query = query.order_by(order_col.desc())
                    else:
                        query = query.order_by(order_col)
                
                # Execute query without pagination (we'll paginate in the frontend)
                assets = session.exec(query).all()
                
                # Process assets with relationships
                self.assets = []
                for asset in assets:
                    # Get related data
                    project = session.exec(
                        select(Project).where(Project.project_id == asset.project_id)
                    ).first()
                    
                    building = session.exec(
                        select(Building).where(Building.building_id == asset.building_id)
                    ).first()
                    
                    floor = session.exec(
                        select(Floor).where(Floor.floor_id == asset.floor_id)
                    ).first()
                    
                    room = None
                    if asset.room_id:
                        room = session.exec(
                            select(Room).where(Room.room_id == asset.room_id)
                        ).first()
                    
                    systype = session.exec(
                        select(SysType).where(SysType.systype_id == asset.systype_id)
                    ).first()
                    
                    os = None
                    if asset.os_id:
                        os = session.exec(
                            select(OperatingSystem).where(OperatingSystem.os_id == asset.os_id)
                        ).first()
                    
                    hw_manu = None
                    if asset.hwmanu_id:
                        hw_manu = session.exec(
                            select(HardwareManufacturer).where(HardwareManufacturer.hwmanu_id == asset.hwmanu_id)
                        ).first()
                    
                    # Process building name to extract just the number
                    building_display = building.building_name if building else "Unknown"
                    if building_display.startswith("Building "):
                        building_display = building_display.replace("Building ", "")
                    
                    # Process floor name to extract just the level
                    floor_display = floor.floor_name if floor else "Unknown"
                    if floor_display.startswith("Floor "):
                        floor_display = floor_display.replace("Floor ", "")
                    
                    self.assets.append({
                        "asset_id": str(asset.asset_id),
                        "asset_name": asset.asset_name or "Unknown",
                        "project": project.project_name if project else "Unknown",
                        "project_id": asset.project_id,
                        "building": building_display,
                        "building_id": asset.building_id,
                        "floor": floor_display,
                        "floor_id": asset.floor_id,
                        "room": room.room_name if room else "N/A",
                        "room_id": asset.room_id,
                        "systype": systype.systype_name if systype else "Unknown",
                        "systype_id": asset.systype_id,
                        "os": os.os_name if os else "N/A",
                        "os_id": asset.os_id,
                        "hw_manufacturer": hw_manu.hwmanu_name if hw_manu else "N/A",
                        "serial_no": asset.serial_no if asset.serial_no else "N/A",
                        "barcode": asset.letterkenny_barcode if asset.letterkenny_barcode else "N/A",
                        "cpu_id": asset.cpu_id,
                        "gpu_id": asset.gpu_id
                    })
                
                # Apply search filter
                if self.search_query:
                    search_lower = self.search_query.lower()
                    self.filtered_assets = [
                        asset for asset in self.assets
                        if search_lower in str(asset.get("asset_name", "")).lower()
                        or search_lower in str(asset.get("serial_no", "")).lower()
                        or search_lower in str(asset.get("barcode", "")).lower()
                        or search_lower in str(asset.get("project", "")).lower()
                    ]
                else:
                    self.filtered_assets = self.assets
                
                # Update total count and pages based on filtered results
                self.total_count = len(self.filtered_assets)
                self.total_pages = max(1, (self.total_count + self.page_size - 1) // self.page_size)
                
                # Debug print
                print(f"Total assets loaded: {len(self.assets)}")
                print(f"Filtered assets: {len(self.filtered_assets)}")
                
                # Calculate analytics
                self.calculate_analytics()
                
        except Exception as e:
            print(f"Error loading assets: {e}")
        finally:
            self.is_loading = False
            yield
    
    def calculate_analytics(self):
        """Calculate analytics for assets."""
        self.assets_by_project = {}
        self.assets_by_building = {}
        self.assets_by_systype = {}
        self.assets_by_os = {}
        
        for asset in self.assets:
            # By project
            project = asset.get("project", "Unknown")
            self.assets_by_project[project] = self.assets_by_project.get(project, 0) + 1
            
            # By building
            building = asset.get("building", "Unknown")
            self.assets_by_building[building] = self.assets_by_building.get(building, 0) + 1
            
            # By system type
            systype = asset.get("systype", "Unknown")
            self.assets_by_systype[systype] = self.assets_by_systype.get(systype, 0) + 1
            
            # By OS (exclude N/A from count)
            os = asset.get("os", "N/A")
            if os != "N/A":
                self.assets_by_os[os] = self.assets_by_os.get(os, 0) + 1
    
    def set_search_query(self, query: str):
        """Set search query and filter assets."""
        self.search_query = query
        self.page = 1
        return self.load_assets_data()
    
    def set_filter_project(self, project_id: str):
        """Set project filter."""
        self.filter_project = project_id
        self.page = 1
        return self.load_assets_data()
    
    def set_filter_building(self, building_id: str):
        """Set building filter."""
        self.filter_building = building_id
        self.page = 1
        return self.load_assets_data()
    
    def set_filter_systype(self, systype_id: str):
        """Set system type filter."""
        self.filter_systype = systype_id
        self.page = 1
        return self.load_assets_data()
    
    def set_filter_os(self, os_id: str):
        """Set OS filter."""
        self.filter_os = os_id
        self.page = 1
        return self.load_assets_data()
    
    def sort_by_column(self, column: str):
        """Sort by column with toggle direction."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"
        return self.load_assets_data()
    
    def toggle_row_selection(self, asset_id: str):
        """Toggle row selection."""
        if asset_id in self.selected_rows:
            self.selected_rows.remove(asset_id)
        else:
            self.selected_rows.append(asset_id)
    
    def toggle_select_all(self):
        """Toggle select all rows on current page."""
        # Get current page assets
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        current_page_assets = self.filtered_assets[start:end]
        current_page_ids = [str(asset["asset_id"]) for asset in current_page_assets]
        
        # Check if all items on current page are selected
        all_selected = all(asset_id in self.selected_rows for asset_id in current_page_ids)
        
        if all_selected:
            # Deselect all on current page
            self.selected_rows = [id for id in self.selected_rows if id not in current_page_ids]
            self.select_all = False
        else:
            # Select all on current page
            for asset_id in current_page_ids:
                if asset_id not in self.selected_rows:
                    self.selected_rows.append(asset_id)
            self.select_all = True
    
    def next_page(self):
        """Go to next page."""
        if self.page < self.total_pages:
            self.page += 1
            return self.load_assets_data()
    
    def prev_page(self):
        """Go to previous page."""
        if self.page > 1:
            self.page -= 1
            return self.load_assets_data()
    
    def set_page(self, page: int):
        """Set specific page."""
        self.page = max(1, min(page, self.total_pages))
        return self.load_assets_data()
    
    def set_page_size(self, size: str):
        """Set page size."""
        self.page_size = int(size)
        self.page = 1
        return self.load_assets_data()
    
    def toggle_column_visibility(self, column: str):
        """Toggle column visibility."""
        if column in self.visible_columns:
            self.visible_columns.remove(column)
        else:
            self.visible_columns.append(column)
    
    def export_selected(self, format: str):
        """Export selected rows."""
        # This would be implemented with actual export logic
        print(f"Exporting {len(self.selected_rows)} rows as {format}")
        self.show_export_menu = False
    
    def clear_filters(self):
        """Clear all filters."""
        self.search_query = ""
        self.filter_project = "All Projects"
        self.filter_building = "All Buildings"
        self.filter_systype = "All System Types"
        self.filter_os = "All Operating Systems"
        self.page = 1
        return self.load_assets_data()
    
    def open_edit_modal(self, asset_id: str):
        """Open edit modal for a specific asset."""
        # Find the asset in our data
        for asset in self.assets:
            if asset["asset_id"] == asset_id:
                self.edit_asset_id = asset_id
                self.edit_asset_name = asset.get("asset_name", "")
                self.edit_project = asset.get("project", "")
                self.edit_building = asset.get("building", "")
                self.edit_floor = asset.get("floor", "")
                self.edit_systype = asset.get("systype", "")
                self.edit_os = asset.get("os", "N/A") if asset.get("os") != "N/A" else ""
                self.edit_serial_no = asset.get("serial_no", "N/A") if asset.get("serial_no") != "N/A" else ""
                self.edit_barcode = asset.get("barcode", "N/A") if asset.get("barcode") != "N/A" else ""
                self.edit_modal_open = True
                break
    
    def close_edit_modal(self):
        """Close the edit modal."""
        self.edit_modal_open = False
        self.edit_asset_id = ""
    
    def save_asset_changes(self):
        """Save changes to the asset."""
        from sqlmodel import Session, create_engine, select
        from ..models.asset import Asset
        
        try:
            # Get database connection
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                print("Database URL not found")
                return
            
            engine = create_engine(database_url)
            
            with Session(engine) as session:
                # Find the asset
                asset = session.exec(
                    select(Asset).where(Asset.asset_id == int(self.edit_asset_id))
                ).first()
                
                if asset:
                    # Update fields
                    asset.asset_name = self.edit_asset_name
                    
                    # Update IDs based on dropdown selections
                    if self.edit_project and self.edit_project in self.project_map:
                        asset.project_id = int(self.project_map[self.edit_project])
                    
                    if self.edit_building and self.edit_building in self.building_map:
                        asset.building_id = int(self.building_map[self.edit_building])
                    
                    if self.edit_floor and hasattr(self, 'floor_map') and self.edit_floor in self.floor_map:
                        asset.floor_id = int(self.floor_map[self.edit_floor])
                    
                    if self.edit_systype and self.edit_systype in self.systype_map:
                        asset.systype_id = int(self.systype_map[self.edit_systype])
                    
                    if self.edit_os and self.edit_os in self.os_map:
                        asset.os_id = int(self.os_map[self.edit_os])
                    else:
                        asset.os_id = None
                    
                    # Update optional fields
                    asset.serial_no = self.edit_serial_no if self.edit_serial_no else None
                    asset.letterkenny_barcode = self.edit_barcode if self.edit_barcode else None
                    
                    # Commit changes
                    session.add(asset)
                    session.commit()
                    
                    print(f"Successfully updated asset {asset.asset_name}")
                    
                    # Close modal and reload data
                    self.close_edit_modal()
                    return self.load_assets_data()
                else:
                    print(f"Asset not found: {self.edit_asset_id}")
                    
        except Exception as e:
            print(f"Error saving asset: {e}")
    
    def start_inline_edit(self, asset_id: str):
        """Start inline editing for a specific asset."""
        # Find the asset in our data
        for asset in self.assets:
            if asset["asset_id"] == asset_id:
                self.editing_asset_id = asset_id
                self.edit_asset_id = asset_id
                self.edit_asset_name = asset.get("asset_name", "")
                self.edit_project = asset.get("project", "")
                self.edit_building = asset.get("building", "")
                self.edit_floor = asset.get("floor", "")
                self.edit_systype = asset.get("systype", "")
                self.edit_os = asset.get("os", "N/A") if asset.get("os") != "N/A" else ""
                self.edit_serial_no = asset.get("serial_no", "N/A") if asset.get("serial_no") != "N/A" else ""
                self.edit_barcode = asset.get("barcode", "N/A") if asset.get("barcode") != "N/A" else ""
                break
    
    def cancel_edit(self):
        """Cancel inline editing."""
        self.editing_asset_id = ""
        self.edit_asset_id = ""
    
    def update_edit_field(self, field: str, value: str):
        """Update a field during inline editing."""
        if field == "asset_name":
            self.edit_asset_name = value
        elif field == "project":
            self.edit_project = value
        elif field == "building":
            self.edit_building = value
        elif field == "floor":
            self.edit_floor = value
        elif field == "systype":
            self.edit_systype = value
        elif field == "os":
            self.edit_os = value
        elif field == "serial_no":
            self.edit_serial_no = value
        elif field == "barcode":
            self.edit_barcode = value
    
    def save_inline_changes(self):
        """Save inline changes to the asset."""
        from sqlmodel import Session, create_engine, select
        from ..models.asset import Asset
        
        try:
            # Get database connection
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                print("Database URL not found")
                return
            
            engine = create_engine(database_url)
            
            with Session(engine) as session:
                # Find the asset
                asset = session.exec(
                    select(Asset).where(Asset.asset_id == int(self.edit_asset_id))
                ).first()
                
                if asset:
                    # Update fields
                    asset.asset_name = self.edit_asset_name
                    
                    # Update IDs based on dropdown selections
                    if self.edit_project and self.edit_project in self.project_map:
                        asset.project_id = int(self.project_map[self.edit_project])
                    
                    if self.edit_building and self.edit_building in self.building_map:
                        asset.building_id = int(self.building_map[self.edit_building])
                    
                    if self.edit_floor and self.floor_map and self.edit_floor in self.floor_map:
                        asset.floor_id = int(self.floor_map[self.edit_floor])
                    
                    if self.edit_systype and self.edit_systype in self.systype_map:
                        asset.systype_id = int(self.systype_map[self.edit_systype])
                    
                    if self.edit_os and self.edit_os in self.os_map:
                        asset.os_id = int(self.os_map[self.edit_os])
                    else:
                        asset.os_id = None
                    
                    # Update optional fields
                    asset.serial_no = self.edit_serial_no if self.edit_serial_no else None
                    asset.letterkenny_barcode = self.edit_barcode if self.edit_barcode else None
                    
                    # Commit changes
                    session.add(asset)
                    session.commit()
                    
                    print(f"Successfully updated asset {asset.asset_name}")
                    
                    # Clear editing state and reload data
                    self.editing_asset_id = ""
                    self.edit_asset_id = ""
                    return self.load_assets_data()
                else:
                    print(f"Asset not found: {self.edit_asset_id}")
                    
        except Exception as e:
            print(f"Error saving asset: {e}")
    
    def open_view_modal(self, asset_id: str):
        """Open view modal for a specific asset."""
        print(f"Opening view modal for asset: {asset_id}")
        # Find the asset in our data
        for asset in self.assets:
            if asset["asset_id"] == asset_id:
                self.view_asset_id = asset_id
                self.view_asset_name = asset.get("asset_name", "Unknown")
                self.view_modal_open = True
                print(f"Modal should be open now for: {self.view_asset_name}")
                # Load recent actions for this asset
                return self.load_recent_actions(asset_id)
        print(f"Asset not found: {asset_id}")
    
    def close_view_modal(self):
        """Close the view modal."""
        self.view_modal_open = False
        self.view_asset_id = ""
        self.recent_actions = []
    
    async def load_recent_actions(self, asset_id: str):
        """Load recent actions for an asset."""
        try:
            with rx.session() as session:
                from ..models.user_activity import UserActivity
                from ..models.employee import Employee
                from sqlmodel import select
                
                # Get recent activities for this asset
                query = (
                    select(UserActivity, Employee)
                    .join(Employee, UserActivity.employee_id == Employee.id)
                    .where(UserActivity.related_asset_id == int(asset_id))
                    .order_by(UserActivity.activity_timestamp.desc())
                    .limit(5)
                )
                
                results = session.exec(query).all()
                
                self.recent_actions = []
                for activity, employee in results:
                    self.recent_actions.append({
                        "action": activity.activity_type,
                        "date": activity.activity_timestamp.strftime("%Y-%m-%d %H:%M") if activity.activity_timestamp else "Unknown",
                        "employee": f"{employee.fname} {employee.lname}",
                        "description": activity.activity_description or "No description"
                    })
                
                # If no activities found, add a placeholder
                if not self.recent_actions:
                    self.recent_actions = [{
                        "action": "No recent actions",
                        "date": "-",
                        "employee": "-",
                        "description": "No activities recorded for this asset yet."
                    }]
                    
        except Exception as e:
            print(f"Error loading recent actions: {e}")
            self.recent_actions = [{
                "action": "Error loading actions",
                "date": "-",
                "employee": "-",
                "description": str(e)
            }]
        
        yield  # Update the UI with the loaded actions
    
    def open_delete_modal(self, asset_id: str):
        """Open delete confirmation modal for a specific asset."""
        print(f"Opening delete modal for asset: {asset_id}")
        # Find the asset in our data
        for asset in self.assets:
            if asset["asset_id"] == asset_id:
                self.delete_asset_id = asset_id
                self.delete_asset_name = asset.get("asset_name", "Unknown")
                self.delete_modal_open = True
                self.delete_confirmation_text = ""  # Reset confirmation text
                print(f"Delete modal should be open now for: {self.delete_asset_name}")
                break
    
    def close_delete_modal(self):
        """Close the delete modal."""
        self.delete_modal_open = False
        self.delete_asset_id = ""
        self.delete_confirmation_text = ""
    
    def set_delete_confirmation_text(self, text: str):
        """Set the delete confirmation text."""
        self.delete_confirmation_text = text
    
    @rx.var
    def delete_confirmation_valid(self) -> bool:
        """Check if the delete confirmation text is valid."""
        expected_text = f"delete {self.delete_asset_name}"
        return self.delete_confirmation_text.lower() == expected_text.lower()
    
    async def submit_delete_request(self):
        """Submit delete request for the asset."""
        if not self.delete_confirmation_valid:
            print("Delete confirmation text does not match")
            return
        
        try:
            with rx.session() as session:
                from ..models.asset import Asset
                from sqlmodel import select
                
                # Find the asset
                asset = session.exec(
                    select(Asset).where(Asset.asset_id == int(self.delete_asset_id))
                ).first()
                
                if asset:
                    # For safety, we'll just mark it as deleted or log the request
                    # In a real system, you might want to soft-delete or require admin approval
                    print(f"Delete request submitted for asset: {asset.asset_name} (ID: {asset.asset_id})")
                    
                    # Log the delete request as an activity
                    from ..models.user_activity import UserActivity
                    from ..models.appuser import AppUser
                    
                    # Get the current user (this is simplified - in real app you'd have auth)
                    # For now, we'll just use the first user
                    user = session.exec(select(AppUser).limit(1)).first()
                    
                    if user:
                        activity = UserActivity(
                            user_id=user.id,
                            employee_id=user.employee_id,
                            activity_type="delete_request",
                            activity_description=f"Requested deletion of asset: {asset.asset_name}",
                            related_asset_id=asset.asset_id,
                            related_project_id=asset.project_id
                        )
                        session.add(activity)
                        session.commit()
                    
                    # Close modal and reload data
                    self.close_delete_modal()
                    yield
                    # Show success message (in real app, you'd have a notification system)
                    print(f"Delete request successfully submitted for: {asset.asset_name}")
                    return
                else:
                    print(f"Asset not found: {self.delete_asset_id}")
                    
        except Exception as e:
            print(f"Error submitting delete request: {e}")
        
        yield