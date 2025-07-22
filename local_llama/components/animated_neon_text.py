"""Animated neon text component with glowing border effect."""
import reflex as rx


def animated_neon_text(text: str, color: str = "#06b6d4", size: str = "2rem", delay: float = 0) -> rx.Component:
    """Create animated neon text with a glowing border that traces around the letters."""
    animation_name = f"neon_trace_{hash(text + str(delay))}"
    
    return rx.box(
        rx.text(
            text,
            style={
                "font_size": size,
                "font_weight": "800",
                "letter_spacing": "0.02em",
                "color": "transparent",
                "background": f"linear-gradient(135deg, {color} 0%, rgba(156, 163, 175, 0.8) 50%, {color} 100%)",
                "background_clip": "text",
                "-webkit-background-clip": "text",
                "-webkit-text-fill-color": "transparent",
                "position": "relative",
                "text_shadow": f"""
                    0 0 3px {color}40,
                    0 0 6px {color}20
                """,
                "animation": f"{animation_name} 4s ease-in-out infinite",
                "animation_delay": f"{delay}s",
            }
        ),
        rx.text(
            text,
            style={
                "font_size": size,
                "font_weight": "800",
                "letter_spacing": "0.02em",
                "color": "transparent",
                "-webkit-text-stroke": f"1px {color}",
                "text_stroke": f"1px {color}",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "filter": f"""
                    drop-shadow(0 0 2px {color}40)
                    drop-shadow(0 0 4px {color}20)
                """,
                "opacity": "0",
                "animation": f"{animation_name}_stroke 4s ease-in-out infinite",
                "animation_delay": f"{delay}s",
            }
        ),
        position="relative",
        display="inline-block",
        style={
            "@keyframes " + animation_name: {
                "0%, 100%": {
                    "filter": f"brightness(1) drop-shadow(0 0 4px {color}30)",
                },
                "50%": {
                    "filter": f"brightness(1.1) drop-shadow(0 0 6px {color}40)",
                }
            },
            "@keyframes " + animation_name + "_stroke": {
                "0%, 100%": {
                    "opacity": "0.2",
                    "filter": f"""
                        drop-shadow(0 0 2px {color}30)
                        drop-shadow(0 0 3px {color}20)
                    """,
                },
                "50%": {
                    "opacity": "0.4",
                    "filter": f"""
                        drop-shadow(0 0 3px {color}40)
                        drop-shadow(0 0 5px {color}30)
                    """,
                }
            }
        }
    )


def animated_neon_stat(name: str, value: str | rx.Var, color: str = "#06b6d4", delay: float = 0) -> rx.Component:
    """Create an animated neon stat with name and value."""
    return rx.vstack(
        rx.text(
            name,
            style={
                "color": "rgba(156, 163, 175, 0.8)",
                "font_size": "0.875rem",
                "font_weight": "500",
                "text_transform": "uppercase",
                "letter_spacing": "0.05em",
                "margin_bottom": "0.5rem",
            }
        ),
        animated_neon_text(
            text=value if isinstance(value, str) else value.to_string(),
            color=color,
            size="2.5rem",
            delay=delay
        ),
        spacing="2",
        align="center",
    )