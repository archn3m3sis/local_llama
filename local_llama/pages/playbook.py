import reflex as rx
from ..components.metallic_text import metallic_title, metallic_text

def Playbook() -> rx.Component:
    return rx.vstack(
        # Massive metallic title matching dashboard style
        metallic_title("Playbooks"),

        # Content area
        rx.vstack(
            rx.text(
                "Documentation and Playbooks", 
                color="gray.300", 
                font_size="1.35rem",
                font_weight="500",
                line_height="1.3",
            ),
            rx.text(
                "Comprehensive operational procedures, SOPs, and technical documentation library.", 
                color="gray.400", 
                font_size="1.1rem",
                margin_top="1em",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),

        spacing="0",
        align="start",
        width="100%",
        height="90vh",
        padding="3em",
        padding_top="2em",
        # Absolute positioning to match dashboard
        position="absolute",
        top="0",
        left="0",
        z_index="10",
    )