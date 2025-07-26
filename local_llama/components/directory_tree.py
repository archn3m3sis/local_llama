import reflex as rx
from typing import Dict, List
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def directory_item(directory: Dict) -> rx.Component:
    """Render a single directory item."""
    return rx.hstack(
        rx.icon(
            "folder",
            size=18,
            color="blue.400",
        ),
        rx.text(
            directory["name"],
            size="2",
            weight="medium",
            color="white",
        ),
        rx.cond(
            directory["file_count"] > 0,
            rx.text(
                f" ({directory['file_count']})",
                size="1",
                color="gray.400",
            ),
        ),
        spacing="2",
        align="center",
        width="100%",
        padding="0.5rem",
        border_radius="md",
        cursor="pointer",
        on_click=[
            DirectoryState.navigate_to_directory(directory["directory_id"]),
            FileStorageState.set_current_directory_id(directory["directory_id"]),
            FileStorageState.set_current_directory_path(directory["full_path"]),
            FileStorageState.load_files(),
        ],
        _hover={
            "background": "rgba(255, 255, 255, 0.05)",
        },
    )


def directory_breadcrumbs() -> rx.Component:
    """Show breadcrumb navigation for current directory."""
    return rx.hstack(
        rx.icon("folder", size=16, color="gray.400"),
        rx.text(FileStorageState.current_directory_path, size="2", color="gray.400"),
        spacing="2",
        align="center",
        padding="0.5rem 0",
    )


def directory_tree() -> rx.Component:
    """Complete directory tree component."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh-cw", size=14),
                size="1",
                variant="soft",
                on_click=DirectoryState.load_directory_tree,
                title="Refresh directory tree",
            ),
            width="100%",
            margin_bottom="1rem",
        ),
        
        rx.scroll_area(
            rx.vstack(
                rx.foreach(
                    DirectoryState.directories,
                    directory_item,
                ),
                spacing="0",
                width="100%",
            ),
            height="400px",
            scrollbars="vertical",
        ),
        
        # Create new directory button
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
        padding="1rem",
        background="rgba(0, 0, 0, 0.3)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="lg",
    )


def create_directory_modal() -> rx.Component:
    """Modal for creating a new directory."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Create New Directory"),
            rx.vstack(
                rx.input(
                    placeholder="Directory name",
                    value=DirectoryState.new_directory_name,
                    on_change=DirectoryState.set_new_directory_name,
                    style={
                        "width": "100%",
                    }
                ),
                rx.text_area(
                    placeholder="Description (optional)",
                    value=DirectoryState.new_directory_description,
                    on_change=DirectoryState.set_new_directory_description,
                    rows="3",
                    style={
                        "width": "100%",
                    }
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
            style={
                "max_width": "450px",
            }
        ),
        open=DirectoryState.creating_directory,
    )