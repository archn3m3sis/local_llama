"""State management for file upload with naming options."""
import reflex as rx
from typing import Optional, List, Dict


class UploadState(rx.State):
    """State for managing file uploads with naming."""
    
    # File naming dialog
    show_naming_dialog: bool = False
    pending_files: List[Dict] = []
    current_file_index: int = 0
    custom_filename: str = ""
    original_filename: str = ""
    file_extension: str = ""
    
    def start_file_naming(self, files):
        """Start the file naming process."""
        if not files:
            return
            
        # Convert files to list format for processing
        self.pending_files = []
        for file in files:
            if isinstance(file, dict):
                self.pending_files.append(file)
            else:
                # Handle other file formats
                self.pending_files.append({
                    'content': file,
                    'name': getattr(file, 'name', f"upload_{len(self.pending_files)}")
                })
        
        if self.pending_files:
            self.current_file_index = 0
            self._show_naming_for_current_file()
    
    def _show_naming_for_current_file(self):
        """Show naming dialog for current file."""
        if self.current_file_index < len(self.pending_files):
            current_file = self.pending_files[self.current_file_index]
            self.original_filename = current_file.get('name', 'unnamed')
            
            # Extract name and extension
            parts = self.original_filename.rsplit('.', 1)
            if len(parts) == 2:
                self.custom_filename = parts[0]
                self.file_extension = f".{parts[1]}"
            else:
                self.custom_filename = self.original_filename
                self.file_extension = ""
            
            self.show_naming_dialog = True
        else:
            # All files processed, start upload
            self._upload_all_files()
    
    def confirm_filename(self):
        """Confirm the custom filename and move to next file."""
        if self.current_file_index < len(self.pending_files):
            # Update the filename
            new_name = self.custom_filename + self.file_extension
            self.pending_files[self.current_file_index]['name'] = new_name
            
            # Move to next file
            self.current_file_index += 1
            self.show_naming_dialog = False
            
            # Show next file or start upload
            self._show_naming_for_current_file()
    
    def skip_naming(self):
        """Skip naming for current file and use original name."""
        self.current_file_index += 1
        self.show_naming_dialog = False
        self._show_naming_for_current_file()
    
    def cancel_upload(self):
        """Cancel the entire upload process."""
        self.show_naming_dialog = False
        self.pending_files = []
        self.current_file_index = 0
        self.custom_filename = ""
        self.original_filename = ""
        self.file_extension = ""
    
    def _upload_all_files(self):
        """Upload all files with their custom names."""
        # Import here to avoid circular import
        from .file_storage_state import FileStorageState
        
        # Get the FileStorageState instance and upload
        file_state = self.get_state(FileStorageState)
        file_state.upload_file(self.pending_files)
        
        # Reset state
        self.pending_files = []
        self.current_file_index = 0