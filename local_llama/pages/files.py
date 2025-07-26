import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.file_upload import file_upload_modal, file_list_item
from ..states.file_storage_state import FileStorageState
from ..states.directory_state import DirectoryState
from ..states.auth_state import AuthState
from ..components.shared_styles import CARD_STYLE
from ..components.simple_directory_tree import simple_breadcrumbs
from ..components.react_directory_tree import react_directory_tree
from ..components.access_restricted import access_restricted_message, upload_restriction_dialog
from ..components.directory_dialog import directory_creation_dialog


def upload_progress_overlay() -> rx.Component:
    """Upload progress overlay that shows during file upload."""
    return rx.cond(
        FileStorageState.uploading,
        rx.box(
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.icon(
                            "cloud_upload",
                            size=48,
                            style={
                                "color": "#60A5FA",
                                "filter": "drop-shadow(0 0 30px #60A5FA)",
                                "animation": "pulse 2s ease-in-out infinite",
                                "@keyframes pulse": {
                                    "0%, 100%": {"transform": "scale(1)", "opacity": "1"},
                                    "50%": {"transform": "scale(1.05)", "opacity": "0.8"}
                                }
                            }
                        ),
                    ),
                    rx.text(
                        FileStorageState.upload_status,
                        size="4",
                        weight="bold",
                        style={
                            "color": "white",
                            "text_shadow": "0 0 20px rgba(0, 0, 0, 0.5)",
                        }
                    ),
                    rx.box(
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
                        width="400px",
                        height="8px",
                        style={
                            "background": "rgba(255, 255, 255, 0.1)",
                            "border_radius": "1rem",
                            "overflow": "hidden",
                            "box_shadow": "inset 0 0 10px rgba(0, 0, 0, 0.3)",
                        },
                        margin_top="1rem",
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        FileStorageState.upload_progress.to_string() + "%",
                        size="6",
                        weight="bold",
                        style={
                            "color": "#60A5FA",
                            "text_shadow": "0 0 10px #60A5FA40",
                        }
                    ),
                    # Add close button for test overlay
                    rx.button(
                        "Close",
                        on_click=FileStorageState.close_upload_overlay,
                        size="2",
                        style={
                            "margin_top": "1rem",
                            "background": "rgba(239, 68, 68, 0.2)",
                            "border": "1px solid rgba(239, 68, 68, 0.4)",
                            "color": "#F87171",
                            "_hover": {
                                "background": "rgba(239, 68, 68, 0.3)",
                                "border_color": "rgba(239, 68, 68, 0.6)",
                            }
                        }
                    ),
                    spacing="4",
                    align="center",
                    padding="2rem",
                    style={
                        "background": "rgba(0, 0, 0, 0.8)",
                        "border": "2px solid rgba(96, 165, 250, 0.3)",
                        "border_radius": "1rem",
                        "backdrop_filter": "blur(10px)",
                        "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.5)",
                    }
                ),
                min_height="100vh",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="1000",
            style={
                "background": "rgba(0, 0, 0, 0.5)",
                "backdrop_filter": "blur(5px)",
            }
        )
    )

def initialize_user_data():
    """Initialize user data from AuthState on mount."""
    # First sync user data from AuthState
    return [
        DirectoryState.sync_user_from_auth,
        FileStorageState.sync_user_from_auth,
        DirectoryState.load_directory_tree,
        FileStorageState.load_files,
    ]


