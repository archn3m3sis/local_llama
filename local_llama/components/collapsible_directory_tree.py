"""Collapsible directory tree component."""
import reflex as rx
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def directory_click_handler() -> rx.Component:
    """JavaScript handler for directory clicks."""
    return rx.script("""
    window.addEventListener('directory-click', (event) => {
        const { id, path } = event.detail;
        // This will trigger the Reflex event handler
        window.reflex_internal_send_event('DirectoryState.handle_directory_click', { directory_id: id, path: path });
    });
    """)


def collapsible_directory_tree() -> rx.Component:
    """Directory tree with collapsible/expandable functionality."""
    return rx.vstack(
        # Include the click handler script
        directory_click_handler(),
        # Header
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.hstack(
                rx.icon_button(
                    rx.icon("folder-open", size=14),
                    size="1",
                    variant="soft",
                    on_click=DirectoryState.expand_all_directories,
                    title="Expand All",
                ),
                rx.icon_button(
                    rx.icon("folder", size=14),
                    size="1",
                    variant="soft",
                    on_click=DirectoryState.collapse_all_directories,
                    title="Collapse All",
                ),
                rx.icon_button(
                    rx.icon("refresh-cw", size=14),
                    size="1",
                    variant="soft",
                    on_click=DirectoryState.load_directory_tree,
                    title="Refresh",
                ),
                spacing="1",
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        rx.text(
            DirectoryState.directory_count,
            size="2", 
            color="gray.400",
            margin_bottom="1rem",
        ),
        
        # Directory tree content using HTML for now
        rx.cond(
            DirectoryState.loading_directories,
            rx.center(
                rx.spinner(size="3"),
                padding="4rem",
            ),
            rx.cond(
                DirectoryState.directories.length() > 0,
                rx.scroll_area(
                    rx.vstack(
                        # Use HTML rendering with click handlers
                        rx.html(DirectoryState.directories_html),
                        spacing="1",
                        width="100%",
                    ),
                    height="calc(100% - 200px)",
                    min_height="200px",
                    max_height="600px",
                    scrollbars="vertical",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("folder-x", size=48, color="gray.600"),
                        rx.text(
                            "No directories found",
                            color="gray.500",
                            size="3",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    padding="4rem",
                ),
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
        
        # Load directories on mount
        on_mount=[
            DirectoryState.load_directory_tree,
        ],
        
        width="100%",
        height="100%",
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
    )