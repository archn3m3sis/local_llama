import reflex as rx
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from sqlmodel import Session, create_engine, select, or_
from ..models.file_storage import FileDirectory, FileMetadata, DirectoryType


class DirectoryState(rx.State):
    """State management for directory operations."""
    
    # State variables with proper type annotations
    directories: List[Dict[str, Any]] = []
    current_directory_id: Optional[int] = None
    current_path: str = "/playbook"
    breadcrumbs: List[Dict[str, Any]] = []
    loading_directories: bool = False
    creating_directory: bool = False
    creating_directory_in_progress: bool = False
    new_directory_name: str = ""
    new_directory_description: str = ""
    selected_directory_id: Optional[int] = None
    directory_tree: List[Dict[str, Any]] = []
    expanded_directories: List[int] = []
    directories_html: str = ""
    directory_count: str = "No directories loaded"
    react_file_tree: Dict[str, Any] = {}  # Tree structure for react-file-tree
    activated_uri: str = ""
    has_directories: bool = False  # Flag to indicate if directories are loaded
    
    # Add property to store current user id
    current_user_id: Optional[int] = None
    
    def set_current_user_id(self, user_id: Optional[int]):
        """Set the current user ID for filtering."""
        self.current_user_id = user_id
        
    def load_directory_tree(self):
        """Load the directory tree structure (temporarily showing all directories)."""
        self.loading_directories = True
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.loading_directories = False
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # For now, show all directories
            all_dirs = session.exec(
                select(FileDirectory).order_by(FileDirectory.full_path)
            ).all()
            print(f"Found {len(all_dirs)} directories in database")  # Debug print
            
            # Build tree structure with file counts
            self.directory_tree = self._build_tree_with_counts(session, all_dirs)
            print(f"Built directory tree with {len(self.directory_tree)} root nodes")  # Debug print
            
            # Create a flat list of all directories with visual hierarchy
            self.directories = []
            for d in all_dirs:
                dir_dict = {
                    "directory_id": d.directory_id,
                    "name": d.name,
                    "full_path": d.full_path,
                    "description": d.description,
                    "icon": d.icon or "folder",
                    "color": d.color,
                    "is_system_directory": d.is_system_directory,
                    "is_public": d.is_public,
                    "can_create_subdirs": d.can_create_subdirs,
                    "can_upload_files": d.can_upload_files,
                    "file_count": self._get_file_count(session, d.directory_id),
                    "has_children": len(session.exec(
                        select(FileDirectory).where(FileDirectory.parent_id == d.directory_id)
                    ).all()) > 0,
                }
                self.directories.append(dir_dict)
            
            print(f"Loaded {len(self.directories)} directories")  # Debug print
            
            # Update directory count
            self.directory_count = f"{len(self.directories)} directories loaded"
            
            # Build HTML for directory list
            self._build_directories_html()
            
            # Build react-file-tree structure
            self._build_react_file_tree(all_dirs)
        
        self.loading_directories = False
    
    def _build_tree_with_counts(self, session: Session, directories: List[FileDirectory], parent_id: Optional[int] = None) -> List[Dict]:
        """Build hierarchical tree structure with file counts."""
        tree = []
        
        for dir in directories:
            if dir.parent_id == parent_id:
                children = self._build_tree_with_counts(session, directories, dir.directory_id)
                node = {
                    "directory_id": dir.directory_id,
                    "name": dir.name,
                    "full_path": dir.full_path,
                    "description": dir.description or "",
                    "icon": dir.icon or "folder",
                    "color": dir.color or "blue",
                    "is_system_directory": dir.is_system_directory,
                    "is_public": dir.is_public,
                    "can_create_subdirs": dir.can_create_subdirs,
                    "can_upload_files": dir.can_upload_files,
                    "children": children,
                    "has_children": len(children) > 0,
                    "file_count": self._get_file_count(session, dir.directory_id),
                }
                tree.append(node)
        
        return tree
    
    def navigate_to_directory(self, directory_id: int):
        """Navigate to a specific directory."""
        self.loading_directories = True
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.loading_directories = False
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Get the directory
            directory = session.get(FileDirectory, directory_id)
            if not directory:
                self.loading_directories = False
                return
            
            self.current_directory_id = directory_id
            self.current_path = directory.full_path
            
            # Build breadcrumbs
            self._build_breadcrumbs(session, directory)
            
            # Load child directories
            child_dirs = session.exec(
                select(FileDirectory)
                .where(FileDirectory.parent_id == directory_id)
                .order_by(FileDirectory.sort_order)
            ).all()
            
            self.directories = [
                {
                    "directory_id": d.directory_id,
                    "name": d.name,
                    "full_path": d.full_path,
                    "description": d.description,
                    "icon": d.icon,
                    "color": d.color,
                    "is_system_directory": d.is_system_directory,
                    "is_public": d.is_public,
                    "can_create_subdirs": d.can_create_subdirs,
                    "can_upload_files": d.can_upload_files,
                    "file_count": self._get_file_count(session, d.directory_id),
                }
                for d in child_dirs
            ]
        
        self.loading_directories = False
    
    def _build_breadcrumbs(self, session: Session, directory: FileDirectory):
        """Build breadcrumb trail for current directory."""
        breadcrumbs = []
        current = directory
        
        while current:
            breadcrumbs.append({
                "directory_id": current.directory_id,
                "name": current.name,
                "icon": current.icon,
            })
            
            if current.parent_id:
                current = session.get(FileDirectory, current.parent_id)
            else:
                current = None
        
        # Reverse to get root -> current order
        self.breadcrumbs = list(reversed(breadcrumbs))
    
    def _get_file_count(self, session: Session, directory_id: int) -> int:
        """Get count of files in a directory."""
        return len(session.exec(
            select(FileMetadata)
            .where(FileMetadata.directory_id == directory_id)
        ).all())
    
    def cancel_directory_creation(self):
        """Cancel directory creation and close modal."""
        self.creating_directory = False
        self.new_directory_name = ""
        self.new_directory_description = ""
        self.creating_directory_in_progress = False
    
    def create_directory_and_close(self):
        """Create directory and close modal on success."""
        self.create_directory()
        if not self.creating_directory_in_progress:  # If creation completed
            self.creating_directory = False
    
    def create_directory(self):
        """Create a new directory in the current location."""
        if not self.new_directory_name.strip():
            return
        
        self.creating_directory_in_progress = True
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            self.creating_directory_in_progress = False
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Check if current directory allows subdirectories
            if self.current_directory_id:
                parent_dir = session.get(FileDirectory, self.current_directory_id)
                if not parent_dir or not parent_dir.can_create_subdirs:
                    self.creating_directory = False
                    return
                
                parent_path = parent_dir.full_path
            else:
                parent_path = ""
            
            # Create the new directory
            full_path = f"{parent_path}/{self.new_directory_name.lower().replace(' ', '_')}"
            
            new_dir = FileDirectory(
                name=self.new_directory_name,
                parent_id=self.current_directory_id,
                full_path=full_path,
                directory_type=DirectoryType.USER,
                owner_id=1,  # TODO: Get from current user
                description=self.new_directory_description,
                is_public=False,
                is_system_directory=False,
                can_create_subdirs=True,
                can_upload_files=True,
            )
            
            session.add(new_dir)
            session.commit()
        
        # Clear form and reload
        self.new_directory_name = ""
        self.new_directory_description = ""
        self.creating_directory_in_progress = False
        
        # Reload current directory
        if self.current_directory_id:
            self.navigate_to_directory(self.current_directory_id)
        else:
            self.load_directory_tree()
    
    def toggle_directory_expanded(self, directory_id: int):
        """Toggle whether a directory is expanded in the tree view."""
        if directory_id in self.expanded_directories:
            self.expanded_directories = [d for d in self.expanded_directories if d != directory_id]
        else:
            self.expanded_directories = self.expanded_directories + [directory_id]
    
    def expand_all_directories(self):
        """Expand all directories in the tree."""
        # Collect all directory IDs that have children
        all_parent_ids = []
        for dir_info in self.directories:
            if dir_info.get("has_children", False):
                all_parent_ids.append(dir_info["directory_id"])
        self.expanded_directories = all_parent_ids
    
    def collapse_all_directories(self):
        """Collapse all directories in the tree."""
        self.expanded_directories = []
    
    def get_directory_path(self, directory_id: int) -> str:
        """Get the full path of a directory."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return "/"
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            directory = session.get(FileDirectory, directory_id)
            return directory.full_path if directory else "/"
    
    def can_create_in_directory(self, directory_id: Optional[int]) -> bool:
        """Check if user can create subdirectories in the given directory."""
        if not directory_id:
            return False
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return False
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            directory = session.get(FileDirectory, directory_id)
            return directory.can_create_subdirs if directory else False
    
    def navigate_to_parent(self):
        """Navigate to parent directory."""
        if not self.current_directory_id:
            return
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            current_dir = session.get(FileDirectory, self.current_directory_id)
            if current_dir and current_dir.parent_id:
                self.navigate_to_directory(current_dir.parent_id)
            else:
                # Go to root
                self.current_directory_id = None
                self.current_path = "/"
                self.breadcrumbs = []
                self.load_directory_tree()
    
    def _build_directories_html(self):
        """Build HTML representation of directories for display with collapsible functionality."""
        if not self.directory_tree:
            self.directories_html = "<div style='color: #9ca3af; text-align: center; padding: 2rem;'>No directories found</div>"
            return
        
        # Build HTML with proper tree structure
        def build_html_node(node: Dict[str, Any], depth: int = 0) -> str:
            directory_id = node.get("directory_id", 0)
            name = node.get("name", "")
            children = node.get("children", [])
            has_children = len(children) > 0
            is_expanded = directory_id in self.expanded_directories
            file_count = node.get("file_count", 0)
            file_count_text = f" ({file_count})" if file_count > 0 else ""
            
            # Build the directory item HTML
            html = f'''
            <div data-dir-id="{directory_id}" style="width: 100%;">
                <div style="
                    display: flex;
                    align-items: center;
                    padding: 0.4rem 0.5rem;
                    padding-left: {depth * 20 + 8}px;
                    border-radius: 0.375rem;
                    cursor: pointer;
                    transition: background 0.2s;
                    background: {'rgba(59, 130, 246, 0.2)' if directory_id == self.selected_directory_id else 'transparent'};
                " 
                onmouseover="this.style.background='rgba(59, 130, 246, 0.1)'"
                onmouseout="this.style.background='{'rgba(59, 130, 246, 0.2)' if directory_id == self.selected_directory_id else 'transparent'}'"
                onclick="window.dispatchEvent(new CustomEvent('directory-click', {{detail: {{id: {directory_id}, path: '{node.get("full_path", "")}'}}}}))">
                    '''
            
            # Add expand/collapse arrow for directories with children
            if has_children:
                html += f'''
                    <svg width="12" height="12" viewBox="0 0 12 12" style="margin-right: 4px; transform: rotate({90 if is_expanded else 0}deg); transition: transform 0.15s;">
                        <path d="M4 2 L8 6 L4 10" stroke="#e0e0e0" stroke-width="2" fill="none"/>
                    </svg>
                '''
            else:
                html += '<div style="width: 16px;"></div>'
            
            # Add folder icon
            icon_color = node.get("color", "#60a5fa")
            html += f'''
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-right: 6px; flex-shrink: 0;">
                        <path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" fill="{icon_color}"/>
                    </svg>
                    <span style="color: white; font-size: 0.875rem; font-weight: 500; flex: 1;">
                        {name}
                    </span>
                    <span style="color: #9ca3af; font-size: 0.75rem;">
                        {file_count_text}
                    </span>
                </div>
            '''
            
            # Add children if expanded
            if has_children and is_expanded:
                html += '<div style="width: 100%;">'
                for child in children:
                    html += build_html_node(child, depth + 1)
                html += '</div>'
            
            html += '</div>'
            return html
        
        # Build the complete HTML
        self.directories_html = build_html_node(self.directory_tree[0] if self.directory_tree else {})
    
    def _build_react_file_tree(self, directories: List[FileDirectory]):
        """Build tree structure compatible with react-file-tree."""
        if not directories:
            self.react_file_tree = {}
            self.has_directories = False
            return
        
        # Find all root directories (those without parent_id)
        root_dirs = [d for d in directories if d.parent_id is None]
        if not root_dirs:
            self.react_file_tree = {}
            self.has_directories = False
            return
        
        # Build tree recursively
        def build_node(directory: FileDirectory) -> Dict[str, Any]:
            children = []
            for d in directories:
                if d.parent_id == directory.directory_id:
                    children.append(build_node(d))
            
            # Sort children: directories first, then by name
            children.sort(key=lambda x: (x["type"] != "directory", x["uri"].lower()))
            
            node = {
                "type": "directory",
                "uri": directory.full_path,
                "expanded": directory.directory_id in self.expanded_directories,
                "name": directory.name,
                "directory_id": directory.directory_id,
            }
            
            if children:
                node["children"] = children
            
            return node
        
        # If we have multiple root directories, create a virtual root node
        if len(root_dirs) > 1:
            children = [build_node(d) for d in root_dirs]
            children.sort(key=lambda x: x["uri"].lower())
            self.react_file_tree = {
                "type": "directory",
                "uri": "/",
                "name": "Root",
                "expanded": True,
                "children": children
            }
        else:
            # Single root directory
            self.react_file_tree = build_node(root_dirs[0])
        
        # Debug output
        import json
        print(f"React file tree structure: {json.dumps(self.react_file_tree, indent=2)}")
        print(f"React file tree keys: {list(self.react_file_tree.keys())}")
        print(f"Has directories flag will be: {bool(self.react_file_tree)}")
        
        # Set flag to indicate we have directories
        self.has_directories = bool(self.react_file_tree)
    
    def initialize_expanded_directories(self):
        """Initialize expanded directories to show some content by default."""
        # Expand the root and first level directories
        if self.directories:
            root_dirs = [d for d in self.directories if d["full_path"].count("/") <= 2]
            self.expanded_directories = [d["directory_id"] for d in root_dirs]
            # Rebuild the tree with expanded state
            self.load_directory_tree()
    
    def handle_react_tree_click(self, node: Dict[str, Any]):
        """Handle click on react-file-tree item."""
        print(f"React tree click: {node}")  # Debug
        
        uri = node.get("uri", "")
        node_type = node.get("type", "")
        directory_id = node.get("directory_id")
        
        if node_type == "directory" and directory_id:
            # Toggle expansion in react tree
            expanded = node.get("expanded", False)
            
            # Update our expanded directories list
            if expanded:
                # Node is currently expanded, so collapse it
                self.expanded_directories = [d for d in self.expanded_directories if d != directory_id]
            else:
                # Node is currently collapsed, so expand it
                if directory_id not in self.expanded_directories:
                    self.expanded_directories = self.expanded_directories + [directory_id]
            
            # Set as selected
            self.selected_directory_id = directory_id
            self.activated_uri = uri
            self.current_directory_id = directory_id
            self.current_path = uri
            
            # Reload tree to update expanded state
            self.load_directory_tree()
            
            # Load files for this directory
            from ..states.file_storage_state import FileStorageState
            return FileStorageState.set_current_directory_from_tree(directory_id, uri)
    
    def handle_tree_item_click(self, node: Dict[str, Any]):
        """Handle click on tree item from react-file-tree."""
        uri = node.get("uri", "")
        directory_id = node.get("directory_id")
        
        if node.get("type") == "directory" and directory_id:
            # Toggle expansion
            if directory_id in self.expanded_directories:
                self.expanded_directories = [d for d in self.expanded_directories if d != directory_id]
            else:
                self.expanded_directories = self.expanded_directories + [directory_id]
            
            # Update the tree to reflect new expansion state
            self.load_directory_tree()
            
            # Set as selected and load files
            self.selected_directory_id = directory_id
            self.activated_uri = uri
            self.current_directory_id = directory_id
            self.current_path = uri
            
            # Trigger file loading through FileStorageState
            # This would need to be handled in the component
    
    def handle_directory_click(self, directory_id: int, path: str):
        """Handle click on directory from HTML tree."""
        # Check if this directory has children
        has_children = False
        for dir_info in self.directories:
            if dir_info["directory_id"] == directory_id and dir_info.get("has_children", False):
                has_children = True
                break
        
        if has_children:
            # Toggle expansion
            if directory_id in self.expanded_directories:
                self.expanded_directories = [d for d in self.expanded_directories if d != directory_id]
            else:
                self.expanded_directories = self.expanded_directories + [directory_id]
            
            # Rebuild HTML to reflect new state
            self._build_directories_html()
        
        # Always set as selected and update path
        self.selected_directory_id = directory_id
        self.current_directory_id = directory_id
        self.current_path = path
        self.activated_uri = path