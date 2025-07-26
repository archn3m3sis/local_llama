"""User-aware directory tree component."""
import reflex as rx
import reflex_clerk_api as clerk
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState
from ..states.auth_state import AuthState


def user_directory_tree() -> rx.Component:
    """Directory tree that shows user-specific directories."""
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
        
        rx.text(
            DirectoryState.directory_count,
            size="2", 
            color="gray.400",
            margin_bottom="1rem",
        ),
        
        # Directory tree content
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
                        # Use HTML rendering for now
                        rx.html(DirectoryState.directories_html),
                        spacing="1",
                        width="100%",
                    ),
                    height="calc(100vh - 500px)",
                    min_height="200px",
                    max_height="600px",
                    scrollbars="vertical",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("folder-x", size=48, color="gray.600"),
                        rx.text(
                            "No accessible directories",
                            color="gray.500",
                            size="3",
                        ),
                        rx.text(
                            "Sign in to see your personal directories",
                            color="gray.600",
                            size="2",
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
        on_mount=DirectoryState.load_directory_tree,
        
        width="100%",
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
    )