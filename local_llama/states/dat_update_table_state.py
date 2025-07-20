import reflex as rx
from typing import List, Dict, Optional
from sqlmodel import Session, select
from ..models.dat_update import DatUpdate
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.dat_version import DatVersion
from ..models.av_version import AVVersion


class DatUpdateTableState(rx.State):
    """State management for DAT update table display."""
    
    # Table data
    updates: List[Dict[str, str]] = []
    is_loading: bool = False
    total_count: int = 0
    
    # Sorting state
    sort_column: str = "date"
    sort_direction: str = "desc"  # Default to newest first
    
    # Pagination state
    current_page: int = 1
    records_per_page: int = 20
    total_pages: int = 1
    
    @rx.var
    def records_display_text(self) -> str:
        """Generate display text for pagination info."""
        if self.total_count == 0:
            return "No records found"
        
        start = (self.current_page - 1) * self.records_per_page + 1
        end = min(self.current_page * self.records_per_page, self.total_count)
        
        return f"Showing {start}-{end} of {self.total_count} records"
    
    def load_updates(self):
        """Load DAT update records from database."""
        self.is_loading = True
        
        try:
            with rx.session() as session:
                # Get total count first for pagination
                count_query = select(DatUpdate)
                self.total_count = len(session.exec(count_query).all())
                
                # Get the 10 most recent record IDs globally for the neon dot indicator
                recent_ids_query = (
                    select(DatUpdate.datupdate_id)
                    .order_by(DatUpdate.date_of_update.desc())
                    .limit(10)
                )
                recent_results = session.exec(recent_ids_query).all()
                most_recent_ids = {str(record_id) for record_id in recent_results}
                
                # Find duplicate records based on key fields (employee, asset, project, datversion, result)
                from sqlalchemy import func
                duplicate_groups_query = (
                    select(
                        DatUpdate.employee_id,
                        DatUpdate.asset_id,
                        DatUpdate.project_id,
                        DatUpdate.datversion_id,
                        DatUpdate.update_result,
                        func.count(DatUpdate.datupdate_id).label('count')
                    )
                    .group_by(
                        DatUpdate.employee_id,
                        DatUpdate.asset_id,
                        DatUpdate.project_id,
                        DatUpdate.datversion_id,
                        DatUpdate.update_result
                    )
                    .having(func.count(DatUpdate.datupdate_id) > 1)
                )
                duplicate_groups = session.exec(duplicate_groups_query).all()
                
                # Create a set of duplicate record combinations
                duplicate_combinations = set()
                for group in duplicate_groups:
                    duplicate_combinations.add((group.employee_id, group.asset_id, group.project_id, group.datversion_id, group.update_result))
                
                print(f"Found {len(duplicate_combinations)} duplicate combinations")
                
                # Find failed records that haven't been followed by successful ones for the same asset
                failed_without_success = set()
                
                # Get all failed records
                failed_query = (
                    select(DatUpdate.asset_id, DatUpdate.date_of_update, DatUpdate.datupdate_id)
                    .where(DatUpdate.update_result == "Failed")
                    .order_by(DatUpdate.asset_id, DatUpdate.date_of_update.desc())
                )
                failed_records = session.exec(failed_query).all()
                
                for failed_record in failed_records:
                    asset_id, failed_date, failed_id = failed_record
                    
                    # Check if there's a successful record for this asset after the failed date
                    success_after_query = (
                        select(DatUpdate.datupdate_id)
                        .where(
                            DatUpdate.asset_id == asset_id,
                            DatUpdate.update_result == "Success",
                            DatUpdate.date_of_update > failed_date
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
                        DatUpdate,
                        Employee.first_name,
                        Employee.last_name,
                        Asset.asset_name,
                        Project.project_name,
                        DatVersion.datversion_name,
                        AVVersion.av_version
                    )
                    .join(Employee, DatUpdate.employee_id == Employee.id)
                    .join(Asset, DatUpdate.asset_id == Asset.asset_id)
                    .join(Project, DatUpdate.project_id == Project.project_id)
                    .join(DatVersion, DatUpdate.datversion_id == DatVersion.datversion_id)
                    .join(AVVersion, DatVersion.avversion_id == AVVersion.avversion_id)
                )
                
                # Apply sorting (MSSQL requires ORDER BY for OFFSET/LIMIT)
                if self.sort_column == "date":
                    if self.sort_direction == "asc":
                        query = query.order_by(DatUpdate.date_of_update.asc())
                    else:
                        query = query.order_by(DatUpdate.date_of_update.desc())
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
                elif self.sort_column == "datversion":
                    if self.sort_direction == "asc":
                        query = query.order_by(DatVersion.datversion_name.asc())
                    else:
                        query = query.order_by(DatVersion.datversion_name.desc())
                elif self.sort_column == "result":
                    if self.sort_direction == "asc":
                        query = query.order_by(DatUpdate.update_result.asc())
                    else:
                        query = query.order_by(DatUpdate.update_result.desc())
                else:
                    # Default to date descending - ALWAYS provide an ORDER BY
                    query = query.order_by(DatUpdate.date_of_update.desc())
                
                # Apply pagination
                query = query.offset(offset).limit(self.records_per_page)
                
                results = session.exec(query).all()
                print(f"Query returned {len(results)} results")
                
                # Format data for table display
                updates_data = []
                for result in results:
                    update, emp_first, emp_last, asset_name, project_name, dat_version, av_version = result
                    
                    # Format date
                    date_str = update.date_of_update.strftime("%Y-%m-%d %H:%M") if update.date_of_update else "N/A"
                    
                    # Format employee name
                    employee_name = f"{emp_last}, {emp_first}" if emp_last and emp_first else "Unknown"
                    
                    # Format DAT version with AV version
                    version_str = f"{dat_version} (AV: {av_version})" if dat_version and av_version else "Unknown"
                    
                    # Format comments (truncate if too long)
                    comments = update.update_comments or ""
                    if len(comments) > 50:
                        comments = comments[:47] + "..."
                    
                    # Check if this record is a duplicate
                    record_combination = (
                        update.employee_id,
                        update.asset_id,
                        update.project_id,
                        update.datversion_id,
                        update.update_result
                    )
                    is_duplicate = record_combination in duplicate_combinations
                    
                    updates_data.append({
                        "id": str(update.datupdate_id),
                        "date": date_str,
                        "date_sort": update.date_of_update.isoformat() if update.date_of_update else "",
                        "employee": employee_name,
                        "asset": asset_name or "Unknown",
                        "project": project_name or "Unknown", 
                        "datversion": version_str,
                        "datfile": update.datfile_name or "Unknown",
                        "result": update.update_result or "Unknown",
                        "comments": comments,
                        "is_recent": str(update.datupdate_id) in most_recent_ids,
                        "is_duplicate": is_duplicate,
                        "is_unresolved_failure": update.datupdate_id in failed_without_success
                    })
                
                # Updates data is already sorted by the database query
                self.updates = updates_data
                
        except Exception as e:
            print(f"Error loading DAT updates: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            self.updates = []
            self.total_count = 0
            
        finally:
            self.is_loading = False
    
    def sort_by_column(self, column: str):
        """Sort by the specified column."""
        if self.sort_column == column:
            # Toggle direction if same column
            self.sort_direction = "asc" if self.sort_direction == "desc" else "desc"
        else:
            # New column, default to ascending
            self.sort_column = column
            self.sort_direction = "asc"
        
        # Reset to first page and reload
        self.current_page = 1
        self.load_updates()
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_updates()
    
    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_updates()
    
    def first_page(self):
        """Go to first page."""
        self.current_page = 1
        self.load_updates()
    
    def last_page(self):
        """Go to last page."""
        self.current_page = self.total_pages
        self.load_updates()