"""Dashboard statistics components."""
import reflex as rx
from .shared_styles import get_card_style_with_hover


def stat_card(title: str, value: rx.Var | str | int, icon: str, color: str, 
              comparison_percent: rx.Var | float = None, comparison_count: rx.Var | int = None) -> rx.Component:
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
            # Comparison text in bottom right
            rx.cond(
                comparison_percent is not None,
                rx.vstack(
                    rx.text(
                        rx.cond(
                            comparison_percent >= 0,
                            "↑ " + comparison_percent.to(str) + "% over last month",
                            "↓ " + (-comparison_percent).to(str) + "% over last month"
                        ),
                        style={
                            "color": rx.cond(
                                comparison_percent >= 0,
                                "#06b6d4",
                                "#ec4899"
                            ),
                            "font_size": "0.7rem",
                            "font_weight": "600",
                            "filter": rx.cond(
                                comparison_percent >= 0,
                                "drop-shadow(0 0 8px #06b6d4)",
                                "drop-shadow(0 0 8px #ec4899)"
                            ),
                        }
                    ),
                    rx.text(
                        rx.cond(
                            comparison_count >= 0,
                            "↑ " + comparison_count.to(str) + " actions over last month",
                            "↓ " + (-comparison_count).to(str) + " actions over last month"
                        ),
                        style={
                            "color": rx.cond(
                                comparison_count >= 0,
                                "#06b6d4",
                                "#ec4899"
                            ),
                            "font_size": "0.7rem",
                            "font_weight": "600",
                            "filter": rx.cond(
                                comparison_count >= 0,
                                "drop-shadow(0 0 8px #06b6d4)",
                                "drop-shadow(0 0 8px #ec4899)"
                            ),
                        }
                    ),
                    spacing="0",
                    align="end",
                    position="absolute",
                    bottom="1rem",
                    right="1rem",
                ),
                rx.fragment()
            ),
            spacing="3",
            align="start",
            width="100%",
            position="relative",
        ),
        style={
            **get_card_style_with_hover(color),
            "padding": "1.5rem",
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
                color=stat["color"],
                comparison_percent=stat.get("comparison_percent"),
                comparison_count=stat.get("comparison_count")
            )
            for stat in stats
        ],
        columns=rx.breakpoints({
            "initial": "1",
            "sm": "2", 
            "md": "4"
        }),
        spacing="4",
        width="100%",
    )