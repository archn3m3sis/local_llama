import reflex as rx
import os
import hashlib
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
import base64
from sqlmodel import Session, create_engine, select
from ..models.file_storage import FileMetadata, FileContent, FileType, StorageLocation


class FileStorageState(rx.State):
    """State management for file storage operations."""
    
    # Configuration
    FILE_STORAGE_PATH: str = "./uploads"  # Base path for file storage
    MAX_DB_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB limit for database storage
    
    # State variables
    upload_progress: int = 0
    uploading: bool = False
    error_message: str = ""
    files: List[Dict] = []
    loading_files: bool = False
    file_to_delete: Optional[int] = None
    file_to_download: Optional[int] = None
    auto_refresh_enabled: bool = True
    refresh_interval: int = 5000  # 5 seconds
    is_dragging: bool = False
    upload_success: bool = False
    current_upload_filename: str = ""
    current_file_size_display: str = ""
    upload_status: str = "Preparing..."
    current_directory_id: Optional[int] = None
    current_directory_path: str = "/playbook"
    
    def _get_file_type(self, filename: str) -> FileType:
        """Determine file type from extension."""
        ext = filename.lower().split('.')[-1]
        type_map = {
            'md': FileType.MARKDOWN,
            'txt': FileType.TEXT,
            'pdf': FileType.PDF,
            'svg': FileType.SVG,
            'png': FileType.PNG,
            'jpg': FileType.JPEG,
            'jpeg': FileType.JPEG,
        }
        return type_map.get(ext, FileType.OTHER)
    
    def _calculate_checksum(self, content: bytes) -> str:
        """Calculate SHA-256 checksum of file content."""
        return hashlib.sha256(content).hexdigest()
    
    def _determine_storage_location(self, file_size: int, file_type: FileType) -> StorageLocation:
        """Determine optimal storage location based on file size and type."""
        # Small critical files go to database
        if file_size <= self.MAX_DB_FILE_SIZE and file_type in [FileType.MARKDOWN, FileType.TEXT]:
            return StorageLocation.DATABASE
        return StorageLocation.FILESYSTEM
    
    async def upload_file(self, files):
        """Handle file upload."""
        if not files:
            return
        
        self.uploading = True
        self.error_message = ""
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.error_message = "Database connection not configured"
            self.uploading = False
            return
        
        engine = create_engine(database_url)
        
        total_files = len(files)
        for idx, file in enumerate(files):
            try:
                # Reset progress for each file
                self.upload_progress = 0
                self.upload_status = f"Uploading {idx + 1} of {total_files}..."
                
                # Check if we received a dictionary with file data
                if isinstance(file, dict):
                    upload_data = file.get('content', b'')
                    filename = file.get('name', f"upload_{datetime.now().timestamp()}")
                    if isinstance(upload_data, str):
                        upload_data = upload_data.encode()
                # Check if file is already bytes
                elif isinstance(file, bytes):
                    upload_data = file
                    filename = f"upload_{datetime.now().timestamp()}"
                # Otherwise try to read it
                else:
                    # Try to get filename first
                    filename = None
                    if hasattr(file, 'filename'):
                        filename = file.filename
                    elif hasattr(file, 'name'):
                        filename = file.name
                    elif hasattr(file, 'file') and hasattr(file.file, 'name'):
                        filename = file.file.name
                    
                    if not filename:
                        filename = f"upload_{datetime.now().timestamp()}"
                    
                    # Read file content
                    if hasattr(file, 'read'):
                        upload_data = await file.read()
                    else:
                        continue
                
                file_size = len(upload_data)
                
                # Update current file info
                self.current_upload_filename = filename
                self.current_file_size_display = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"
                
                # Simulate progress updates
                self.upload_progress = 20
                yield
                
                # Determine file properties
                file_type = self._get_file_type(filename)
                mime_type = getattr(file, 'content_type', None) or "application/octet-stream"
                
                self.upload_progress = 40
                self.upload_status = "Processing file..."
                yield
                
                checksum = self._calculate_checksum(upload_data)
                storage_location = self._determine_storage_location(file_size, file_type)
                
                self.upload_progress = 60
                self.upload_status = "Saving to storage..."
                yield
                
                with Session(engine) as session:
                    # Create metadata entry
                    metadata = FileMetadata(
                        filename=f"{datetime.now().timestamp()}_{filename}",
                        original_filename=filename,
                        file_type=file_type,
                        mime_type=mime_type,
                        file_size=file_size,
                        storage_location=storage_location,
                        checksum=checksum,
                        uploaded_by=1,  # TODO: Get from current user
                        directory_id=self.current_directory_id,  # Store in current directory
                    )
                    
                    if storage_location == StorageLocation.DATABASE:
                        # Store in database
                        session.add(metadata)
                        session.flush()  # Get the file_id
                        
                        file_content = FileContent(
                            file_id=metadata.file_id,
                            content=upload_data
                        )
                        session.add(file_content)
                    else:
                        # Store in filesystem
                        Path(self.FILE_STORAGE_PATH).mkdir(parents=True, exist_ok=True)
                        file_path = os.path.join(
                            self.FILE_STORAGE_PATH,
                            f"{datetime.now().timestamp()}_{filename}"
                        )
                        
                        with open(file_path, "wb") as f:
                            f.write(upload_data)
                        
                        metadata.file_path = file_path
                        session.add(metadata)
                    
                    session.commit()
                    
                    self.upload_progress = 90
                    self.upload_status = "Finalizing..."
                    yield
                    
            except Exception as e:
                self.error_message = f"Upload failed: {str(e)}"
                self.uploading = False
                return
        
        self.upload_progress = 100
        self.upload_status = "Upload complete!"
        yield
        
        # Small delay to show completion
        yield rx.call_script("await new Promise(r => setTimeout(r, 500))")
        
        self.uploading = False
        self.upload_success = True
        # Reload the file list
        self.load_files()
        
        # Reset after showing success
        yield rx.call_script("await new Promise(r => setTimeout(r, 2000))")
        self.upload_success = False
        self.upload_progress = 0
        self.current_upload_filename = ""
        self.upload_status = "Preparing..."
    
    def get_file_url(self, file_id: int) -> Optional[str]:
        """Get URL or base64 data for file display."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return None
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            metadata = session.get(FileMetadata, file_id)
            if not metadata:
                return None
            
            if metadata.storage_location == StorageLocation.DATABASE:
                # Get from database
                file_content = session.exec(
                    select(FileContent).where(FileContent.file_id == file_id)
                ).first()
                
                if file_content:
                    # Return as base64 data URL
                    b64_content = base64.b64encode(file_content.content).decode()
                    return f"data:{metadata.mime_type};base64,{b64_content}"
            else:
                # For filesystem, return the file path (you'd implement serving logic)
                return f"/api/files/{file_id}"
        
        return None
    
    def set_current_directory_from_tree(self, directory_id: int, directory_path: str = None):
        """Set current directory from tree click and reload files."""
        self.current_directory_id = directory_id
        if directory_path:
            self.current_directory_path = directory_path
        self.load_files()
    
    def load_files(self):
        """Load all files for display in current directory."""
        self.loading_files = True
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.loading_files = False
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Filter by current directory
            query = select(FileMetadata)
            if self.current_directory_id:
                query = query.where(FileMetadata.directory_id == self.current_directory_id)
            else:
                # Show files without directory (root level)
                query = query.where(FileMetadata.directory_id == None)
            
            files = session.exec(query.order_by(FileMetadata.uploaded_at.desc())).all()
            
            self.files = [
                {
                    "file_id": f.file_id,
                    "original_filename": f.original_filename,
                    "file_type": f.file_type.value,
                    "file_size": f.file_size,
                    "file_size_kb": f"{f.file_size / 1024:.1f}",
                    "uploaded_at": f.uploaded_at.strftime("%Y-%m-%d %H:%M"),
                    "storage_location": f.storage_location.value,
                    "is_public": f.is_public,
                    "directory_id": f.directory_id,
                }
                for f in files
            ]
        
        self.loading_files = False
    
    def delete_file(self, file_id: int):
        """Delete a file from storage."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.error_message = "Database connection not configured"
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            metadata = session.get(FileMetadata, file_id)
            if not metadata:
                self.error_message = "File not found"
                return
            
            # Delete physical file if stored in filesystem
            if metadata.storage_location == StorageLocation.FILESYSTEM and metadata.file_path:
                try:
                    if os.path.exists(metadata.file_path):
                        os.remove(metadata.file_path)
                except Exception as e:
                    print(f"Error deleting physical file: {e}")
            
            # Delete database records
            if metadata.storage_location == StorageLocation.DATABASE:
                file_content = session.exec(
                    select(FileContent).where(FileContent.file_id == file_id)
                ).first()
                if file_content:
                    session.delete(file_content)
            
            session.delete(metadata)
            session.commit()
        
        # Reload files
        self.load_files()
    
    def handle_delete_file(self, file_id: int):
        """Wrapper for delete file to handle from UI."""
        return self.delete_file(file_id)
    
    async def download_file(self, file_id: int):
        """Download a file."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.error_message = "Database connection not configured"
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            metadata = session.get(FileMetadata, file_id)
            if not metadata:
                self.error_message = "File not found"
                return
            
            content = None
            
            if metadata.storage_location == StorageLocation.DATABASE:
                # Get from database
                file_content = session.exec(
                    select(FileContent).where(FileContent.file_id == file_id)
                ).first()
                
                if file_content:
                    content = file_content.content
            else:
                # Get from filesystem
                if metadata.file_path and os.path.exists(metadata.file_path):
                    with open(metadata.file_path, "rb") as f:
                        content = f.read()
            
            if content:
                # Use Reflex's download functionality
                return rx.download(
                    data=content,
                    filename=metadata.original_filename
                )
    
    def handle_download_file(self, file_id: int):
        """Wrapper for download file to handle from UI."""
        return self.download_file(file_id)
    
    def set_file_to_delete(self, file_id: int):
        """Set file to delete and trigger deletion."""
        self.delete_file(file_id)
    
    def set_file_to_download(self, file_id: int):
        """Set file to download and trigger download."""
        yield self.download_file(file_id)