"""Enhanced directory tree component with proper nested structure support."""
import reflex as rx
from typing import Dict, List, Any, Optional
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def get_directory_icon(is_expanded: bool, is_system: bool) -> rx.Component:
    """Get appropriate icon for directory state."""
    return rx.cond(
        is_system,
        rx.cond(
            is_expanded,
            rx.icon("lock-open", size=16, color="gray.500"),
            rx.icon("lock", size=16, color="gray.500")
        ),
        rx.cond(
            is_expanded,
            rx.icon("folder-open", size=18, color="blue.400"),
            rx.icon("folder", size=18, color="blue.400")
        )
    )


def render_directory_node(node: Dict[str, Any], level: int = 0) -> rx.Component:
    """Render a single directory node with its children."""
    node_id = node["directory_id"]
    # Use the has_children flag that we'll add to the node data
    has_children = node.get("has_children", False)
    is_expanded = DirectoryState.expanded_directories.contains(node_id)
    is_current = FileStorageState.current_directory_id == node_id
    
    return rx.vstack(
        # Directory node
        rx.hstack(
            # Indentation
            rx.box(width=f"{level * 24}px"),
            
            # Expand/collapse chevron
            rx.cond(
                has_children,
                rx.icon_button(
                    rx.cond(
                        is_expanded,
                        rx.icon("chevron-down", size=14),
                        rx.icon("chevron-right", size=14)
                    ),
                    size="1",
                    variant="ghost",
                    on_click=DirectoryState.toggle_directory_expanded(node_id),
                    style={
                        "min_width": "20px",
                        "height": "20px",
                        "padding": "0",
                    }
                ),
                rx.box(width="20px")  # Spacer for alignment
            ),
            
            # Directory content
            rx.hstack(
                get_directory_icon(is_expanded, node.get("is_system_directory", False)),
                rx.text(
                    node["name"],
                    size="2",
                    weight="medium",
                    color=rx.cond(is_current, "blue.400", "white"),
                ),
                rx.cond(
                    node["file_count"] > 0,
                    rx.box(
                        rx.text(
                            node["file_count"],
                            size="1",
                            color="gray.400",
                        ),
                        padding="0 6px",
                        background="rgba(255, 255, 255, 0.1)",
                        border_radius="full",
                    ),
                ),
                spacing="2",
                align="center",
            ),
            
            width="100%",
            padding="4px 8px",
            border_radius="md",
            cursor="pointer",
            on_click=[
                DirectoryState.navigate_to_directory(node_id),
                FileStorageState.set_current_directory_id(node_id),
                FileStorageState.set_current_directory_path(node["full_path"]),
                FileStorageState.load_files(),
            ],
            _hover={
                "background": "rgba(59, 130, 246, 0.1)",
            },
            style={
                "background": rx.cond(
                    is_current,
                    "rgba(59, 130, 246, 0.15)",
                    "transparent"
                ),
                "border": rx.cond(
                    is_current,
                    "1px solid rgba(59, 130, 246, 0.3)",
                    "1px solid transparent"
                ),
            }
        ),
        
        # Children (rendered recursively when expanded)
        rx.cond(
            is_expanded & has_children,
            rx.vstack(
                rx.foreach(
                    node.get("children", []),
                    lambda child: render_directory_node(child, level + 1)
                ),
                spacing="0",
                width="100%",
            ),
        ),
        
        spacing="0",
        width="100%",
    )


