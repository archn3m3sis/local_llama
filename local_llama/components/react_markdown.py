"""React Markdown component wrapper for Reflex."""
import reflex as rx
from typing import Dict, Any


class ReactMarkdown(rx.Component):
    """A React Markdown component that renders markdown content."""
    
    # The React library to wrap
    library = "react-markdown"
    
    # The React component tag
    tag = "ReactMarkdown"
    
    # Props - don't define children as it's handled by Reflex
    class_name: rx.Var[str] = ""  # CSS class name
    
    # Allow raw HTML (be careful with this)
    allow_element: rx.Var[bool] = True
    skip_html: rx.Var[bool] = False
    
    # Props for styling
    components: rx.Var[Dict[str, Any]] = {}
    
    # Use is_default=True to accept children
    is_default = True
    
    def _get_custom_code(self) -> str:
        return ""


# Create the component function
react_markdown = ReactMarkdown.create