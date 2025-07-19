import reflex as rx
import reflex_type_animation as ta
from ..components.metallic_text import metallic_title, metallic_text

def Dashboard() -> rx.Component:
    return rx.vstack(
        # Massive 3D chrome metallic title - xAI Colossus style
        metallic_title("Industrial Cyber Dashboard"),

        # Dashboard content area
        rx.vstack(
            rx.box(
                ta.type_animation(
                    sequence=[
                        "Welcome to the Industrial Asset Management System",
                        2000,
                        "Advanced Cybersecurity Asset Tracking", 
                        2000,
                        "Next Generation Industrial Protection",
                        2000,
                        "Real-Time Asset Intelligence Platform",
                        2000,
                    ],
                    wrapper="span",
                    cursor=True,
                    repeat=True,
                    speed=50,
                    style={
                        "color": "rgb(156, 163, 175)",  # gray.300 equivalent
                        "font_size": "1.35rem",
                        "font_weight": "500",
                        "line_height": "1.3",
                        "text_align": "left",
                        "display": "block",
                        "min_height": "1.8rem",  # Prevent layout shift
                        "transition": "text-shadow 0.8s ease-in-out",
                        "animation": "fadeInShadow 3s ease-in-out infinite"
                    }
                ),
                # Add CSS animation for whispy shadow effect
                rx.html("""
                <style>
                    @keyframes fadeInShadow {
                        0%, 70% {
                            text-shadow: none;
                        }
                        85% {
                            text-shadow: 
                                0 0 15px rgba(156, 163, 175, 0.5),
                                0 0 25px rgba(156, 163, 175, 0.35),
                                0 0 35px rgba(156, 163, 175, 0.25),
                                0 0 45px rgba(156, 163, 175, 0.15);
                        }
                        100% {
                            text-shadow: 
                                0 0 20px rgba(156, 163, 175, 0.6),
                                0 0 30px rgba(156, 163, 175, 0.4),
                                0 0 40px rgba(156, 163, 175, 0.3),
                                0 0 50px rgba(156, 163, 175, 0.2),
                                0 0 60px rgba(156, 163, 175, 0.1);
                        }
                    }
                </style>
                """),
            ),

            spacing="4",
            align="start",  # Changed from center to left
            width="100%",
        ),

        spacing="0",
        align="start",  # Changed from center to left
        width="100%",
        height="90vh",
        padding="3em",  # Increased padding for better spacing
        padding_top="4em",  # More space from top to position text lower
        # Absolute positioning to bypass container issues
        position="absolute",
        top="0",
        left="0",
        z_index="10",
    )