def Files() -> rx.Component:
    """File management page."""
    return rx.fragment(
        # Script to sync user data after Clerk loads
        rx.script("""
            setTimeout(() => {
                // Give Clerk time to load, then sync user data
                if (window.Clerk && window.Clerk.user) {
                    console.log('Clerk user loaded, syncing directory state...');
                    // Trigger a state sync
                    const event = new Event('clerk-user-loaded');
                    window.dispatchEvent(event);
                }
            }, 1000);
        """),
        upload_progress_overlay(),
        upload_restriction_dialog(),
        directory_creation_dialog(),
        rx.vstack(
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
        
        # Auto-refresh toggle and upload button
        rx.hstack(
            rx.spacer(),
            rx.box(
                rx.hstack(
                    rx.switch(
                        checked=FileStorageState.auto_refresh_enabled,
                        on_change=FileStorageState.set_auto_refresh_enabled,
                        color_scheme="cyan",
                        size="2",
                    ),
                    rx.text(
                        "Auto-refresh", 
                        size="2", 
                        style={
                            "color": "rgba(156, 163, 175, 0.9)",
                            "font_family": "Inter, system-ui, sans-serif",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                style={
                    "padding": "0.5rem 1rem",
                    "background": "rgba(96, 165, 250, 0.05)",
                    "border": "1px solid rgba(96, 165, 250, 0.15)",
                    "border_radius": "0.75rem",
                    "transition": "all 0.2s ease",
                    "_hover": {
                        "background": "rgba(96, 165, 250, 0.1)",
                        "border_color": "rgba(96, 165, 250, 0.25)",
                    }
                }
            ),
            # Debug buttons - remove after testing
            rx.button(
                "Test Overlay",
                on_click=FileStorageState.test_upload_overlay,
                size="1",
                variant="ghost",
                color_scheme="gray",
            ),
            rx.button(
                "Clear All Files",
                on_click=FileStorageState.clear_all_files,
                size="1",
                variant="ghost",
                color_scheme="red",
            ),
            file_upload_modal(),
            width="100%",
            align="center",
            margin_bottom="2em",
            spacing="3",
        ),
        
        # Main content area with directory tree and files
        rx.hstack(
            # Left sidebar - Directory tree
            rx.box(
                react_directory_tree(),
                width="400px",
                min_width="350px",
                max_height="calc(100vh - 250px)",
                style={
                    "flex_shrink": "0",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.08)",
                    "border_radius": "1rem",
                    "backdrop_filter": "blur(10px)",
                },
            ),
            
            # Right content - Files
            rx.vstack(
                # Enhanced breadcrumbs
                rx.box(
                    simple_breadcrumbs(),
                    width="100%",
                    padding="0.75rem 1.25rem",
                    style={
                        "background": "linear-gradient(135deg, rgba(96, 165, 250, 0.08) 0%, rgba(167, 139, 250, 0.08) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "0.75rem",
                        "backdrop_filter": "blur(10px)",
                        "margin_bottom": "1.5rem",
                    }
                ),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading(
                                "Files", 
                                size="5", 
                                style={
                                    "background": "linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%)",
                                    "background_clip": "text",
                                    "-webkit-background-clip": "text",
                                    "color": "transparent",
                                    "font_weight": "600",
                                }
                            ),
                            rx.spacer(),
                            rx.box(
                                rx.text(
                                    rx.cond(
                                        FileStorageState.files.length() > 0,
                                        FileStorageState.files.length().to_string() + " files",
                                        "No files"
                                    ),
                                    size="2",
                                    style={
                                        "color": "rgba(156, 163, 175, 0.9)",
                                        "font_family": "Inter, system-ui, sans-serif",
                                    }
                                ),
                                style={
                                    "padding": "0.25rem 1rem",
                                    "background": "rgba(96, 165, 250, 0.1)",
                                    "border": "1px solid rgba(96, 165, 250, 0.2)",
                                    "border_radius": "2rem",
                                }
                            ),
                            width="100%",
                            align="center",
                            margin_bottom="1.5em",
                        ),
                        
                        rx.cond(
                            FileStorageState.access_denied,
                            access_restricted_message(),
                            rx.cond(
                                FileStorageState.loading_files,
                                rx.center(
                                    rx.box(
                                        rx.spinner(
                                            size="3",
                                            color="cyan",
                                        ),
                                        style={
                                            "filter": "drop-shadow(0 0 20px #06B6D440)",
                                        }
                                    ),
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
                                            rx.box(
                                                rx.icon("file-x", size=48),
                                                style={
                                                    "color": "#9CA3AF",
                                                    "filter": "drop-shadow(0 0 20px #9CA3AF30)",
                                                }
                                            ),
                                            rx.text(
                                                "No files in this directory",
                                                size="3",
                                                style={
                                                    "color": "rgba(255, 255, 255, 0.7)",
                                                    "font_weight": "500",
                                                }
                                            ),
                                            rx.text(
                                                "Upload files or navigate to a different directory",
                                                size="2",
                                                style={
                                                    "color": "rgba(156, 163, 175, 0.7)",
                                                }
                                            ),
                                            spacing="3",
                                            align="center",
                                        ),
                                        padding="4em",
                                        width="100%",
                                    ),
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    style={
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "1rem",
                        "backdrop_filter": "blur(20px)",
                        "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2)",
                        "padding": "2rem",
                    },
                    width="100%",
                ),
                width="100%",
                spacing="4",
            ),
            
            width="100%",
            spacing="4",
            align="start",
        ),
        
        # Main page positioning - matching working pages
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
        on_mount=initialize_user_data,
    )
    )