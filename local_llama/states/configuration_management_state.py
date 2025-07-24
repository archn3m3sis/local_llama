"""State management for Configuration Management page."""
import reflex as rx
import os
from typing import List, Dict, Optional
from sqlmodel import Session, select, func, and_, or_, create_engine
from ..models import (
    SoftwareCatalog, AssetSoftware, Asset, Project, 
    SWManufacturer, SoftwareVersion, Department
)


class ConfigurationManagementState(rx.State):
    """State for the Configuration Management page."""
    
    # View mode: catalog shows all software, asset shows software for selected assets
    view_mode: str = "catalog"
    
    # Selection states
    selected_project: str = "All Projects"
    selected_asset: str = ""
    available_projects: List[str] = []
    available_assets: List[str] = []
    
    @rx.var
    def project_options(self) -> List[str]:
        """Return project options including 'All Projects'."""
        return ["All Projects"] + self.available_projects
    
    @rx.var
    def has_software(self) -> bool:
        """Check if there is any software to display."""
        return len(self.filtered_software) > 0
    
    @rx.var
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.filtered_software_count == 0:
            return 1
        return (self.filtered_software_count + self.items_per_page - 1) // self.items_per_page
    
    @rx.var
    def paginated_software(self) -> List[Dict]:
        """Get current page of software after sorting."""
        # Sort the filtered software
        sorted_software = sorted(
            self.filtered_software,
            key=lambda x: x.get(self.sort_column, ""),
            reverse=not self.sort_ascending
        )
        
        # Calculate pagination
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        
        return sorted_software[start_idx:end_idx]
    
    @rx.var
    def page_info(self) -> str:
        """Get pagination info text."""
        if self.filtered_software_count == 0:
            return "No items"
        
        start = (self.current_page - 1) * self.items_per_page + 1
        end = min(self.current_page * self.items_per_page, self.filtered_software_count)
        return f"Showing {start}-{end} of {self.filtered_software_count} items"
    
    # Search states
    asset_search: str = ""
    software_search: str = ""
    filtered_assets: List[str] = []
    
    # Software data
    filtered_software: List[Dict] = []
    _all_software: List[Dict] = []  # Store unfiltered software list
    total_software: int = 0
    filtered_software_count: int = 0
    
    # Pagination
    current_page: int = 1
    items_per_page: int = 20
    sort_column: str = "name"
    sort_ascending: bool = True
    
    # Version history
    selected_software: str = ""
    version_history: List[Dict] = []
    
    def on_mount(self):
        """Initialize the state when the page loads."""
        self.load_projects()
        self.load_software_catalog()
    
    def load_projects(self):
        """Load all available projects."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            projects = session.exec(select(Project)).all()
            self.available_projects = [p.project_name for p in projects]
    
    def load_assets_for_project(self):
        """Load assets for the selected project."""
        if self.selected_project == "All Projects":
            self.available_assets = []
            self.filtered_assets = []
            return
            
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Get project ID
            project = session.exec(
                select(Project).where(Project.project_name == self.selected_project)
            ).first()
            
            if project:
                # Get all assets for this project
                assets = session.exec(
                    select(Asset).where(Asset.project_id == project.project_id)
                ).all()
                self.available_assets = [a.asset_name for a in assets]
                self.filter_assets()
    
    def filter_assets(self):
        """Filter assets based on search term."""
        if not self.asset_search:
            self.filtered_assets = self.available_assets
        else:
            search_lower = self.asset_search.lower()
            self.filtered_assets = [
                asset for asset in self.available_assets 
                if search_lower in asset.lower()
            ]
    
    def set_selected_project(self, project: str):
        """Set the selected project and reload assets."""
        self.selected_project = project
        self.selected_asset = ""
        self.load_assets_for_project()
        if self.view_mode == "asset":
            self.load_software_for_selection()
    
    def set_selected_asset(self, asset: str):
        """Set the selected asset."""
        self.selected_asset = asset
        if self.view_mode == "asset":
            self.load_software_for_selection()
    
    def set_asset_search(self, search: str):
        """Update asset search and filter results."""
        self.asset_search = search
        self.filter_assets()
    
    def set_software_search(self, search: str):
        """Update software search and filter results."""
        self.software_search = search
        self.filter_software()
    
    def set_view_mode(self, mode: str):
        """Switch between catalog and asset view modes."""
        self.view_mode = mode
        if mode == "catalog":
            self.load_software_catalog()
        else:
            self.load_software_for_selection()
    
    def set_catalog_view(self):
        """Set view mode to catalog."""
        self.set_view_mode("catalog")
    
    def set_asset_view(self):
        """Set view mode to asset."""
        self.set_view_mode("asset")
    
    def load_software_catalog(self):
        """Load the entire software catalog."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Get total count
            self.total_software = session.exec(
                select(func.count(SoftwareCatalog.software_catalog_id))
            ).one()
            
            # Get all software with vendor info
            query = select(
                SoftwareCatalog,
                SWManufacturer.swmanu_name,
                func.count(AssetSoftware.asset_id).label("install_count")
            ).outerjoin(
                SWManufacturer, 
                SoftwareCatalog.sw_vendor == SWManufacturer.swmanu_id
            ).outerjoin(
                AssetSoftware,
                SoftwareCatalog.software_catalog_id == AssetSoftware.software_catalog_id
            ).group_by(
                SoftwareCatalog.software_catalog_id,
                SoftwareCatalog.sw_name,
                SoftwareCatalog.sw_vendor,
                SoftwareCatalog.sw_category,
                SoftwareCatalog.sw_type,
                SoftwareCatalog.latest_version,
                SoftwareCatalog.sw_architecture_compatibility,
                SoftwareCatalog.dod_compliant,
                SoftwareCatalog.is_approved,
                SoftwareCatalog.is_licensed,
                SoftwareCatalog.license_model,
                SoftwareCatalog.eol_date,
                SoftwareCatalog.description,
                SoftwareCatalog.created_date,
                SoftwareCatalog.updated_date,
                SWManufacturer.swmanu_name
            )
            
            results = session.exec(query).all()
            
            software_list = [
                {
                    "name": sw.sw_name,
                    "vendor": vendor or "Unknown",
                    "category": sw.sw_category or "Uncategorized",
                    "latest_version": sw.latest_version or "Unknown",
                    "architecture": sw.sw_architecture_compatibility or "Any",
                    "dod_compliant": sw.dod_compliant,
                    "installations": install_count
                }
                for sw, vendor, install_count in results
            ]
            
            self._all_software = software_list
            self.filtered_software = software_list
            self.filtered_software_count = len(software_list)
    
    def load_software_for_selection(self):
        """Load software for selected project or asset."""
        if self.selected_project == "All Projects":
            self._all_software = []
            self.filtered_software = []
            self.filtered_software_count = 0
            return
            
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            if self.selected_asset:
                # Get software for specific asset
                asset = session.exec(
                    select(Asset).where(Asset.asset_name == self.selected_asset)
                ).first()
                
                if asset:
                    query = select(
                        SoftwareCatalog,
                        SWManufacturer.swmanu_name,
                        AssetSoftware.installed_version
                    ).join(
                        AssetSoftware,
                        SoftwareCatalog.software_catalog_id == AssetSoftware.software_catalog_id
                    ).outerjoin(
                        SWManufacturer,
                        SoftwareCatalog.sw_vendor == SWManufacturer.swmanu_id
                    ).where(
                        AssetSoftware.asset_id == asset.asset_id
                    )
                    
                    results = session.exec(query).all()
                    
                    software_list = [
                        {
                            "name": sw.sw_name,
                            "vendor": vendor or "Unknown",
                            "category": sw.sw_category or "Uncategorized",
                            "latest_version": version or sw.latest_version or "Unknown",
                            "architecture": sw.sw_architecture_compatibility or "Any",
                            "dod_compliant": sw.dod_compliant,
                            "installations": 1
                        }
                        for sw, vendor, version in results
                    ]
                    
                    self._all_software = software_list
                    self.filtered_software = software_list
            else:
                # Get aggregated software for entire project
                project = session.exec(
                    select(Project).where(Project.project_name == self.selected_project)
                ).first()
                
                if project:
                    # Get all unique software for assets in this project
                    query = select(
                        SoftwareCatalog,
                        SWManufacturer.swmanu_name,
                        func.count(func.distinct(AssetSoftware.asset_id)).label("install_count")
                    ).join(
                        AssetSoftware,
                        SoftwareCatalog.software_catalog_id == AssetSoftware.software_catalog_id
                    ).join(
                        Asset,
                        AssetSoftware.asset_id == Asset.asset_id
                    ).outerjoin(
                        SWManufacturer,
                        SoftwareCatalog.sw_vendor == SWManufacturer.swmanu_id
                    ).where(
                        Asset.project_id == project.project_id
                    ).group_by(
                        SoftwareCatalog.software_catalog_id,
                        SoftwareCatalog.sw_name,
                        SoftwareCatalog.sw_vendor,
                        SoftwareCatalog.sw_category,
                        SoftwareCatalog.sw_type,
                        SoftwareCatalog.latest_version,
                        SoftwareCatalog.sw_architecture_compatibility,
                        SoftwareCatalog.dod_compliant,
                        SoftwareCatalog.is_approved,
                        SoftwareCatalog.is_licensed,
                        SoftwareCatalog.license_model,
                        SoftwareCatalog.eol_date,
                        SoftwareCatalog.description,
                        SoftwareCatalog.created_date,
                        SoftwareCatalog.updated_date,
                        SWManufacturer.swmanu_name
                    )
                    
                    results = session.exec(query).all()
                    
                    software_list = [
                        {
                            "name": sw.sw_name,
                            "vendor": vendor or "Unknown",
                            "category": sw.sw_category or "Uncategorized",
                            "latest_version": sw.latest_version or "Unknown",
                            "architecture": sw.sw_architecture_compatibility or "Any",
                            "dod_compliant": sw.dod_compliant,
                            "installations": install_count
                        }
                        for sw, vendor, install_count in results
                    ]
                    
                    self._all_software = software_list
                    self.filtered_software = software_list
                    self.filtered_software_count = len(software_list)
    
    def filter_software(self):
        """Filter software based on search term."""
        if not self.software_search:
            # Show all software when no search term
            self.filtered_software = self._all_software.copy()
            self.filtered_software_count = len(self.filtered_software)
            return
        
        search_lower = self.software_search.lower()
        filtered = []
        
        for sw in self._all_software:
            if (search_lower in sw["name"].lower() or
                search_lower in sw["vendor"].lower() or
                search_lower in sw["category"].lower()):
                filtered.append(sw)
        
        self.filtered_software = filtered
        self.filtered_software_count = len(filtered)
        # Reset to first page when filtering
        self.current_page = 1
    
    def select_software(self, software_name: str):
        """Select a software item and load its version history."""
        self.selected_software = software_name
        self.load_version_history()
    
    def set_page(self, page: int):
        """Set current page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
    
    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
    
    def sort_by_column(self, column: str):
        """Sort by specified column."""
        if self.sort_column == column:
            # Toggle sort direction if clicking same column
            self.sort_ascending = not self.sort_ascending
        else:
            # New column, default to ascending
            self.sort_column = column
            self.sort_ascending = True
        # Reset to first page when sorting changes
        self.current_page = 1
    
    def sort_by_name(self):
        """Sort by name column."""
        self.sort_by_column("name")
    
    def sort_by_vendor(self):
        """Sort by vendor column."""
        self.sort_by_column("vendor")
    
    def sort_by_category(self):
        """Sort by category column."""
        self.sort_by_column("category")
    
    def load_version_history(self):
        """Load version history for selected software."""
        if not self.selected_software:
            self.version_history = []
            return
            
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Get the software catalog entry
            software = session.exec(
                select(SoftwareCatalog).where(
                    SoftwareCatalog.sw_name == self.selected_software
                )
            ).first()
            
            if software:
                # Get all versions from SoftwareVersion table
                versions = session.exec(
                    select(SoftwareVersion).where(
                        SoftwareVersion.software_catalog_id == software.software_catalog_id
                    ).order_by(SoftwareVersion.release_date.desc())
                ).all()
                
                if versions:
                    # Use actual version data
                    self.version_history = []
                    for v in versions:
                        # Count installations of this version
                        install_count = session.exec(
                            select(func.count(AssetSoftware.asset_id)).where(
                                and_(
                                    AssetSoftware.software_catalog_id == software.software_catalog_id,
                                    AssetSoftware.installed_version == v.version_number
                                )
                            )
                        ).one()
                        
                        self.version_history.append({
                            "version": v.version_number,
                            "release_date": v.release_date.strftime("%Y-%m-%d") if v.release_date else "Unknown",
                            "is_latest": v.version_number == software.latest_version,
                            "installations": install_count
                        })
                else:
                    # Create mock version history if no versions exist
                    self.version_history = [
                        {
                            "version": software.latest_version or "1.0.0",
                            "release_date": "Current",
                            "is_latest": True,
                            "installations": session.exec(
                                select(func.count(AssetSoftware.asset_id)).where(
                                    AssetSoftware.software_catalog_id == software.software_catalog_id
                                )
                            ).one()
                        }
                    ]