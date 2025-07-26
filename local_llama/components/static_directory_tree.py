"""Static directory tree that renders all directories."""
import reflex as rx
from ..states.directory_state import DirectoryState
from ..states.file_storage_state import FileStorageState


def directory_item(name: str, directory_id: int, full_path: str, depth: int, file_count: int = 0) -> rx.Component:
    """Render a single directory item."""
    return rx.hstack(
        rx.icon("folder", size=18, color="blue.400"),
        rx.text(
            name,
            size="2",
            weight="medium",
            color="white",
        ),
        rx.cond(
            file_count > 0,
            rx.text(
                f" ({file_count})",
                size="1",
                color="gray.400",
            ),
        ),
        spacing="2",
        align="center",
        width="100%",
        padding="0.5rem",
        padding_left=f"{depth * 20 + 8}px",
        border_radius="md",
        cursor="pointer",
        on_click=[
            DirectoryState.set_selected_directory_id(directory_id),
            FileStorageState.set_current_directory_id(directory_id),
            FileStorageState.set_current_directory_path(full_path),
            FileStorageState.load_files(),
        ],
        _hover={
            "background": "rgba(59, 130, 246, 0.1)",
        },
    )


def static_directory_tree() -> rx.Component:
    """Static directory tree that displays all directories."""
    # Manually create the tree structure based on what we know is in the database
    return rx.vstack(
        # Header
        rx.hstack(
            rx.heading("Directories", size="4", color="white"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("refresh-cw", size=14),
                size="1",
                variant="soft",
                on_click=DirectoryState.load_directory_tree,
                title="Refresh",
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        rx.text(
            DirectoryState.directory_count,
            size="2", 
            color="gray.400",
            margin_bottom="1rem",
        ),
        
        # Directory tree - manually structured
        rx.scroll_area(
            rx.vstack(
                # Root
                directory_item("playbook", 6, "/playbook", 0),
                
                # Personal
                directory_item("playbook_personal", 7, "/playbook/playbook_personal", 1),
                directory_item("pbper_drafts", 8, "/playbook/playbook_personal/pbper_drafts", 2),
                directory_item("pbper_templates", 9, "/playbook/playbook_personal/pbper_templates", 2),
                directory_item("pbper_published", 10, "/playbook/playbook_personal/pbper_published", 2),
                directory_item("pbper_fs", 11, "/playbook/playbook_personal/pbper_fs", 2),
                
                # Public
                directory_item("playbook_public", 12, "/playbook/playbook_public", 1),
                directory_item("pbpub_wips", 13, "/playbook/playbook_public/pbpub_wips", 2),
                directory_item("pbpub_templates", 14, "/playbook/playbook_public/pbpub_templates", 2),
                
                # Articles
                directory_item("pbpub_articles", 15, "/playbook/playbook_public/pbpub_articles", 2),
                directory_item("networking", 24, "/playbook/playbook_public/pbpub_articles/networking", 3),
                directory_item("cybersecurity", 25, "/playbook/playbook_public/pbpub_articles/cybersecurity", 3),
                directory_item("development", 26, "/playbook/playbook_public/pbpub_articles/development", 3),
                directory_item("career_development", 27, "/playbook/playbook_public/pbpub_articles/career_development", 3),
                directory_item("emerging_tech", 28, "/playbook/playbook_public/pbpub_articles/emerging_tech", 3),
                directory_item("hardware", 29, "/playbook/playbook_public/pbpub_articles/hardware", 3),
                directory_item("software", 30, "/playbook/playbook_public/pbpub_articles/software", 3),
                
                # Documentation
                directory_item("pbpub_documentation", 16, "/playbook/playbook_public/pbpub_documentation", 2),
                directory_item("incident_response", 17, "/playbook/playbook_public/pbpub_documentation/incident_response", 3),
                directory_item("maintenance", 18, "/playbook/playbook_public/pbpub_documentation/maintenance", 3),
                directory_item("compliance", 19, "/playbook/playbook_public/pbpub_documentation/compliance", 3),
                directory_item("emergency", 20, "/playbook/playbook_public/pbpub_documentation/emergency", 3),
                directory_item("security", 21, "/playbook/playbook_public/pbpub_documentation/security", 3),
                directory_item("standard_operating_procedures", 22, "/playbook/playbook_public/pbpub_documentation/standard_operating_procedures", 3),
                directory_item("training", 23, "/playbook/playbook_public/pbpub_documentation/training", 3),
                
                spacing="1",
                width="100%",
            ),
            height="calc(100vh - 400px)",
            min_height="300px",
            scrollbars="vertical",
        ),
        
        # Create button
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
        padding="1.5rem",
        background="rgba(0, 0, 0, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="xl",
        spacing="4",
    )