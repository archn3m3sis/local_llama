import reflex as rx
from ..components.metallic_text import metallic_title

def FilesSimple() -> rx.Component:
    """Simple test version of file management page."""
    return rx.vstack(
        # Title
        metallic_title("IAMS - File Management"),
        
        # Test text
        rx.text("Test: If you can see this, the page is rendering", color="white", size="4"),
        
        # Page positioning
        spacing="6",
        align="start",
        width="100%",
        padding="3em",
        padding_top="4em",
        position="absolute",
        top="0",
        left="0",
        right="0",
        min_height="100vh",
        z_index="10",
    )