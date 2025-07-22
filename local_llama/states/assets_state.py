"""State management for Assets page."""
import reflex as rx
from sqlmodel import select, func, or_, and_
from typing import List, Dict, Any
from datetime import datetime
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
    
    # Mappings from display string to database ID (str since some are "all")
    project_map: Dict[str, str] = {}
    building_map: Dict[str, str] = {}
    systype_map: Dict[str, str] = {}
    os_map: Dict[str, str] = {}
    
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
                self.project_map = {"All Projects": "all"}
                projects = session.exec(select(Project).order_by(Project.project_name)).all()
                for p in projects:
                    self.projects.append(p.project_name)
                    self.project_map[p.project_name] = str(p.project_id)
                
                # Buildings
                self.buildings = ["All Buildings"]
                self.building_map = {"All Buildings": "all"}
                buildings = session.exec(select(Building).order_by(Building.building_name)).all()
                for b in buildings:
                    self.buildings.append(b.building_name)
                    self.building_map[b.building_name] = str(b.building_id)
                
                # System Types
                self.systypes = ["All System Types"]
                self.systype_map = {"All System Types": "all"}
                systypes = session.exec(select(SysType).order_by(SysType.systype_name)).all()
                for s in systypes:
                    self.systypes.append(s.systype_name)
                    self.systype_map[s.systype_name] = str(s.systype_id)
                
                # Operating Systems
                self.operating_systems = ["All Operating Systems"]
                self.os_map = {"All Operating Systems": "all"}
                oses = session.exec(select(OperatingSystem).order_by(OperatingSystem.os_name)).all()
                for os in oses:
                    self.operating_systems.append(os.os_name)
                    self.os_map[os.os_name] = str(os.os_id)
                
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
                
                # Apply pagination
                offset = (self.page - 1) * self.page_size
                query = query.offset(offset).limit(self.page_size)
                
                # Execute query
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
                    
                    self.assets.append({
                        "asset_id": str(asset.asset_id),
                        "asset_name": asset.asset_name or "Unknown",
                        "project": project.project_name if project else "Unknown",
                        "project_id": asset.project_id,
                        "building": building.building_name if building else "Unknown",
                        "building_id": asset.building_id,
                        "floor": floor.floor_name if floor else "Unknown",
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
            
            # By OS
            os = asset.get("os", "N/A")
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