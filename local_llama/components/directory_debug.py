"""Debug component to show directory state."""
import reflex as rx
from ..states.directory_state import DirectoryState


def directory_debug() -> rx.Component:
    """Debug component to show directory loading state."""
    return rx.vstack(
        rx.heading("Directory Debug Info", size="4", color="yellow"),
        
        rx.hstack(
            rx.text("Loading: ", weight="bold"),
            rx.text(DirectoryState.loading_directories),
            spacing="2",
        ),
        
        rx.hstack(
            rx.text("Directory Count: ", weight="bold"),
            rx.text(DirectoryState.directory_count),
            spacing="2",
        ),
        
        rx.hstack(
            rx.text("HTML Length: ", weight="bold"),
            rx.text(DirectoryState.directories_html.length()),
            spacing="2",
        ),
        
        rx.hstack(
            rx.text("Current Path: ", weight="bold"),
            rx.text(DirectoryState.current_path),
            spacing="2",
        ),
        
        rx.button(
            "Force Reload Directories",
            on_click=DirectoryState.load_directory_tree,
            color_scheme="green",
            size="2",
        ),
        
        spacing="3",
        padding="1rem",
        background="rgba(255, 255, 0, 0.1)",
        border="2px solid yellow",
        border_radius="md",
        width="100%",
    )