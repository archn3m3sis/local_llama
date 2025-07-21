"""Virtual Machine Creation Page."""
import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.vm_creation_form import vm_creation_form
from ..components.vm_creation_table import vm_creation_table
from ..states.vm_creation_state import VMCreationState
from ..states.vm_creation_table_state import VMCreationTableState

def VMCreation() -> rx.Component:
    """Virtual Machine Creation page component."""
    return rx.vstack(
        # Massive metallic title matching other pages
        metallic_title("IAMS - Virtual Machine Creation"),
        
        # Content area
        rx.vstack(
            rx.text(
                "Log new virtual machine deployments and track their operational status", 
                color="gray.400", 
                font_size="1.1rem",
                margin_bottom="2em",
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
            
            # Tab Navigation with Action Buttons
            rx.hstack(
                # Left side - navigation buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="plus", size=20),
                            rx.text("New VM"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%)",
                            "border": "1px solid rgba(16, 185, 129, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.2) 100%)",
                                "border": "1px solid rgba(16, 185, 129, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(16, 185, 129, 0.2)",
                            },
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="list", size=20),
                            rx.text("View History"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(79, 70, 229, 0.1) 100%)",
                            "border": "1px solid rgba(99, 102, 241, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(79, 70, 229, 0.2) 100%)",
                                "border": "1px solid rgba(99, 102, 241, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(99, 102, 241, 0.2)",
                            },
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="bar_chart", size=20),
                            rx.text("Analytics"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(245, 101, 101, 0.15) 0%, rgba(239, 68, 68, 0.1) 100%)",
                            "border": "1px solid rgba(245, 101, 101, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(245, 101, 101, 0.25) 0%, rgba(239, 68, 68, 0.2) 100%)",
                                "border": "1px solid rgba(245, 101, 101, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(245, 101, 101, 0.2)",
                            },
                        }
                    ),
                    spacing="3",
                ),
                
                # Right side - action buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="rotate_ccw", size=20),
                            rx.text("Reset Form"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=VMCreationState.reset_form,
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(148, 163, 184, 0.15) 0%, rgba(100, 116, 139, 0.1) 100%)",
                            "border": "1px solid rgba(148, 163, 184, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(148, 163, 184, 0.25) 0%, rgba(100, 116, 139, 0.2) 100%)",
                                "border": "1px solid rgba(148, 163, 184, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(148, 163, 184, 0.2)",
                            },
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="check", size=20),
                            rx.text("Create VM"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=VMCreationState.submit_vm_creation,
                        size="3",
                        disabled=rx.cond(
                            VMCreationState.is_form_valid,
                            False,
                            True
                        ),
                        style={
                            "background": rx.cond(
                                VMCreationState.is_form_valid,
                                "linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.15) 100%)",
                                "linear-gradient(135deg, rgba(75, 85, 99, 0.15) 0%, rgba(55, 65, 81, 0.1) 100%)"
                            ),
                            "border": rx.cond(
                                VMCreationState.is_form_valid,
                                "1px solid rgba(59, 130, 246, 0.3)",
                                "1px solid rgba(75, 85, 99, 0.25)"
                            ),
                            "color": "white",
                            "font_weight": "600",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": rx.cond(
                                VMCreationState.is_form_valid,
                                {
                                    "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.25) 100%)",
                                    "border": "1px solid rgba(59, 130, 246, 0.4)",
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 4px 16px rgba(59, 130, 246, 0.3)",
                                },
                                {}
                            ),
                            "_disabled": {
                                "background": "linear-gradient(135deg, rgba(75, 85, 99, 0.1) 0%, rgba(55, 65, 81, 0.05) 100%)",
                                "border": "1px solid rgba(75, 85, 99, 0.2)",
                                "color": "rgba(255, 255, 255, 0.4)",
                                "cursor": "not-allowed",
                                "transform": "none",
                                "box_shadow": "none",
                            },
                        }
                    ),
                    spacing="3",
                ),
                
                justify="between",
                align="center",
                width="90%",
                max_width="1400px",
                margin="0 auto 2rem auto",
                padding="0 2rem",
            ),
            
            # VM Creation Form
            vm_creation_form(),
            
            # VM Creation Table
            vm_creation_table(),
            
            spacing="4",
            align="start",
            width="100%",
        ),
        
        spacing="0",
        align="start",
        width="100%",
        height="100vh",
        padding="3em",
        padding_top="2em",
        padding_bottom="10rem",
        overflow_y="auto",
        position="absolute",
        top="0",
        left="0",
        z_index="10",
    )