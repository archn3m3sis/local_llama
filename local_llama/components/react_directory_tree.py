"""Directory tree component using react-file-tree."""
import reflex as rx
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState
from .file_tree_wrapper import file_tree_component
from .shared_styles import BUTTON_SOFT_STYLE


def react_directory_tree() -> rx.Component:
    """Directory tree component using react-file-tree."""
    return rx.vstack(
        # Include CSS imports
        rx.html('''
            <link rel="stylesheet" href="https://unpkg.com/@sinm/react-file-tree@latest/styles.css" />
            <style>
                /* Override styles for dark theme */
                .file-tree {
                    background: transparent;
                    color: #e0e0e0;
                }
                .file-tree__item {
                    color: #e0e0e0;
                }
                .file-tree__item:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            </style>
        '''),
        
        # Header
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.hstack(
                rx.icon_button(
                    rx.icon("refresh-cw", size=14),
                    size="1",
                    on_click=DirectoryState.load_directory_tree,
                    title="Refresh",
                    **BUTTON_SOFT_STYLE,
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
        
        # Debug: Show the tree data
        rx.vstack(
            rx.text(
                rx.cond(
                    DirectoryState.has_directories,
                    "Debug: has_directories = true",
                    "Debug: has_directories = false"
                ),
                color="gray.400",
                size="1",
            ),
            rx.text(
                DirectoryState.directory_count,
                color="gray.400", 
                size="1",
            ),
            spacing="0",
            margin_bottom="0.5rem",
        ),
        
        # React File Tree component
        rx.cond(
            DirectoryState.loading_directories,
            rx.center(
                rx.spinner(size="3"),
                padding="4rem",
            ),
            rx.cond(
                DirectoryState.has_directories,
                rx.box(
                    file_tree_component(
                        tree=DirectoryState.react_file_tree,
                        activated_uri=DirectoryState.activated_uri,
                        on_item_click=DirectoryState.handle_react_tree_click,
                    ),
                    width="100%",  # Full width of parent
                    height="calc(100% - 200px)",
                    min_height="200px",
                    max_height="600px",
                    overflow_y="auto",
                    overflow_x="auto",  # Allow horizontal scroll
                    class_name="file-tree-container",
                    background="rgba(255, 255, 255, 0.02)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="md",
                    padding="1rem",
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
            width="100%",
            on_click=DirectoryState.set_creating_directory(True),
            **BUTTON_SOFT_STYLE,
        ),
        
        
        # Load directories on mount
        on_mount=[
            DirectoryState.load_directory_tree,
            DirectoryState.initialize_expanded_directories,
        ],
        
        width="100%",
        min_width="350px",  # Ensure minimum width
        height="100%",
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
        overflow_x="auto",  # Allow horizontal scroll if needed
    )