"""Access restricted component for private directories."""
import reflex as rx
from ..states.file_storage_state import FileStorageState


def access_restricted_message() -> rx.Component:
    """Display message when accessing restricted directories."""
    return rx.center(
        rx.vstack(
            rx.box(
                rx.icon("lock", size=48),
                style={
                    "color": "#EF4444",
                    "filter": "drop-shadow(0 0 20px #EF444440)",
                }
            ),
            rx.heading(
                "Access Restricted",
                size="5",
                style={
                    "color": "#EF4444",
                    "font_weight": "600",
                }
            ),
            rx.text(
                "Private Content",
                size="3",
                style={
                    "color": "rgba(239, 68, 68, 0.8)",
                    "font_weight": "500",
                }
            ),
            rx.text(
                "You don't have permission to view files in this directory.",
                size="2",
                style={
                    "color": "rgba(156, 163, 175, 0.9)",
                    "text_align": "center",
                    "max_width": "300px",
                }
            ),
            spacing="3",
            align="center",
            style={
                "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%)",
                "border": "1px solid rgba(239, 68, 68, 0.2)",
                "border_radius": "1rem",
                "padding": "3rem",
                "backdrop_filter": "blur(10px)",
            }
        ),
        padding="4em",
        width="100%",
    )


def upload_restriction_dialog() -> rx.Component:
    """Dialog shown when trying to upload to restricted directories."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Upload Restricted",
                style={"color": "#EF4444"}
            ),
            rx.dialog.description(
                rx.vstack(
                    rx.text(
                        "Content uploads into other users' personal directories are restricted.",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "You can only upload files to:",
                        weight="medium",
                        margin_bottom="0.5rem",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.icon("check", size=16, color="green.500"),
                            rx.text("Your own directories"),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.icon("check", size=16, color="green.500"),
                            rx.text("Other users' public folders"),
                            spacing="2",
                        ),
                        spacing="2",
                        align="start",
                        margin_left="1rem",
                    ),
                    spacing="3",
                )
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Understood",
                        color_scheme="red",
                        variant="soft",
                        on_click=FileStorageState.close_upload_restriction_dialog,
                    ),
                ),
                justify="end",
                margin_top="1rem",
            ),
        ),
        open=FileStorageState.show_upload_restriction_dialog,
    )