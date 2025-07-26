from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from enum import Enum


class FileType(str, Enum):
    MARKDOWN = "markdown"
    TEXT = "text"
    PDF = "pdf"
    SVG = "svg"
    PNG = "png"
    JPEG = "jpeg"
    OTHER = "other"


class StorageLocation(str, Enum):
    DATABASE = "database"  # For small, critical files
    FILESYSTEM = "filesystem"  # For larger files
    

class DirectoryType(str, Enum):
    """Types of directories in the system."""
    SYSTEM = "system"  # System-created directories (can't be deleted)
    USER = "user"  # User-created directories
    

class FileDirectory(SQLModel, table=True):
    """Directory structure for organizing files."""
    __tablename__ = "file_directory"
    
    directory_id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    parent_id: Optional[int] = Field(default=None, foreign_key="file_directory.directory_id")
    full_path: str = Field(max_length=1000)  # /playbook/playbook_personal/pbper_drafts
    
    # Directory type and ownership
    directory_type: DirectoryType = Field(default=DirectoryType.USER)
    owner_id: Optional[int] = Field(default=None, foreign_key="employee.id")
    is_public: bool = Field(default=False)
    is_system_directory: bool = Field(default=False)  # Cannot be deleted if True
    
    # Associated entities
    project_id: Optional[int] = Field(default=None, foreign_key="project.project_id")
    department_id: Optional[int] = Field(default=None, foreign_key="department.dept_id")
    
    # Metadata
    description: Optional[str] = Field(default=None)
    icon: Optional[str] = Field(default="folder", max_length=50)
    color: Optional[str] = Field(default="#3b82f6", max_length=7)
    sort_order: int = Field(default=0)  # For ordering directories in UI
    
    # Access control
    can_create_subdirs: bool = Field(default=True)
    can_upload_files: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class FileMetadata(SQLModel, table=True):
    """Metadata for all stored files in IAMS."""
    __tablename__ = "file_metadata"
    
    file_id: int = Field(primary_key=True)
    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_type: FileType
    mime_type: str = Field(max_length=100)
    file_size: int  # Size in bytes
    storage_location: StorageLocation
    file_path: Optional[str] = Field(default=None, max_length=500)  # For filesystem storage
    checksum: str = Field(max_length=64)  # SHA-256 hash
    
    # Directory structure
    directory_id: Optional[int] = Field(default=None, foreign_key="file_directory.directory_id")
    
    # Relationships
    uploaded_by: int = Field(foreign_key="employee.id")
    asset_id: Optional[int] = Field(default=None, foreign_key="asset.asset_id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.project_id")
    
    # Metadata
    description: Optional[str] = Field(default=None)
    tags: Optional[str] = Field(default=None)  # JSON array of tags
    is_public: bool = Field(default=False)
    
    # Timestamps
    uploaded_at: datetime = Field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = Field(default=None)
    

class FileContent(SQLModel, table=True):
    """Storage for small files directly in database."""
    __tablename__ = "file_content"
    
    content_id: int = Field(primary_key=True)
    file_id: int = Field(foreign_key="file_metadata.file_id", unique=True)
    content: bytes  # VARBINARY(MAX) in MSSQL
    

class FileVersion(SQLModel, table=True):
    """Version tracking for files."""
    __tablename__ = "file_version"
    
    version_id: int = Field(primary_key=True)
    file_id: int = Field(foreign_key="file_metadata.file_id")
    version_number: int
    file_path: Optional[str] = Field(default=None, max_length=500)
    content: Optional[bytes] = Field(default=None)  # For database-stored versions
    checksum: str = Field(max_length=64)
    
    # Change tracking
    changed_by: int = Field(foreign_key="employee.id")
    change_description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    

class DocumentLink(SQLModel, table=True):
    """Links between documents and system entities."""
    __tablename__ = "document_link"
    
    link_id: int = Field(primary_key=True)
    file_id: int = Field(foreign_key="file_metadata.file_id")
    
    # Polymorphic relationships
    entity_type: str = Field(max_length=50)  # 'asset', 'ticket', 'vulnerability', etc.
    entity_id: int
    
    link_type: str = Field(max_length=50)  # 'attachment', 'evidence', 'report', etc.
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: int = Field(foreign_key="employee.id")