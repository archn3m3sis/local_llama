import reflex as rx
from typing import List, Dict
from ..states.file_storage_state import FileStorageState
from .upload_animation import creative_upload_animation, file_appear_animation
from .shared_styles import BUTTON_STYLE, BUTTON_SOFT_STYLE


def smooth_progress_bar() -> rx.Component:
    """Create a smooth animated progress bar."""
    return rx.box(
        rx.box(
            style={
                "width": FileStorageState.upload_progress.to_string() + "%",
                "height": "100%",
                "background": "linear-gradient(90deg, #60A5FA 0%, #A78BFA 50%, #60A5FA 100%)",
                "background_size": "200% 100%",
                "border_radius": "1rem",
                "transition": "width 0.3s ease-out",
                "animation": "shimmer 2s linear infinite",
                "box_shadow": "0 0 20px #60A5FA40, inset 0 0 10px rgba(255, 255, 255, 0.3)",
                "@keyframes shimmer": {
                    "0%": {"background_position": "0% 50%"},
                    "100%": {"background_position": "200% 50%"}
                }
            }
        ),
        width="100%",
        height="6px",
        style={
            "background": "rgba(255, 255, 255, 0.1)",
            "border_radius": "1rem",
            "overflow": "hidden",
            "box_shadow": "inset 0 0 10px rgba(0, 0, 0, 0.3)",
        }
    )



def file_upload_zone() -> rx.Component:
    """Create a file upload zone with drag and drop support."""
    return rx.vstack(
        rx.upload(
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.icon("cloud_upload", size=64),
                        style={
                            "color": "#60A5FA",
                            "filter": "drop-shadow(0 0 30px #60A5FA40)",
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
                        style={
                            "color": "rgba(255, 255, 255, 0.9)",
                            "font_weight": "500",
                            "font_family": "Inter, system-ui, sans-serif",
                        }
                    ),
                    rx.text(
                        "Supports: .md, .txt, .pdf, .svg, .png, .jpg",
                        size="2",
                        style={
                            "color": "rgba(156, 163, 175, 0.7)",
                            "font_family": "Inter, system-ui, sans-serif",
                        }
                    ),
                    spacing="3",
                    align="center",
                ),
                height="100%",
                width="100%",
            ),
            id="upload_zone",
            style={
                "border": "2px dashed rgba(96, 165, 250, 0.3)",
                "border_radius": "1rem",
                "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(147, 51, 234, 0.05) 100%)",
                "padding": "1rem",
                "width": "100%",
                "height": "200px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "transition": "all 0.3s ease",
                "backdrop_filter": "blur(10px)",
                "_hover": {
                    "border_color": "rgba(96, 165, 250, 0.6)",
                    "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%)",
                    "cursor": "pointer",
                    "box_shadow": "0 8px 32px rgba(59, 130, 246, 0.15)",
                }
            },
            on_drop=FileStorageState.handle_upload,
            multiple=False,  # Change to single file to ensure clean state
            accept={
                "text/markdown": [".md"],
                "text/plain": [".txt"],
                "application/pdf": [".pdf"],
                "image/svg+xml": [".svg"],
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
            },
        ),
        rx.cond(
            FileStorageState.uploading,
            rx.vstack(
                creative_upload_animation(),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            FileStorageState.upload_status,
                            size="2",
                            color="cyan.400",
                            weight="medium",
                        ),
                        rx.spacer(),
                        rx.text(
                            FileStorageState.upload_progress.to_string() + "%",
                            size="2",
                            color="cyan.400",
                            weight="bold",
                        ),
                        width="100%",
                        align="center",
                    ),
                    smooth_progress_bar(),
                    spacing="2",
                    width="100%",
                    margin_top="1rem",
                ),
                spacing="4",
                width="100%",
                align="center",
            ),
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
    """Return appropriate icon for file type with modern colors."""
    icon_config = {
        "markdown": {"icon": "file-text", "color": "#818CF8"},  # Purple
        "text": {"icon": "file-text", "color": "#60A5FA"},     # Blue
        "pdf": {"icon": "file-text", "color": "#F87171"},      # Red
        "svg": {"icon": "image", "color": "#34D399"},          # Green
        "png": {"icon": "image", "color": "#FBBF24"},          # Yellow
        "jpeg": {"icon": "image", "color": "#FB923C"},         # Orange
    }
    config = icon_config.get(file_type, {"icon": "file", "color": "#9CA3AF"})
    return rx.box(
        rx.icon(
            config["icon"],
            size=20,
            color=config["color"],
        ),
        style={
            "padding": "0.5rem",
            "background": f"radial-gradient(circle, {config['color']}20 0%, transparent 70%)",
            "border_radius": "0.75rem",
        }
    )


