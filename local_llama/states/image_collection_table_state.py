import reflex as rx
from typing import List, Dict, Optional
from sqlmodel import Session, select
from ..models.image_collection import ImageCollection
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.imaging_method import ImagingMethod


class ImageCollectionTableState(rx.State):
    """State management for image collection table display."""
    
    # Table data
    collections: List[Dict[str, str]] = []
    is_loading: bool = False
    total_count: int = 0
    
    # Sorting state
    sort_column: str = "date"
    sort_direction: str = "desc"  # "asc" or "desc"
    
    # Pagination state
    current_page: int = 1
    records_per_page: int = 20
    total_pages: int = 1
    
    @rx.var
    def records_display_text(self) -> str:
        """Generate display text for record count."""
        if self.total_count == 0:
            return "No records found"
        
        start = ((self.current_page - 1) * self.records_per_page) + 1
        end = min(self.current_page * self.records_per_page, self.total_count)
        return f"Showing {start} - {end} of {self.total_count} records"
    
    def load_collections(self):
        """Load image collection records from database."""
        self.is_loading = True
        
        try:
            with rx.session() as session:
                # Get total count first for pagination
                count_query = select(ImageCollection)
                self.total_count = len(session.exec(count_query).all())
                
                # Get the 10 most recent record IDs globally for the neon dot indicator
                recent_ids_query = (
                    select(ImageCollection.imgcollection_id)
                    .order_by(ImageCollection.imgcollection_date.desc())
                    .limit(10)
                )
                recent_results = session.exec(recent_ids_query).all()
                most_recent_ids = {str(record_id) for record_id in recent_results}
                
                # Find duplicate records based on key fields (employee, asset, project, method, result)
                from sqlalchemy import func
                duplicate_groups_query = (
                    select(
                        ImageCollection.employee_id,
                        ImageCollection.asset_id,
                        ImageCollection.project_id,
                        ImageCollection.imgmethod_id,
                        ImageCollection.imaging_result,
                        func.count(ImageCollection.imgcollection_id).label('count')
                    )
                    .group_by(
                        ImageCollection.employee_id,
                        ImageCollection.asset_id,
                        ImageCollection.project_id,
                        ImageCollection.imgmethod_id,
                        ImageCollection.imaging_result
                    )
                    .having(func.count(ImageCollection.imgcollection_id) > 1)
                )
                duplicate_groups = session.exec(duplicate_groups_query).all()
                
                # Create a set of duplicate record combinations
                duplicate_combinations = set()
                for group in duplicate_groups:
                    duplicate_combinations.add((group.employee_id, group.asset_id, group.project_id, group.imgmethod_id, group.imaging_result))
                
                print(f"Found {len(duplicate_combinations)} duplicate combinations")
                
                # Find failed records that haven't been followed by successful ones for the same asset
                failed_without_success = set()
                
                # Get all failed records
                failed_query = (
                    select(ImageCollection.asset_id, ImageCollection.imgcollection_date, ImageCollection.imgcollection_id)
                    .where(ImageCollection.imaging_result == "Failed")
                    .order_by(ImageCollection.asset_id, ImageCollection.imgcollection_date.desc())
                )
                failed_records = session.exec(failed_query).all()
                
                for failed_record in failed_records:
                    asset_id, failed_date, failed_id = failed_record
                    
                    # Check if there's a successful record for this asset after the failed date
                    success_after_query = (
                        select(ImageCollection.imgcollection_id)
                        .where(
                            ImageCollection.asset_id == asset_id,
                            ImageCollection.imaging_result == "Success",
                            ImageCollection.imgcollection_date > failed_date
                        )
                        .limit(1)
                    )
                    success_after = session.exec(success_after_query).first()
                    
                    # If no success found after this failure, mark it as unresolved
                    if not success_after:
                        failed_without_success.add(failed_id)
                
                print(f"Found {len(failed_without_success)} unresolved failed records")
                
                # Calculate total pages
                import math
                self.total_pages = max(1, math.ceil(self.total_count / self.records_per_page))
                
                # Ensure current page is within valid range
                if self.current_page > self.total_pages:
                    self.current_page = max(1, self.total_pages)
                
                # Calculate offset for pagination
                offset = (self.current_page - 1) * self.records_per_page
                
                # Build query with sorting
                query = (
                    select(
                        ImageCollection,
                        Employee.first_name,
                        Employee.last_name,
                        Asset.asset_name,
                        Project.project_name,
                        ImagingMethod.img_method
                    )
                    .join(Employee, ImageCollection.employee_id == Employee.id)
                    .join(Asset, ImageCollection.asset_id == Asset.asset_id)
                    .join(Project, ImageCollection.project_id == Project.project_id)
                    .join(ImagingMethod, ImageCollection.imgmethod_id == ImagingMethod.imgmethod_id)
                )
                
                # Apply sorting (MSSQL requires ORDER BY for OFFSET/LIMIT)
                if self.sort_column == "date":
                    if self.sort_direction == "asc":
                        query = query.order_by(ImageCollection.imgcollection_date.asc())
                    else:
                        query = query.order_by(ImageCollection.imgcollection_date.desc())
                elif self.sort_column == "employee":
                    if self.sort_direction == "asc":
                        query = query.order_by(Employee.last_name.asc(), Employee.first_name.asc())
                    else:
                        query = query.order_by(Employee.last_name.desc(), Employee.first_name.desc())
                elif self.sort_column == "asset":
                    if self.sort_direction == "asc":
                        query = query.order_by(Asset.asset_name.asc())
                    else:
                        query = query.order_by(Asset.asset_name.desc())
                elif self.sort_column == "project":
                    if self.sort_direction == "asc":
                        query = query.order_by(Project.project_name.asc())
                    else:
                        query = query.order_by(Project.project_name.desc())
                elif self.sort_column == "method":
                    if self.sort_direction == "asc":
                        query = query.order_by(ImagingMethod.img_method.asc())
                    else:
                        query = query.order_by(ImagingMethod.img_method.desc())
                elif self.sort_column == "size":
                    if self.sort_direction == "asc":
                        query = query.order_by(ImageCollection.img_size_mb.asc())
                    else:
                        query = query.order_by(ImageCollection.img_size_mb.desc())
                elif self.sort_column == "result":
                    if self.sort_direction == "asc":
                        query = query.order_by(ImageCollection.imaging_result.asc())
                    else:
                        query = query.order_by(ImageCollection.imaging_result.desc())
                else:
                    # Default to date descending - ALWAYS provide an ORDER BY
                    query = query.order_by(ImageCollection.imgcollection_date.desc())
                
                # Apply pagination
                query = query.offset(offset).limit(self.records_per_page)
                
                results = session.exec(query).all()
                print(f"Query returned {len(results)} results")
                
                # Format data for table display
                collections_data = []
                for result in results:
                    collection, emp_first, emp_last, asset_name, project_name, img_method = result
                    
                    # Format date
                    date_str = collection.imgcollection_date.strftime("%Y-%m-%d %H:%M") if collection.imgcollection_date else "N/A"
                    
                    # Format employee name
                    employee_name = f"{emp_last}, {emp_first}" if emp_last and emp_first else "Unknown"
                    
                    # Format image size
                    size_str = f"{collection.img_size_mb:.1f} MB" if collection.img_size_mb else "N/A"
                    
                    # Format comments (truncate if too long)
                    comments = collection.imaging_comments or ""
                    if len(comments) > 50:
                        comments = comments[:47] + "..."
                    
                    # Check if this record is a duplicate
                    record_combination = (
                        collection.employee_id,
                        collection.asset_id,
                        collection.project_id,
                        collection.imgmethod_id,
                        collection.imaging_result
                    )
                    is_duplicate = record_combination in duplicate_combinations
                    
                    collections_data.append({
                        "id": str(collection.imgcollection_id),
                        "date": date_str,
                        "date_sort": collection.imgcollection_date.isoformat() if collection.imgcollection_date else "",
                        "employee": employee_name,
                        "asset": asset_name or "Unknown",
                        "project": project_name or "Unknown", 
                        "method": img_method or "Unknown",
                        "size": size_str,
                        "result": collection.imaging_result or "Unknown",
                        "comments": comments,
                        "is_recent": str(collection.imgcollection_id) in most_recent_ids,
                        "is_duplicate": is_duplicate,
                        "is_unresolved_failure": collection.imgcollection_id in failed_without_success
                    })
                
                # Collections data is already sorted by the database query
                self.collections = collections_data
                
        except Exception as e:
            print(f"Error loading image collections: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            self.collections = []
            self.total_count = 0
            
        finally:
            self.is_loading = False
    
    def _sort_collections(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Sort collections data based on current sort settings."""
        if not data:
            return data
        
        reverse = self.sort_direction == "desc"
        
        # Use appropriate sort key based on column
        if self.sort_column == "date":
            return sorted(data, key=lambda x: x.get("date_sort", ""), reverse=reverse)
        else:
            return sorted(data, key=lambda x: x.get(self.sort_column, ""), reverse=reverse)
    
    def sort_by_column(self, column: str):
        """Handle column header click for sorting."""
        if self.sort_column == column:
            # Toggle direction if same column
            self.sort_direction = "asc" if self.sort_direction == "desc" else "desc"
        else:
            # New column, default to ascending
            self.sort_column = column
            self.sort_direction = "asc"
        
        # Reload data with new sorting
        self.load_collections()
    
    def go_to_page(self, page: int):
        """Navigate to a specific page."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.load_collections()
    
    def next_page(self):
        """Navigate to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_collections()
    
    def previous_page(self):
        """Navigate to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_collections()
    
    def first_page(self):
        """Navigate to first page."""
        self.current_page = 1
        self.load_collections()
    
    def last_page(self):
        """Navigate to last page."""
        self.current_page = self.total_pages
        self.load_collections()