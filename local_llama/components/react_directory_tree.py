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
                    transition: all 0.2s ease;
                }
                .file-tree__item:hover {
                    background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
                    transform: translateX(2px);
                }
                
                /* Custom directory colors based on data attributes */
                .file-tree__item[data-uri*="/personal"] .file-tree__item-name {
                    color: #60A5FA;  /* Blue */
                }
                .file-tree__item[data-uri*="/shared"] .file-tree__item-name {
                    color: #34D399;  /* Green */
                }
                .file-tree__item[data-uri*="/projects"] .file-tree__item-name {
                    color: #F59E0B;  /* Amber */
                }
                .file-tree__item[data-uri*="/archive"] .file-tree__item-name {
                    color: #9CA3AF;  /* Gray */
                }
                .file-tree__item[data-uri*="/templates"] .file-tree__item-name {
                    color: #A78BFA;  /* Purple */
                }
                .file-tree__item[data-uri*="/reports"] .file-tree__item-name {
                    color: #F87171;  /* Red */
                }
                .file-tree__item[data-uri*="/documentation"] .file-tree__item-name {
                    color: #FBBF24;  /* Yellow */
                }
                .file-tree__item[data-uri*="/media"] .file-tree__item-name {
                    color: #EC4899;  /* Pink */
                }
                
                /* Icon colors */
                .file-tree__item[data-uri*="/personal"] .file-tree__item-icon {
                    color: #60A5FA;
                    filter: drop-shadow(0 0 8px #60A5FA40);
                }
                .file-tree__item[data-uri*="/shared"] .file-tree__item-icon {
                    color: #34D399;
                    filter: drop-shadow(0 0 8px #34D39940);
                }
                .file-tree__item[data-uri*="/projects"] .file-tree__item-icon {
                    color: #F59E0B;
                    filter: drop-shadow(0 0 8px #F59E0B40);
                }
                .file-tree__item[data-uri*="/archive"] .file-tree__item-icon {
                    color: #9CA3AF;
                }
                .file-tree__item[data-uri*="/templates"] .file-tree__item-icon {
                    color: #A78BFA;
                    filter: drop-shadow(0 0 8px #A78BFA40);
                }
                .file-tree__item[data-uri*="/reports"] .file-tree__item-icon {
                    color: #F87171;
                    filter: drop-shadow(0 0 8px #F8717140);
                }
                .file-tree__item[data-uri*="/documentation"] .file-tree__item-icon {
                    color: #FBBF24;
                    filter: drop-shadow(0 0 8px #FBBF2440);
                }
                .file-tree__item[data-uri*="/media"] .file-tree__item-icon {
                    color: #EC4899;
                    filter: drop-shadow(0 0 8px #EC489940);
                }
                
                /* Enhanced tree styling */
                .file-tree__list {
                    padding-left: 1.5rem;
                }
                .file-tree__item-arrow {
                    color: #6B7280;
                    transition: transform 0.2s ease;
                }
                .file-tree__item-arrow--expanded {
                    transform: rotate(90deg);
                }
                .file-tree__item-name {
                    font-family: 'Inter', system-ui, sans-serif;
                    font-weight: 500;
                    font-size: 0.9rem;
                }
            </style>
        '''),
        
        # Header
        rx.hstack(
            rx.heading(
                "Directories", 
                size="4", 
                style={
                    "background": "linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%)",
                    "background_clip": "text",
                    "-webkit-background-clip": "text",
                    "color": "transparent",
                    "font_weight": "600",
                }
            ),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh-cw", size=14),
                size="1",
                on_click=DirectoryState.load_directory_tree,
                title="Refresh",
                style={
                    "background": "rgba(96, 165, 250, 0.1)",
                    "color": "#60A5FA",
                    "border": "1px solid rgba(96, 165, 250, 0.2)",
                    "cursor": "pointer",
                    "transition": "all 0.2s ease",
                    "_hover": {
                        "background": "rgba(96, 165, 250, 0.2)",
                        "border_color": "rgba(96, 165, 250, 0.4)",
                        "transform": "rotate(180deg)",
                    }
                },
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        rx.vstack(
            rx.text(
                DirectoryState.directory_count,
                size="2", 
                color="gray.400",
            ),
            rx.text(
                f"Files Discovered: {DirectoryState.total_file_count}",
                size="2",
                color="gray.400",
            ),
            spacing="1",
            margin_bottom="1rem",
        ),
        
        # React File Tree component - simplified container
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
                    width="100%",
                    max_height="400px",  # Changed from height to max_height
                    min_height="200px",  # Added min_height
                    overflow_y="auto",
                    overflow_x="auto",
                    padding="1rem",
                    margin_bottom="1rem",
                    style={
                        "background": "rgba(255, 255, 255, 0.02)",
                        "border": "1px solid rgba(255, 255, 255, 0.08)",
                        "border_radius": "0.75rem",
                    },
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
        
        # Create button - always visible at bottom
        rx.button(
            rx.icon("folder-plus", size=16),
            "New Directory",
            size="2",
            width="100%",
            on_click=DirectoryState.set_creating_directory(True),
            style={
                "background": "rgba(59, 130, 246, 0.1)",
                "color": "#3B82F6",
                "border": "1px solid rgba(59, 130, 246, 0.2)",
                "cursor": "pointer",
                "font_weight": "500",
                "transition": "all 0.2s ease",
                "_hover": {
                    "background": "rgba(59, 130, 246, 0.2)",
                    "border_color": "rgba(59, 130, 246, 0.4)",
                    "transform": "translateY(-1px)",
                    "box_shadow": "0 4px 12px rgba(59, 130, 246, 0.15)",
                }
            }
        ),
        
        # Load directories on mount
        on_mount=[
            DirectoryState.load_directory_tree,
            DirectoryState.initialize_expanded_directories,
        ],
        
        width="100%",
        height="100%",  # Take full height of parent
        spacing="2",
        overflow="hidden",  # Prevent overflow from vstack
    )