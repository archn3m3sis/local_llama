"""Dashboard statistics components."""
import reflex as rx


def stat_card(title: str, value: rx.Var | str | int, icon: str, color: str) -> rx.Component:
    """Create a statistics card with glassmorphism effect."""
    # Convert value to string properly if it's a Var
    if isinstance(value, rx.Var):
        display_value = value.to_string()
    else:
        display_value = str(value)
        
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag=icon,
                    size=24,
                    style={
                        "color": color,
                        "filter": f"drop-shadow(0 0 10px {color})"
                    }
                ),
                rx.text(
                    title,
                    style={
                        "color": "rgba(156, 163, 175, 0.9)",
                        "font_size": "0.875rem",
                        "font_weight": "500",
                        "text_transform": "uppercase",
                        "letter_spacing": "0.05em"
                    }
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.text(
                display_value,
                style={
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "2.5rem",
                    "font_weight": "700",
                    "line_height": "1",
                    "background": f"linear-gradient(135deg, {color} 0%, rgba(255, 255, 255, 0.9) 100%)",
                    "background_clip": "text",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "filter": f"drop-shadow(0 0 20px {color})"
                }
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        style={
            "background": "rgba(17, 24, 39, 0.6)",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(55, 65, 81, 0.5)",
            "border_radius": "12px",
            "padding": "1.5rem",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": "rgba(17, 24, 39, 0.8)",
                "border_color": color,
                "transform": "translateY(-2px)",
                "box_shadow": f"0 12px 40px rgba(0, 0, 0, 0.4), 0 0 20px {color}20"
            }
        }
    )


def stats_grid(stats: list[dict]) -> rx.Component:
    """Create a grid of statistics cards."""
    return rx.grid(
        *[
            stat_card(
                title=stat["title"],
                value=stat["value"],
                icon=stat["icon"],
                color=stat["color"]
            )
            for stat in stats
        ],
        columns=rx.breakpoints(default="1", sm="2", md="4"),
        spacing="4",
        width="100%",
    )