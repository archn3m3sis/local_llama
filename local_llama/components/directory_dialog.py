"""Directory creation dialog component."""
import reflex as rx
from ..states.directory_state import DirectoryState


def directory_creation_dialog() -> rx.Component:
    """Dialog for creating new directories."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Create New Directory"),
            rx.dialog.description(
                "Enter a name for the new directory. It will be created in the current location."
            ),
            rx.vstack(
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
                    width="100%",
                    rows="3",
                ),
                rx.cond(
                    DirectoryState.creating_directory_in_progress,
                    rx.center(
                        rx.spinner(size="3"),
                        padding="1rem",
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        on_click=DirectoryState.cancel_directory_creation,
                    ),
                ),
                rx.spacer(),
                rx.button(
                    "Create",
                    color_scheme="blue",
                    on_click=DirectoryState.create_directory_and_close,
                    loading=DirectoryState.creating_directory_in_progress,
                ),
                width="100%",
                margin_top="1rem",
            ),
        ),
        open=DirectoryState.creating_directory,
    )