def directory_breadcrumbs_v2() -> rx.Component:
    """Enhanced breadcrumb navigation with proper styling."""
    return rx.hstack(
        rx.icon("home", size=16, color="gray.400"),
        rx.text(
            "Root",
            size="2",
            color="gray.400",
            cursor="pointer",
            on_click=[
                FileStorageState.set_current_directory_id(None),
                FileStorageState.set_current_directory_path("/"),
                DirectoryState.load_directory_tree,
                FileStorageState.load_files,
            ],
            _hover={"color": "blue.400"},
        ),
        rx.foreach(
            DirectoryState.breadcrumbs,
            lambda crumb: rx.fragment(
                rx.icon("chevron-right", size=14, color="gray.600"),
                rx.text(
                    crumb["name"],
                    size="2",
                    color="gray.400",
                    cursor="pointer",
                    on_click=[
                        DirectoryState.navigate_to_directory(crumb["directory_id"]),
                        FileStorageState.set_current_directory_id(crumb["directory_id"]),
                        FileStorageState.set_current_directory_path(
                            DirectoryState.get_directory_path(crumb["directory_id"])
                        ),
                        FileStorageState.load_files(),
                    ],
                    _hover={"color": "blue.400"},
                ),
            ),
        ),
        spacing="1",
        align="center",
        padding="0.75rem 1rem",
    )


def directory_tree_v2() -> rx.Component:
    """Enhanced directory tree with proper nested structure."""
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    ~FileStorageState.current_directory_id.is_none(),
                    rx.icon_button(
                        rx.icon("arrow-up", size=14),
                        size="1",
                        variant="soft",
                        on_click=DirectoryState.navigate_to_parent,
                        title="Go to parent directory",
                    ),
                ),
                rx.icon_button(
                    rx.icon("refresh-cw", size=14),
                    size="1",
                    variant="soft",
                    on_click=DirectoryState.load_directory_tree,
                    title="Refresh directory tree",
                ),
                spacing="2",
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        # Tree content
        rx.cond(
            DirectoryState.loading_directories,
            rx.center(
                rx.spinner(size="3"),
                padding="4rem",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        DirectoryState.directory_tree,
                        lambda node: render_directory_node(node, 0)
                    ),
                    spacing="0",
                    width="100%",
                ),
                height="calc(100vh - 400px)",
                min_height="300px",
                scrollbars="vertical",
                style={
                    "& > div": {"width": "100%"},
                }
            ),
        ),
        
        # Actions
        rx.cond(
            ~FileStorageState.current_directory_id.is_none(),
            rx.cond(
                DirectoryState.can_create_in_directory(FileStorageState.current_directory_id),
                rx.button(
                    rx.icon("folder-plus", size=16),
                    "New Directory",
                    size="2",
                    variant="soft",
                    color_scheme="blue",
                    width="100%",
                    on_click=DirectoryState.set_creating_directory(True),
                ),
            ),
        ),
        
        width="100%",
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
    )


def create_directory_modal_v2() -> rx.Component:
    """Enhanced directory creation modal."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title(
                    rx.hstack(
                        rx.icon("folder-plus", size=20),
                        rx.text("Create New Directory"),
                        spacing="2",
                        align="center",
                    )
                ),
                
                rx.dialog.description(
                    rx.text(
                        "Create a new directory in: ",
                        rx.text(
                            FileStorageState.current_directory_path,
                            color="blue.400",
                            weight="medium",
                        ),
                        size="2",
                    )
                ),
                
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Directory Name"),
                        rx.input(
                            placeholder="Enter directory name",
                            value=DirectoryState.new_directory_name,
                            on_change=DirectoryState.set_new_directory_name,
                            auto_focus=True,
                        ),
                        name="directory_name",
                        width="100%",
                    ),
                    
                    rx.form.field(
                        rx.form.label("Description (optional)"),
                        rx.text_area(
                            placeholder="Enter a description for this directory",
                            value=DirectoryState.new_directory_description,
                            on_change=DirectoryState.set_new_directory_description,
                            rows="3",
                            resize="vertical",
                        ),
                        name="description",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("folder-plus", size=16),
                            "Create Directory",
                            color_scheme="blue",
                            on_click=DirectoryState.create_directory,
                            disabled=DirectoryState.new_directory_name.length() == 0,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="1rem",
                ),
                
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "500px",
                "background": "var(--gray-1)",
                "border": "1px solid var(--gray-4)",
            }
        ),
        open=DirectoryState.creating_directory,
    )