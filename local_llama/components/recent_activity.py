"""Recent activity components for dashboard."""
import reflex as rx
from .shared_styles import CARD_STYLE


def activity_item(activity: dict) -> rx.Component:
    """Create a single activity item."""
    # Determine icon and color based on activity type
    icon_map = {
        "Vm Created": ("server", "#10b981"),
        "Image Captured": ("camera", "#06b6d4"),
        "Log Added": ("file_text", "#a78bfa"),
        "Dat Updated": ("shield", "#f59e0b"),
        "Vm Updated": ("edit", "#10b981"),
    }
    
    icon, color = icon_map.get(activity["type"], ("activity", "#6b7280"))
    
    return rx.hstack(
        rx.box(
            rx.icon(
                tag=icon,
                size=16,
                style={
                    "color": color,
                }
            ),
            style={
                "width": "32px",
                "height": "32px",
                "background": f"{color}20",
                "border_radius": "8px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "flex_shrink": "0",
            }
        ),
        rx.vstack(
            rx.hstack(
                rx.text(
                    activity["employee"],
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_weight": "600",
                        "font_size": "0.875rem",
                    }
                ),
                rx.text(
                    activity["timestamp"],
                    style={
                        "color": "rgba(156, 163, 175, 0.7)",
                        "font_size": "0.75rem",
                    }
                ),
                spacing="2",
                width="100%",
                justify="between",
            ),
            rx.text(
                activity["description"],
                style={
                    "color": "rgba(156, 163, 175, 0.9)",
                    "font_size": "0.813rem",
                    "line_height": "1.4",
                }
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding="0.75rem",
        style={
            "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
            "_hover": {
                "background": "rgba(55, 65, 81, 0.2)",
            }
        }
    )


def recent_activity_panel(activities: list[dict]) -> rx.Component:
    """Create the recent activity panel."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="activity",
                    size=20,
                    style={
                        "color": "#10b981",
                        "filter": "drop-shadow(0 0 10px #10b981)"
                    }
                ),
                rx.text(
                    "Recent Activity",
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_size": "1.125rem",
                        "font_weight": "600",
                    }
                ),
                spacing="3",
                align="center",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(activities, activity_item),
                    spacing="0",
                    width="100%",
                ),
                style={
                    "height": "335px",
                    "width": "100%",
                    "overflow_y": "auto",
                }
            ),
            spacing="4",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "height": "fit-content",
        }
    )