def file_list_item(file_data: Dict, index: int) -> rx.Component:
    """Display a single file in the list with modern styling."""
    return rx.hstack(
        file_type_icon(file_data["file_type"]),
        rx.vstack(
            rx.text(
                file_data["original_filename"],
                size="3",
                weight="medium",
                style={
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_family": "Inter, system-ui, sans-serif",
                }
            ),
            rx.hstack(
                rx.text(
                    file_data["file_size_kb"],
                    " KB",
                    size="1",
                    style={"color": "rgba(156, 163, 175, 0.8)"},
                ),
                rx.text("•", style={"color": "rgba(107, 114, 128, 0.6)"}, size="1"),
                rx.text(
                    file_data["uploaded_at"],
                    size="1",
                    style={"color": "rgba(156, 163, 175, 0.8)"},
                ),
                spacing="2",
            ),
            spacing="1",
            align_items="start",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("download", size=16),
                size="2",
                style={
                    "background": "rgba(59, 130, 246, 0.1)",
                    "color": "#60A5FA",
                    "border": "1px solid rgba(59, 130, 246, 0.2)",
                    "cursor": "pointer",
                    "transition": "all 0.2s ease",
                    "_hover": {
                        "background": "rgba(59, 130, 246, 0.2)",
                        "border_color": "rgba(59, 130, 246, 0.4)",
                        "transform": "translateY(-1px)",
                        "box_shadow": "0 4px 12px rgba(59, 130, 246, 0.15)",
                    }
                },
                on_click=FileStorageState.set_file_to_download(file_data["file_id"]),
            ),
            rx.icon_button(
                rx.icon("trash-2", size=16),
                size="2",
                style={
                    "background": "rgba(239, 68, 68, 0.1)",
                    "color": "#F87171",
                    "border": "1px solid rgba(239, 68, 68, 0.2)",
                    "cursor": "pointer",
                    "transition": "all 0.2s ease",
                    "_hover": {
                        "background": "rgba(239, 68, 68, 0.2)",
                        "border_color": "rgba(239, 68, 68, 0.4)",
                        "transform": "translateY(-1px)",
                        "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.15)",
                    }
                },
                on_click=FileStorageState.set_file_to_delete(file_data["file_id"]),
            ),
            spacing="2",
        ),
        width="100%",
        padding="1rem",
        style={
            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
            "border": "1px solid rgba(255, 255, 255, 0.08)",
            "border_radius": "0.75rem",
            "backdrop_filter": "blur(10px)",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%)",
                "border_color": "rgba(255, 255, 255, 0.15)",
                "transform": "translateX(4px)",
                "box_shadow": "0 8px 24px rgba(0, 0, 0, 0.15)",
            }
        },
        align="center",
        spacing="3",
        class_name="file-list-item",
    )


def file_rename_dialog() -> rx.Component:
    """Simple file rename dialog."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Name Your File"),
            rx.dialog.description(f"Original: {FileStorageState.original_filename}"),
            rx.vstack(
                rx.input(
                    value=FileStorageState.custom_filename,
                    on_change=FileStorageState.set_custom_filename,
                    placeholder="Enter filename",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=FileStorageState.cancel_rename,
                        variant="soft",
                    ),
                    rx.button(
                        "Upload",
                        on_click=FileStorageState.confirm_rename,
                        color_scheme="blue",
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
        ),
        open=FileStorageState.show_rename_dialog,
    )

def file_upload_modal() -> rx.Component:
    """Modal for uploading files."""
    return rx.fragment(
        file_rename_dialog(),
        rx.dialog.root(
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
                rx.flex(
                    rx.button(
                        "Reset",
                        on_click=FileStorageState.reset_upload_state,
                        variant="ghost",
                        size="2",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            "Close",
                            **BUTTON_SOFT_STYLE,
                        ),
                    ),
                    width="100%",
                    justify="between",
                    margin_top="1rem",
                ),
                style={
                    "max_width": "600px",
                    "background": "rgba(20, 20, 20, 0.95)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                },
            ),
        )
    )