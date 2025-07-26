import reflex as rx
from ..components.universal_background import page_wrapper
from ..components.metallic_text import metallic_title
from ..components.file_upload import file_upload_modal, file_list_item
from ..states.file_storage_state import FileStorageState
from ..states.directory_state import DirectoryState
from ..components.shared_styles import CARD_STYLE
from ..components.upload_animation import file_appear_animation
from ..components.simple_directory_tree import simple_breadcrumbs
from ..components.react_directory_tree import react_directory_tree
from ..components.directory_modal import directory_creation_modal


def Files() -> rx.Component:
    """File management page."""
    return rx.vstack(
        # Massive metallic title
        metallic_title("IAMS - File Management"),
        
        # Animated description text
        rx.text(
                "Manage documents, images, and files across industrial asset directories", 
                color="gray.400", 
                font_size="1.1rem",
                margin_top="-1.5em",
                style={
                    "animation": "pixelateIn 1.5s ease-out forwards",
                    "filter": "blur(0px)",
                    "@keyframes pixelateIn": {
                        "0%": {
                            "filter": "blur(8px) brightness(0.3)",
                            "opacity": "0",
                            "transform": "scale(0.98) translateY(10px)",
                            "letter_spacing": "0.5em",
                        },
                        "20%": {
                            "filter": "blur(6px) brightness(0.4)",
                            "opacity": "0.2",
                            "transform": "scale(0.99) translateY(8px)",
                            "letter_spacing": "0.3em",
                        },
                        "40%": {
                            "filter": "blur(4px) brightness(0.6)",
                            "opacity": "0.4",
                            "transform": "scale(0.995) translateY(5px)",
                            "letter_spacing": "0.2em",
                        },
                        "60%": {
                            "filter": "blur(2px) brightness(0.8)",
                            "opacity": "0.7",
                            "transform": "scale(0.998) translateY(3px)",
                            "letter_spacing": "0.1em",
                        },
                        "80%": {
                            "filter": "blur(1px) brightness(0.9)",
                            "opacity": "0.9",
                            "transform": "scale(0.999) translateY(1px)",
                            "letter_spacing": "0.05em",
                        },
                        "100%": {
                            "filter": "blur(0px) brightness(1)",
                            "opacity": "1",
                            "transform": "scale(1) translateY(0px)",
                            "letter_spacing": "normal",
                        }
                    }
                }
            ),
        
        rx.hstack(
            rx.spacer(),
            rx.hstack(
                rx.switch(
                    checked=FileStorageState.auto_refresh_enabled,
                    on_change=FileStorageState.set_auto_refresh_enabled,
                    color_scheme="cyan",
                    size="2",
                ),
                rx.text("Auto-refresh", size="2", color="gray.400"),
                spacing="2",
                align="center",
            ),
            file_upload_modal(),
            width="100%",
            align="center",
            margin_bottom="2em",
            spacing="4",
        ),
        
        
        # Main content area with directory tree and files
        rx.hstack(
            # Left sidebar - Enhanced directory tree
            rx.box(
                react_directory_tree(),
                width="400px",  # Increased width
                min_width="350px",  # Minimum width
                height="calc(100vh - 250px)",  # Account for header and padding
                overflow_y="auto",  # Changed to auto to allow scrolling
                position="relative",  # Ensure z-index works
                style={"flex_shrink": "0"},
            ),
            
            # Right content - Files
            rx.vstack(
                # Enhanced breadcrumbs
                rx.box(
                    simple_breadcrumbs(),
                    width="100%",
                    padding="0.5rem 1rem",
                    background="rgba(0, 0, 0, 0.2)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="md",
                    margin_bottom="1rem",
                ),
                
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Files", size="5", color="white"),
                            rx.spacer(),
                            rx.text(
                                rx.cond(
                                    FileStorageState.files.length() > 0,
                                    FileStorageState.files.length().to_string() + " files",
                                    "No files"
                                ),
                                color="gray.400",
                                size="2",
                            ),
                            width="100%",
                            align="center",
                            margin_bottom="1em",
                        ),
                        
                        rx.cond(
                            FileStorageState.loading_files,
                            rx.center(
                                rx.spinner(size="3"),
                                padding="4em",
                            ),
                            rx.cond(
                                FileStorageState.files.length() > 0,
                                rx.vstack(
                                    rx.foreach(
                                        FileStorageState.files,
                                        file_list_item,
                                    ),
                                    width="100%",
                                    spacing="2",
                                ),
                                rx.center(
                                    rx.vstack(
                                        rx.icon("file-x", size=48, color="gray.600"),
                                        rx.text(
                                            "No files in this directory",
                                            color="gray.500",
                                            size="3",
                                        ),
                                        rx.text(
                                            "Upload files or navigate to a different directory",
                                            color="gray.600",
                                            size="2",
                                        ),
                                        spacing="2",
                                        align="center",
                                    ),
                                    padding="4em",
                                    width="100%",
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    **CARD_STYLE,
                    width="100%",
                ),
                width="100%",
                spacing="4",
            ),
            
            width="100%",
            spacing="4",
            align="start",
        ),
        
        # Load files and directories when page loads
        on_mount=[
            DirectoryState.load_directory_tree,
            FileStorageState.load_files,
        ],
            
        # Page positioning - match Dashboard structure
        spacing="6",
        align="start",
        width="100%",
        padding="3em",
        padding_top="4em",
        position="absolute",
        top="0",
        left="0",
        right="0",
        min_height="100vh",
        z_index="10",
    )