"""Simplified directory tree component that works with Reflex constraints."""
import reflex as rx
from typing import Dict, List, Any
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def directory_item_simple(directory: Dict[str, Any]) -> rx.Component:
    """Render a simple directory item."""
    # Create static components based on the directory data
    return rx.hstack(
        rx.icon("folder", size=18, color="blue.400"),
        rx.text(
            directory["name"],
            size="2",
            weight="medium",
            color="white",
        ),
        spacing="2",
        align="center",
        width="100%",
        padding="0.5rem",
        padding_left=f"{(directory['full_path'].count('/') - 1) * 20 + 8}px",  # Dynamic indentation
        border_radius="md",
        cursor="pointer",
        on_click=[
            DirectoryState.navigate_to_directory(directory["directory_id"]),
            FileStorageState.set_current_directory_id(directory["directory_id"]),
            FileStorageState.set_current_directory_path(directory["full_path"]),
            FileStorageState.load_files(),
        ],
        _hover={
            "background": "rgba(59, 130, 246, 0.1)",
        },
    )


def simple_breadcrumbs() -> rx.Component:
    """Simple breadcrumb navigation."""
    return rx.hstack(
        rx.icon("home", size=16, color="gray.400"),
        rx.text(FileStorageState.current_directory_path, size="2", color="gray.400"),
        spacing="2",
        align="center",
        padding="0.75rem 1rem",
    )


def simple_directory_tree() -> rx.Component:
    """Simplified directory tree that works with Reflex."""
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
        
        # Directory list
        rx.cond(
            DirectoryState.loading_directories,
            rx.center(
                rx.spinner(size="3"),
                padding="4rem",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        DirectoryState.directories,
                        directory_item_simple,
                    ),
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


def simple_create_directory_modal() -> rx.Component:
    """Simple directory creation modal."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title("Create New Directory"),
                
                rx.input(
                    placeholder="Directory name",
                    value=DirectoryState.new_directory_name,
                    on_change=DirectoryState.set_new_directory_name,
                    width="100%",
                ),
                
                rx.text_area(
                    placeholder="Description (optional)",
                    value=DirectoryState.new_directory_description,
                    on_change=DirectoryState.set_new_directory_description,
                    rows="3",
                    width="100%",
                ),
                
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Create",
                            color_scheme="blue",
                            on_click=DirectoryState.create_directory,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                
                spacing="4",
                width="100%",
            ),
        ),
        open=DirectoryState.creating_directory,
    )