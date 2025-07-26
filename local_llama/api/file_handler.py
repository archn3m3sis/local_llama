import os
from typing import Optional
from pathlib import Path
import reflex as rx
from sqlmodel import Session, create_engine, select
from ..models.file_storage import FileMetadata, FileContent, StorageLocation


class FileHandler(rx.State):
    """API handler for file operations."""
    
    @staticmethod
    def get_file_by_id(file_id: int) -> Optional[dict]:
        """Retrieve file data by ID."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return None
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            metadata = session.get(FileMetadata, file_id)
            if not metadata:
                return None
            
            result = {
                "filename": metadata.original_filename,
                "mime_type": metadata.mime_type,
                "content": None
            }
            
            if metadata.storage_location == StorageLocation.DATABASE:
                # Get from database
                file_content = session.exec(
                    select(FileContent).where(FileContent.file_id == file_id)
                ).first()
                
                if file_content:
                    result["content"] = file_content.content
            else:
                # Get from filesystem
                if metadata.file_path and os.path.exists(metadata.file_path):
                    with open(metadata.file_path, "rb") as f:
                        result["content"] = f.read()
            
            return result
    
    @staticmethod
    def download_file(file_id: int) -> rx.Component:
        """Create a download response for a file."""
        file_data = FileHandler.get_file_by_id(file_id)
        if not file_data or not file_data["content"]:
            return rx.text("File not found", status_code=404)
        
        return rx.download(
            data=file_data["content"],
            filename=file_data["filename"],
            mime_type=file_data["mime_type"]
        )