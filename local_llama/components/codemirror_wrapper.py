"""CodeMirror wrapper component for Reflex."""
import reflex as rx
from typing import Dict, Any

class CodeMirrorEditor(rx.Component):
    """CodeMirror wrapper component for Reflex."""
    
    library = "@uiw/react-codemirror"
    tag = "CodeMirror"
    
    # Props
    value: rx.Var[str] = ""
    height: rx.Var[str] = "500px"
    placeholder: rx.Var[str] = "Start typing your markdown here..."
    editable: rx.Var[bool] = True
    
    # Define event triggers
    def get_event_triggers(self) -> Dict[str, Any]:
        """Get the event triggers for the component."""
        return {
            **super().get_event_triggers(),
            "on_change": lambda value: [value],
        }
    
    def _get_imports(self) -> Dict:
        """Define the imports for the component."""
        return {
            "react": ["useEffect"],
            "@codemirror/lang-markdown": ["markdown"],
            "@codemirror/theme-one-dark": ["oneDark"],
        }
    
    def _get_custom_code(self) -> str:
        """Add custom code for markdown extensions."""
        return """
const markdownExtensions = [markdown()];
"""
    
    def _render(self):
        """Render the component with markdown extensions."""
        return super()._render().add_props(
            extensions="markdownExtensions",
            theme="oneDark"
        )


# Create wrapper function
def codemirror_editor(**props) -> rx.Component:
    """Create a CodeMirror editor component."""
    return CodeMirrorEditor.create(**props)