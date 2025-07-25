"""Playbook Editor page."""
import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.shared_styles import CARD_STYLE
from ..states.playbook_editor_state import PlaybookEditorState


def PlaybookEditor() -> rx.Component:
    """Playbook editor page."""
    return rx.vstack(
        metallic_title("Playbook Editor"),
        
        rx.text(
            "Create and edit playbooks for your operations.",
            color="gray.400",
            font_size="lg",
            margin_bottom="2rem",
        ),
        
        rx.box(
            rx.text(
                "Playbook editor coming soon...",
                color="gray.500",
                font_size="xl",
                text_align="center",
                padding="4rem",
            ),
            style=CARD_STYLE,
            width="100%",
        ),
        
        spacing="6",
        width="100%",
        padding="2rem",
        position="absolute",
        top="0",
        left="50%",
        transform="translateX(-50%)",
        max_width="1200px",
        min_height="100vh",
        z_index="10",
    )