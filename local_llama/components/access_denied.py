"""Neon glowing access denied component."""
import reflex as rx


def neon_access_denied() -> rx.Component:
    """A neon glowing access denied message that appears at the top of the screen."""
    return rx.box(
        rx.vstack(
            # Warning icon with pulsing glow
            rx.box(
                rx.icon(
                    "shield-alert", 
                    size=64,
                    style={
                        "color": "#FF0080",
                        "filter": "drop-shadow(0 0 30px #FF0080) drop-shadow(0 0 60px #FF0080)",
                        "animation": "pulse 2s ease-in-out infinite",
                        "@keyframes pulse": {
                            "0%, 100%": {
                                "transform": "scale(1)",
                                "filter": "drop-shadow(0 0 30px #FF0080) drop-shadow(0 0 60px #FF0080)",
                            },
                            "50%": {
                                "transform": "scale(1.1)",
                                "filter": "drop-shadow(0 0 40px #FF0080) drop-shadow(0 0 80px #FF0080)",
                            }
                        }
                    }
                ),
                margin_bottom="1rem",
            ),
            
            # Neon glowing title
            rx.heading(
                "ACCESS DENIED",
                size="8",
                style={
                    "background": "linear-gradient(45deg, #FF0080, #FF80FF, #00FFFF)",
                    "background_clip": "text",
                    "-webkit-background-clip": "text",
                    "color": "transparent",
                    "font_weight": "900",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.1em",
                    "text_shadow": "0 0 40px #FF0080",
                    "filter": "drop-shadow(0 0 20px #FF0080)",
                    "animation": "neonFlicker 3s ease-in-out infinite",
                    "@keyframes neonFlicker": {
                        "0%, 100%": {
                            "opacity": "1",
                            "filter": "drop-shadow(0 0 20px #FF0080) drop-shadow(0 0 40px #FF0080)",
                        },
                        "50%": {
                            "opacity": "0.8",
                            "filter": "drop-shadow(0 0 30px #FF0080) drop-shadow(0 0 60px #FF0080)",
                        }
                    }
                }
            ),
            
            # Glowing divider
            rx.box(
                height="2px",
                width="300px",
                style={
                    "background": "linear-gradient(90deg, transparent, #FF0080, #00FFFF, #FF0080, transparent)",
                    "box_shadow": "0 0 20px #FF0080, 0 0 40px #00FFFF",
                    "animation": "shimmer 3s linear infinite",
                    "@keyframes shimmer": {
                        "0%": {"background_position": "-300px"},
                        "100%": {"background_position": "300px"}
                    }
                },
                margin_y="1rem",
            ),
            
            # Authentication required message
            rx.text(
                "AUTHENTICATION REQUIRED",
                size="5",
                style={
                    "color": "#00FFFF",
                    "font_weight": "600",
                    "letter_spacing": "0.05em",
                    "text_shadow": "0 0 10px #00FFFF",
                }
            ),
            
            rx.text(
                "Please sign in to access this secure area",
                size="3",
                style={
                    "color": "rgba(255, 255, 255, 0.8)",
                    "margin_top": "0.5rem",
                }
            ),
            
            # Neon glowing button
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon("home", size=18),
                        rx.text("RETURN TO HOME"),
                        spacing="2",
                        align="center",
                    ),
                    size="3",
                    style={
                        "background": "linear-gradient(45deg, #FF0080, #FF80FF)",
                        "color": "white",
                        "font_weight": "700",
                        "letter_spacing": "0.05em",
                        "padding": "1rem 2rem",
                        "border": "2px solid transparent",
                        "border_radius": "50px",
                        "box_shadow": "0 0 20px #FF0080, inset 0 0 20px rgba(255, 255, 255, 0.2)",
                        "transition": "all 0.3s ease",
                        "cursor": "pointer",
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 0 30px #FF0080, 0 5px 20px rgba(255, 0, 128, 0.5), inset 0 0 30px rgba(255, 255, 255, 0.3)",
                            "border_color": "#FF80FF",
                        },
                        "_active": {
                            "transform": "translateY(0)",
                        }
                    }
                ),
                href="/",
                style={"text_decoration": "none"},
            ),
            
            spacing="4",
            align="center",
            justify="center",
        ),
        
        # Container positioning and styling
        position="fixed",
        top="20vh",
        left="50%",
        transform="translateX(-50%)",
        z_index="1000",
        padding="3rem",
        style={
            "background": "linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(40, 0, 60, 0.9) 100%)",
            "border": "2px solid",
            "border_image": "linear-gradient(45deg, #FF0080, #00FFFF) 1",
            "border_radius": "20px",
            "backdrop_filter": "blur(20px)",
            "box_shadow": "0 0 50px #FF0080, 0 0 100px rgba(255, 0, 128, 0.5), inset 0 0 50px rgba(255, 0, 128, 0.1)",
            "animation": "float 4s ease-in-out infinite",
            "@keyframes float": {
                "0%, 100%": {"transform": "translateX(-50%) translateY(0)"},
                "50%": {"transform": "translateX(-50%) translateY(-10px)"}
            }
        }
    )