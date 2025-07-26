"""Test component to verify directory loading."""
import reflex as rx
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def directory_list_test() -> rx.Component:
    """Simple list of all directories for testing."""
    return rx.vstack(
        rx.heading("Directory List Test", size="4"),
        rx.text(f"Total directories: {DirectoryState.directories.length()}"),
        
        rx.vstack(
            rx.foreach(
                DirectoryState.directories,
                lambda d: rx.hstack(
                    rx.text(d["full_path"], size="2"),
                    rx.text(f"(ID: {d['directory_id']})", size="1", color="gray.500"),
                    padding="0.25rem",
                    width="100%",
                    border_bottom="1px solid rgba(255,255,255,0.1)",
                )
            ),
            width="100%",
            spacing="0",
        ),
        
        rx.button(
            "Reload Directories",
            on_click=DirectoryState.load_directory_tree,
            size="2",
            color_scheme="blue",
        ),
        
        width="100%",
        padding="1rem",
        background="rgba(0,0,0,0.3)",
        border="1px solid rgba(255,255,255,0.1)",
        border_radius="md",
    )