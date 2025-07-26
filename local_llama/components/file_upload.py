import reflex as rx
from typing import List, Dict
from ..states.file_storage_state import FileStorageState
from .upload_animation import creative_upload_animation, file_appear_animation
from .shared_styles import BUTTON_STYLE, BUTTON_SOFT_STYLE


def file_upload_zone() -> rx.Component:
    """Create a file upload zone with drag and drop support."""
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.box(
                    rx.icon("cloud_upload", size=64, color="blue.400"),
                    style={
                        "animation": "float 3s ease-in-out infinite",
                        "@keyframes float": {
                            "0%, 100%": {"transform": "translateY(0)"},
                            "50%": {"transform": "translateY(-20px)"}
                        }
                    }
                ),
                rx.text(
                    "Drag and drop files here or click to browse",
                    size="4",
                    color="gray.300",
                    weight="medium",
                ),
                rx.text(
                    "Supports: .md, .txt, .pdf, .svg, .png, .jpg",
                    size="2",
                    color="gray.500",
                ),
                spacing="3",
                align="center",
                padding="3em",
            ),
            id="upload_zone",
            border="2px dashed",
            border_color="gray.600",
            border_radius="xl",
            background="rgba(59, 130, 246, 0.02)",
            padding="2em",
            width="100%",
            height="240px",
            on_drop=FileStorageState.upload_file,
            multiple=True,
            accept={
                "text/markdown": [".md"],
                "text/plain": [".txt"],
                "application/pdf": [".pdf"],
                "image/svg+xml": [".svg"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
            },
            transition="all 0.3s ease",
            _hover={
                "border_color": "blue.400",
                "background": "rgba(59, 130, 246, 0.05)",
                "cursor": "pointer",
            }
        ),
        rx.cond(
            FileStorageState.uploading,
            creative_upload_animation(),
        ),
        rx.cond(
            FileStorageState.error_message != "",
            rx.text(
                FileStorageState.error_message,
                color="red.400",
                size="2",
            ),
        ),
        width="100%",
        spacing="4",
    )


def file_type_icon(file_type: str) -> rx.Component:
    """Return appropriate icon for file type."""
    icon_map = {
        "markdown": "file-text",
        "text": "file-text",
        "pdf": "file-text",
        "svg": "image",
        "png": "image",
        "jpeg": "image",
    }
    return rx.icon(
        icon_map.get(file_type, "file"),
        size=16,
        color="gray.400",
    )


def file_list_item(file_data: Dict, index: int) -> rx.Component:
    """Display a single file in the list."""
    return rx.hstack(
        file_type_icon(file_data["file_type"]),
        rx.vstack(
            rx.text(
                file_data["original_filename"],
                size="2",
                weight="medium",
                color="white",
            ),
            rx.hstack(
                rx.text(
                    file_data["file_size_kb"],
                    " KB",
                    size="1",
                    color="gray.400",
                ),
                rx.text("•", color="gray.600", size="1"),
                rx.text(
                    file_data["uploaded_at"],
                    size="1",
                    color="gray.400",
                ),
                spacing="1",
            ),
            spacing="1",
            align_items="start",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("download", size=14),
                size="1",
                variant="soft",
                color_scheme="blue",
                on_click=FileStorageState.set_file_to_download(file_data["file_id"]),
            ),
            rx.icon_button(
                rx.icon("trash-2", size=14),
                size="1",
                variant="soft",
                color_scheme="red",
                on_click=FileStorageState.set_file_to_delete(file_data["file_id"]),
            ),
            spacing="2",
        ),
        width="100%",
        padding="0.75em",
        border_radius="md",
        _hover={
            "background": "rgba(255, 255, 255, 0.05)",
            "cursor": "pointer",
        },
        align="center",
        spacing="3",
        class_name="file-list-item",
    )


def file_upload_modal() -> rx.Component:
    """Modal for uploading files."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("upload", size=16),
                "Upload Files",
                size="2",
                **BUTTON_SOFT_STYLE,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Upload Files"),
            rx.dialog.description(
                "Upload documents, images, and other files to the system.",
            ),
            rx.vstack(
                file_upload_zone(),
                spacing="4",
                width="100%",
            ),
            rx.dialog.close(
                rx.button(
                    "Close",
                    **BUTTON_SOFT_STYLE,
                ),
            ),
            style={
                "max_width": "600px",
                "background": "rgba(20, 20, 20, 0.95)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
            },
        ),
    )