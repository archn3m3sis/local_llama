import reflex as rx
import os
import hashlib
from typing import List, Optional, Dict
from reflex import UploadFile
from datetime import datetime
from pathlib import Path
import base64
import asyncio
from sqlmodel import Session, create_engine, select
from ..models.file_storage import FileMetadata, FileContent, FileType, StorageLocation
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import time


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
    current_directory_path: str = "/"  # Start at root to see all files
    
    # File naming dialog
    show_rename_dialog: bool = False
    custom_filename: str = ""
    pending_upload_data: bytes = b""
    original_filename: str = ""
    upload_key: int = 0  # Key to force re-render of upload component
    show_upload_modal: bool = False  # Control upload modal visibility
    
    # Access control
    current_user_id: Optional[int] = 1  # TODO: Get from auth system
    access_denied: bool = False
    access_denied_message: str = ""
    show_upload_restriction_dialog: bool = False
    upload_restriction_message: str = ""
    
    def sync_user_from_auth(self):
        """Sync user ID from AuthState."""
        # For now, hardcode user ID until we can properly access AuthState
        # TODO: Implement proper user authentication integration
        self.current_user_id = 1  # Temporary hardcoded user ID
        print(f"FileStorageState: Set current_user_id to {self.current_user_id} (hardcoded)")
    
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
    
    def _save_file_to_db_with_timeout(self, engine, metadata, upload_data, storage_location, timeout=5):
        """Save file to database with timeout."""
        try:
            with Session(engine) as session:
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
                        f"{metadata.filename}"
                    )
                    
                    with open(file_path, "wb") as f:
                        f.write(upload_data)
                    
                    metadata.file_path = file_path
                    session.add(metadata)
                
                session.commit()
                return True, None
        except Exception as e:
            return False, str(e)
    
    async def handle_upload(self, files):
        """Handle file upload from Reflex upload component."""
        print(f"[handle_upload] Called with files: {files}")
        print(f"[handle_upload] Current state - uploading: {self.uploading}, show_rename_dialog: {self.show_rename_dialog}")
        
        if not files:
            return
            
        # For now, handle single file with rename option
        file = files[0]
        
        # Don't process if we're already uploading
        if self.uploading:
            print("[handle_upload] Skipping - already uploading")
            return
            
        # Clear any previous pending data if dialog is not shown
        if not self.show_rename_dialog:
            self.pending_upload_data = b""
            self.original_filename = ""
            self.custom_filename = ""
            
        try:
            # Check if file is already bytes
            if isinstance(file, bytes):
                self.pending_upload_data = file
                self.original_filename = f"upload_{datetime.now().timestamp()}"
            elif isinstance(file, dict):
                # File might be a dictionary with content and name
                self.pending_upload_data = file.get('content', b'')
                self.original_filename = file.get('name', f"upload_{datetime.now().timestamp()}")
            else:
                # Try to read file data if it has a read method
                if hasattr(file, 'read'):
                    self.pending_upload_data = await file.read()
                else:
                    # File might already be the data
                    self.pending_upload_data = file
                    
                # Get filename
                self.original_filename = getattr(file, 'filename', None) or \
                                       getattr(file, 'name', None) or \
                                       f"upload_{datetime.now().timestamp()}"
            
            # Only proceed if we actually have data
            if not self.pending_upload_data:
                self.error_message = "No file data received"
                return
                
            # Extract just the name without extension for editing
            name_parts = self.original_filename.rsplit('.', 1)
            if len(name_parts) == 2:
                self.custom_filename = name_parts[0]
            else:
                self.custom_filename = self.original_filename
                
            # Show rename dialog
            self.show_rename_dialog = True
            print(f"[handle_upload] Showing rename dialog for: {self.original_filename}")
            
        except Exception as e:
            print(f"[handle_upload] Error: {str(e)}")
            self.error_message = f"Failed to process file: {str(e)}"
    
    def cancel_rename(self):
        """Cancel the rename operation."""
        self.show_rename_dialog = False
        self.pending_upload_data = b""
        self.original_filename = ""
        self.custom_filename = ""
    
    def confirm_rename(self):
        """Confirm rename and proceed with upload."""
        self.show_rename_dialog = False
        
        # Check upload permissions first
        can_view, can_upload = self._check_directory_access(self.current_directory_id)
        
        if not can_upload:
            # Show upload restriction dialog
            self.show_upload_restriction_dialog = True
            self.upload_restriction_message = (
                "Content uploads into other users' personal directories are restricted. "
                "You can only upload files to:\n"
                "• Your own directories\n"
                "• Other users' public folders"
            )
            # Clear pending upload data
            self.pending_upload_data = b""
            self.original_filename = ""
            self.custom_filename = ""
            return
        
        # Construct final filename
        name_parts = self.original_filename.rsplit('.', 1)
        if len(name_parts) == 2:
            final_filename = f"{self.custom_filename}.{name_parts[1]}"
        else:
            final_filename = self.custom_filename
            
        # Start upload - set these immediately for UI feedback
        self.uploading = True
        self.error_message = ""
        self.upload_progress = 0
        self.upload_status = "Starting upload..."
        
        # Debug print
        print(f"Starting upload for file: {final_filename}, uploading={self.uploading}")
        
        # Schedule the upload to run after UI updates
        return self.start_upload_process(self.pending_upload_data, final_filename)
    
    async def start_upload_process(self, upload_data: bytes, filename: str):
        """Start the upload process with proper async handling."""
        # Small delay to ensure UI state updates first
        await asyncio.sleep(0.1)
        yield
        
        # Now do the actual upload
        async for _ in self.do_upload(upload_data, filename):
            yield
    
    async def do_upload(self, upload_data: bytes, filename: str):
        """Perform the actual upload with progress updates."""
        print(f"[do_upload] Starting upload for: {filename}")
        try:
            # Set initial progress immediately
            self.upload_progress = 1
            self.upload_status = "Initializing upload..."
            yield
            
            # Small delay to ensure UI shows
            await asyncio.sleep(0.1)
            yield
            
            # Process the upload with progress updates
            async for _ in self.upload_single_file(upload_data, filename):
                yield
                
            print(f"[do_upload] Upload completed for: {filename}")
            
            # Ensure we're at 100% before cleanup
            self.upload_progress = 100
            self.upload_status = "Upload complete!"
            yield
            await asyncio.sleep(0.5)  # Show complete status briefly
            
            # Clean up upload state
            self.uploading = False
            self.upload_success = True
            self.upload_progress = 0
            self.upload_status = ""
            
            # Clear ALL upload-related data to prevent dialog from reopening
            self.pending_upload_data = b""
            self.original_filename = ""
            self.custom_filename = ""
            self.current_upload_filename = ""
            self.current_file_size_display = ""
            
            # Increment upload key to reset the upload component
            self.upload_key += 1
            
            # Reload files
            self.load_files()
            
            # Small delay before resetting success flag
            await asyncio.sleep(2)
            self.upload_success = False
            
        except Exception as e:
            print(f"[do_upload] Upload failed: {str(e)}")
            self.error_message = f"Upload failed: {str(e)}"
            self.uploading = False
            self.upload_progress = 0
            self.upload_status = ""
            
            # Clear upload data on error too
            self.pending_upload_data = b""
            self.original_filename = ""
            self.custom_filename = ""
            self.current_upload_filename = ""
            self.current_file_size_display = ""
            
            # Increment key to reset upload component
            self.upload_key += 1
    
    async def upload_single_file(self, upload_data: bytes, filename: str):
        """Upload a single file."""
        print(f"[upload_single_file] Starting for: {filename}")
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.error_message = "Database connection not configured"
            return
            
        engine = create_engine(database_url)
        
        try:
            file_size = len(upload_data)
            print(f"[upload_single_file] File size: {file_size} bytes")
            
            # Update current file info
            self.current_upload_filename = filename
            self.current_file_size_display = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"
            
            # Smooth progress updates with visible delays
            print("[upload_single_file] Phase 1: Reading file...")
            for progress in range(0, 31, 2):
                self.upload_progress = progress
                self.upload_status = f"Reading file... {progress}%"
                yield
                await asyncio.sleep(0.05)  # 50ms delay
            
            # Determine file properties
            file_type = self._get_file_type(filename)
            mime_type = "application/octet-stream"
            
            print("[upload_single_file] Phase 2: Processing file...")
            for progress in range(30, 51, 2):
                self.upload_progress = progress
                self.upload_status = f"Processing file... {progress}%"
                yield
                await asyncio.sleep(0.05)  # 50ms delay
            
            checksum = self._calculate_checksum(upload_data)
            storage_location = self._determine_storage_location(file_size, file_type)
            print(f"[upload_single_file] Storage location: {storage_location}")
            
            print("[upload_single_file] Phase 3: Preparing save...")
            for progress in range(50, 71, 2):
                self.upload_progress = progress
                self.upload_status = f"Preparing save... {progress}%"
                yield
                await asyncio.sleep(0.05)  # 50ms delay
            
            print(f"Progress reached 71%, now attempting database save...")
            
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
                directory_id=self.current_directory_id,
            )
            
            # Run database save in a separate thread to prevent blocking
            save_success = False
            save_error = None
            
            # Create executor for async database operation
            executor = ThreadPoolExecutor(max_workers=1)
            
            # Start the save operation
            future = executor.submit(
                self._save_file_to_db_with_timeout,
                engine,
                metadata,
                upload_data,
                storage_location
            )
            
            # Continue progress while save happens in background
            for progress in range(71, 86):
                self.upload_progress = progress
                self.upload_status = f"Saving to storage... {progress}%"
                yield
                await asyncio.sleep(0.1)  # 100ms delay
                
                # Check if save completed
                if future.done():
                    try:
                        save_success, save_error = future.result(timeout=0.1)
                        if save_success:
                            print(f"File saved successfully: {filename}")
                        else:
                            print(f"Database error: {save_error}")
                    except Exception as e:
                        print(f"Error getting save result: {str(e)}")
                    break
            
            # If save still not complete, continue anyway
            if not future.done():
                print("Save operation taking too long, continuing with progress...")
                # Cancel the future to prevent resource leak
                future.cancel()
            
            executor.shutdown(wait=False)
            
            # Complete the progress regardless of save success
            print("[upload_single_file] Phase 4: Finalizing...")
            for progress in range(86, 91, 1):
                self.upload_progress = progress
                self.upload_status = f"Finalizing... {progress}%"
                yield
                await asyncio.sleep(0.05)  # 50ms delay
            
            # Final smooth progress
            print("[upload_single_file] Phase 5: Completing upload...")
            for progress in range(90, 101):
                self.upload_progress = progress
                self.upload_status = f"Upload complete! {progress}%"
                yield
                await asyncio.sleep(0.05)  # 50ms delay
                
            print(f"[upload_single_file] Upload finished at {self.upload_progress}%")
                
        except Exception as e:
            print(f"[upload_single_file] Exception: {str(e)}")
            self.error_message = f"Upload failed: {str(e)}"
            # Still try to complete the progress bar
            for progress in range(self.upload_progress, 101, 5):
                self.upload_progress = progress
                self.upload_status = f"Error occurred... {progress}%"
                yield
                await asyncio.sleep(0.05)
            raise
    
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
    
    def _check_directory_access(self, directory_id: Optional[int]) -> tuple[bool, bool]:
        """Check if user has access to view/upload in directory.
        Returns: (can_view, can_upload)
        """
        if not directory_id:
            # Root directory - everyone can view but not upload
            return True, False
            
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return False, False
            
        engine = create_engine(database_url)
        with Session(engine) as session:
            from ..models.file_storage import FileDirectory
            directory = session.get(FileDirectory, directory_id)
            
            if not directory:
                return False, False
                
            # User owns the directory
            if directory.owner_id == self.current_user_id:
                return True, True
                
            # Check if it's a public folder
            if directory.is_public or "public" in directory.name.lower():
                return True, True
                
            # Check parent directories for public access
            current = directory
            while current.parent_id:
                parent = session.get(FileDirectory, current.parent_id)
                if parent and parent.owner_id == self.current_user_id:
                    # Parent is owned by user, but this subdirectory isn't - no access
                    return False, False
                current = parent
                
        return False, False
    
    def set_current_directory_from_tree(self, directory_id: int, directory_path: str = None):
        """Set current directory from tree click and reload files."""
        self.current_directory_id = directory_id
        if directory_path:
            self.current_directory_path = directory_path
            
        # Check access before loading files
        can_view, can_upload = self._check_directory_access(directory_id)
        
        if can_view:
            self.access_denied = False
            self.access_denied_message = ""
            self.load_files()
        else:
            self.access_denied = True
            self.access_denied_message = "Access Restricted: Private Content"
            self.files = []  # Clear files list
    
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
            
            print(f"[load_files] Found {len(files)} files for directory_id: {self.current_directory_id}")
            
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
    
    def test_upload_overlay(self):
        """Test function to manually trigger upload overlay."""
        self.uploading = True
        self.upload_progress = 50
        self.upload_status = "Testing upload overlay..."
    
    def close_upload_overlay(self):
        """Close the upload overlay."""
        self.uploading = False
        self.upload_progress = 0
        self.upload_status = ""
    
    def close_upload_restriction_dialog(self):
        """Close the upload restriction dialog."""
        self.show_upload_restriction_dialog = False
        self.upload_restriction_message = ""
    
    def reset_upload_state(self):
        """Force reset all upload-related state."""
        print("[reset_upload_state] Resetting upload state")
        self.pending_upload_data = b""
        self.original_filename = ""
        self.custom_filename = ""
        self.show_rename_dialog = False
        self.uploading = False
        self.upload_progress = 0
        self.upload_status = ""
        self.error_message = ""
    
    def clear_all_files(self):
        """Clear all files from storage - both database and filesystem."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.error_message = "Database connection not configured"
            return
            
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Get all files
            all_files = session.exec(select(FileMetadata)).all()
            
            print(f"[clear_all_files] Clearing {len(all_files)} files")
            
            # Delete physical files
            for file_meta in all_files:
                if file_meta.storage_location == StorageLocation.FILESYSTEM and file_meta.file_path:
                    try:
                        if os.path.exists(file_meta.file_path):
                            os.remove(file_meta.file_path)
                            print(f"[clear_all_files] Deleted file: {file_meta.file_path}")
                    except Exception as e:
                        print(f"[clear_all_files] Error deleting file {file_meta.file_path}: {e}")
            
            # Delete all file content records
            file_contents = session.exec(select(FileContent)).all()
            for fc in file_contents:
                session.delete(fc)
            
            # Delete all file metadata records
            for fm in all_files:
                session.delete(fm)
            
            session.commit()
            print("[clear_all_files] All files cleared from database")
        
        # Clear the files list
        self.files = []
        
        # Also try to clean up the uploads directory
        try:
            import shutil
            if os.path.exists(self.FILE_STORAGE_PATH):
                shutil.rmtree(self.FILE_STORAGE_PATH)
                os.makedirs(self.FILE_STORAGE_PATH)
                print(f"[clear_all_files] Cleaned uploads directory: {self.FILE_STORAGE_PATH}")
        except Exception as e:
            print(f"[clear_all_files] Error cleaning uploads directory: {e}")