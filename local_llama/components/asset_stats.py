"""Asset statistics component for dashboard."""
import reflex as rx
from .animated_neon_text import animated_neon_text


def asset_stat_item(name_line1: str, name_line2: str, value: rx.Var | str, color: str = "#06b6d4", delay: float = 0, spacing: str = "5", margin_left: str = "0") -> rx.Component:
    """Create a single asset stat item with text on left and value on right."""
    return rx.hstack(
        rx.vstack(
            rx.text(
                name_line1,
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "400",
                    "line_height": "1.2",
                    "text_align": "right",
                }
            ),
            rx.text(
                name_line2,
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "400",
                    "line_height": "1.2",
                    "text_align": "right",
                }
            ),
            spacing="0",
            align="end",
            style={
                "margin_top": "-0.5rem",
                "margin_right": "0.75rem",
            }
        ),
        animated_neon_text(
            text=value if isinstance(value, str) else value.to_string(),
            color=color,
            size="3rem",
            delay=delay
        ),
        spacing=spacing,
        align="center",
        style={
            "flex": "1",
            "margin_left": margin_left,
        }
    )


def asset_stats_panel(total_assets: rx.Var[int], total_projects: rx.Var[int], total_operating_systems: rx.Var[int]) -> rx.Component:
    """Create the asset statistics panel without backdrop."""
    return rx.box(
        rx.hstack(
            asset_stat_item(
                name_line1="Total Number Of Standalone",
                name_line2="Industrial Assets:",
                value=total_assets,
                color="#ffffff",
                delay=0,
                spacing="3",
                margin_left="0"
            ),
            asset_stat_item(
                name_line1="Total Number Of Asset",
                name_line2="Parent Programs:",
                value=total_projects,
                color="#ffffff",
                delay=0.5,
                spacing="5",
                margin_left="0.5rem"
            ),
            asset_stat_item(
                name_line1="Total Number Unique",
                name_line2="Maintained Operating Systems:",
                value=total_operating_systems,
                color="#ffffff",
                delay=1,
                spacing="5",
                margin_left="-3.25rem"
            ),
            spacing="4",
            width="100%",
            justify="center",
        ),
        style={
            "position": "absolute",
            "top": "4rem",
            "left": "59%",
            "transform": "translateX(-50%)",
            "width": "auto",
            "z_index": "15",
        }
    )