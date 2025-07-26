"""Basic directory list component for Reflex."""
import reflex as rx
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def basic_directory_list() -> rx.Component:
    """Basic directory list without dynamic foreach."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh-cw", size=14),
                size="1",
                variant="soft",
                on_click=DirectoryState.load_directory_tree,
                title="Refresh",
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        # Directory count
        rx.text(
            DirectoryState.directory_count,
            size="2",
            color="gray.400",
            margin_bottom="0.5rem",
        ),
        
        # Directory list
        rx.cond(
            DirectoryState.loading_directories,
            rx.center(
                rx.spinner(size="3"),
                padding="4rem",
            ),
            rx.scroll_area(
                rx.vstack(
                    # We'll render directories as HTML from the state
                    rx.html(DirectoryState.directories_html),
                    spacing="1",
                    width="100%",
                ),
                height="calc(100vh - 400px)",
                min_height="300px",
                scrollbars="vertical",
            ),
        ),
        
        # Create button
        rx.button(
            rx.icon("folder-plus", size=16),
            "New Directory",
            size="2",
            variant="soft",
            color_scheme="blue",
            width="100%",
            on_click=DirectoryState.set_creating_directory(True),
        ),
        
        width="100%",
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
    )