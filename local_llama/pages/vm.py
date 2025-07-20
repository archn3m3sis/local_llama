import reflex as rx
from ..components.metallic_text import metallic_title, metallic_text
from ..components.vm_creation_form import vm_creation_form
from ..components.vm_table import vm_table
from ..states.vm_state import VMState

def VM() -> rx.Component:
    return rx.vstack(
        # Massive metallic title matching dashboard style
        metallic_title("IAMS - Virtual Machine Creation"),

        # Content area with tab system
        rx.vstack(
            rx.text(
                "Create and manage virtual machines for industrial systems & review VM deployment records", 
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
                            "opacity": "0.6",
                            "transform": "scale(0.998) translateY(3px)",
                            "letter_spacing": "0.1em",
                        },
                        "80%": {
                            "filter": "blur(1px) brightness(0.9)",
                            "opacity": "0.8",
                            "transform": "scale(0.999) translateY(1px)",
                            "letter_spacing": "0.05em",
                        },
                        "100%": {
                            "filter": "blur(0px) brightness(1)",
                            "opacity": "1",
                            "transform": "scale(1) translateY(0px)",
                            "letter_spacing": "0em",
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
                            "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.1) 100%)",
                            "border": "1px solid rgba(59, 130, 246, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.2) 100%)",
                                "border": "1px solid rgba(59, 130, 246, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(59, 130, 246, 0.2)",
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
                            "background": "linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%)",
                            "border": "1px solid rgba(139, 92, 246, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(124, 58, 237, 0.2) 100%)",
                                "border": "1px solid rgba(139, 92, 246, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(139, 92, 246, 0.2)",
                            },
                        }
                    ),
                    spacing="3",
                ),
                
                # Right side - form action buttons
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="send", size=18),
                            rx.text("Create VM"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        on_click=VMState.create_vm,
                        disabled=~VMState.form_is_valid,
                        style={
                            "background": rx.cond(
                                VMState.form_is_valid,
                                "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.15) 100%)",
                                "linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(75, 85, 99, 0.05) 100%)"
                            ),
                            "border": rx.cond(
                                VMState.form_is_valid,
                                "1px solid rgba(34, 197, 94, 0.3)",
                                "1px solid rgba(107, 114, 128, 0.2)"
                            ),
                            "color": rx.cond(VMState.form_is_valid, "white", "rgba(156, 163, 175, 0.8)"),
                            "font_weight": "500",
                            "border_radius": "12px",
                            "cursor": rx.cond(VMState.form_is_valid, "pointer", "not-allowed"),
                            "_hover": rx.cond(
                                VMState.form_is_valid,
                                {
                                    "background": "linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(22, 163, 74, 0.25) 100%)",
                                    "border": "1px solid rgba(34, 197, 94, 0.5)",
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 4px 16px rgba(34, 197, 94, 0.3)",
                                },
                                {}
                            ),
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="rotate_ccw", size=18),
                            rx.text("Reset Form"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        on_click=VMState.reset_form,
                        style={
                            "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%)",
                            "border": "1px solid rgba(239, 68, 68, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "12px",
                            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(220, 38, 38, 0.2) 100%)",
                                "border": "1px solid rgba(239, 68, 68, 0.4)",
                                "transform": "translateY(-1px)",
                                "box_shadow": "0 4px 16px rgba(239, 68, 68, 0.2)",
                            },
                        }
                    ),
                    spacing="3",
                ),
                
                width="100%",
                justify="between",
                align="center",
                margin_bottom="2rem",
            ),
            
            # Form and Table Container
            rx.vstack(
                # VM Creation Form
                vm_creation_form(),
                
                # VM Table
                vm_table(),
                
                spacing="3rem",
                width="100%",
            ),
            
            width="100%",
            max_width="100%",
            padding="0 2rem",
        ),
        
        spacing="2rem",
        width="100%",
        min_height="100vh",
        align="start",
    )