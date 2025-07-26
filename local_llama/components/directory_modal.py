"""Enhanced directory creation modal."""
import reflex as rx
from ..states.directory_state import DirectoryState


def directory_creation_modal() -> rx.Component:
    """Directory creation modal with proper state handling."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title("Create New Directory"),
                
                rx.input(
                    placeholder="Directory name",
                    value=DirectoryState.new_directory_name,
                    on_change=DirectoryState.set_new_directory_name,
                    width="100%",
                    auto_focus=True,
                ),
                
                rx.text_area(
                    placeholder="Description (optional)",
                    value=DirectoryState.new_directory_description,
                    on_change=DirectoryState.set_new_directory_description,
                    rows="3",
                    width="100%",
                ),
                
                rx.hstack(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        on_click=DirectoryState.cancel_directory_creation,
                    ),
                    rx.button(
                        "Create",
                        color_scheme="blue",
                        on_click=DirectoryState.create_directory_and_close,
                        loading=DirectoryState.creating_directory_in_progress,
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
            },
        ),
        open=DirectoryState.creating_directory,
        on_open_change=DirectoryState.set_creating_directory,
    )