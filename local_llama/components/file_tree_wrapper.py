"""Simple wrapper for react-file-tree component."""
import reflex as rx
from typing import Dict, Any, Optional, List


class FileTreeComponent(rx.Component):
    """React file tree component wrapper."""
    
    library = "@sinm/react-file-tree"
    tag = "FileTree"
    
    
    # Component props
    tree: rx.Var[Dict[str, Any]]
    activated_uri: rx.Var[str] = ""
    
    def add_imports(self) -> Dict[str, List[str]]:
        """Import CSS files."""
        return {}
    
    def get_event_triggers(self) -> dict:
        """Define event handlers."""
        return {
            **super().get_event_triggers(),
            "on_item_click": lambda e0: [e0],
        }


# Create the component
file_tree_component = FileTreeComponent.create