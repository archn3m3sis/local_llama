"""Asset view details modal component."""
import reflex as rx
from typing import Dict, List, Any
from ..states.assets_state import AssetsState


def action_history_row(action: Dict[str, Any]) -> rx.Component:
    """Create a row for action history."""
    return rx.hstack(
        rx.box(
            rx.icon(
                tag="activity",
                size=16,
                style={
                    "color": "#06b6d4",
                    "filter": "drop-shadow(0 0 4px #06b6d4)",
                }
            ),
            style={
                "padding": "0.5rem",
                "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
                "border_radius": "8px",
            }
        ),
        rx.vstack(
            rx.hstack(
                rx.text(
                    action["action"],
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_weight": "600",
                        "font_size": "0.875rem",
                    }
                ),
                rx.spacer(),
                rx.text(
                    action["date"],
                    style={
                        "color": "rgba(156, 163, 175, 0.8)",
                        "font_size": "0.75rem",
                    }
                ),
                width="100%",
            ),
            rx.hstack(
                rx.text(
                    f"By {action['employee']}",
                    style={
                        "color": "rgba(156, 163, 175, 0.8)",
                        "font_size": "0.75rem",
                    }
                ),
                rx.text(
                    f" - {action['description']}",
                    style={
                        "color": "rgba(229, 231, 235, 0.9)",
                        "font_size": "0.75rem",
                    }
                ),
                spacing="0",
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        spacing="3",
        width="100%",
        style={
            "padding": "1rem",
            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
            "border_radius": "8px",
            "border": "1px solid rgba(255, 255, 255, 0.05)",
            "margin_bottom": "0.75rem",
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border_color": "rgba(255, 255, 255, 0.1)",
            }
        }
    )


def operation_button(icon: str, text: str, color: str, on_click=None) -> rx.Component:
    """Create an operation button."""
    return rx.button(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=16,
                style={"color": color}
            ),
            rx.text(
                text,
                style={
                    "color": color,
                    "font_weight": "500",
                }
            ),
            spacing="2",
            align="center",
        ),
        style={
            "padding": "0.75rem 1.25rem",
            "background": f"linear-gradient(135deg, {color}20 0%, {color}10 100%)",
            "border": f"1px solid {color}40",
            "border_radius": "8px",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "width": "100%",
            "_hover": {
                "background": f"linear-gradient(135deg, {color}30 0%, {color}20 100%)",
                "border_color": color,
                "transform": "translateY(-1px)",
                "box_shadow": f"0 4px 12px {color}20",
            }
        },
        on_click=on_click,
    )


def asset_view_modal() -> rx.Component:
    """Create the asset view details modal."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.hstack(
                        rx.icon(
                            tag="server",
                            size=24,
                            style={
                                "color": "#06b6d4",
                                "filter": "drop-shadow(0 0 8px #06b6d4)",
                            }
                        ),
                        rx.text(
                            AssetsState.view_asset_name,
                            style={
                                "font_size": "1.5rem",
                                "font_weight": "700",
                                "color": "rgba(255, 255, 255, 0.95)",
                                "background": "linear-gradient(135deg, #06b6d4 0%, rgba(255, 255, 255, 0.9) 100%)",
                                "background_clip": "text",
                                "-webkit-background-clip": "text",
                                "-webkit-text-fill-color": "transparent",
                            }
                        ),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon(tag="x", size=20),
                        on_click=AssetsState.close_view_modal,
                        style={
                            "background": "transparent",
                            "border": "none",
                            "color": "rgba(156, 163, 175, 0.8)",
                            "cursor": "pointer",
                            "padding": "0.5rem",
                            "_hover": {
                                "color": "rgba(255, 255, 255, 0.9)",
                            }
                        }
                    ),
                    width="100%",
                    align="center",
                ),
                
                # Recent Actions Section
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(
                                tag="clock",
                                size=20,
                                style={
                                    "color": "#10b981",
                                    "filter": "drop-shadow(0 0 6px #10b981)",
                                }
                            ),
                            rx.text(
                                "Recent Activity",
                                style={
                                    "color": "rgba(255, 255, 255, 0.95)",
                                    "font_weight": "600",
                                    "font_size": "1.125rem",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.foreach(
                                AssetsState.recent_actions,
                                action_history_row
                            ),
                            style={
                                "max_height": "300px",
                                "overflow_y": "auto",
                                "padding_right": "0.5rem",
                                "&::-webkit-scrollbar": {
                                    "width": "8px",
                                },
                                "&::-webkit-scrollbar-track": {
                                    "background": "rgba(0, 0, 0, 0.2)",
                                    "border_radius": "4px",
                                },
                                "&::-webkit-scrollbar-thumb": {
                                    "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.4) 0%, rgba(6, 182, 212, 0.2) 100%)",
                                    "border_radius": "4px",
                                },
                            }
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    style={
                        "width": "100%",
                        "padding": "1.5rem",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "12px",
                        "backdrop_filter": "blur(16px)",
                    }
                ),
                
                # Operations Section
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(
                                tag="settings",
                                size=20,
                                style={
                                    "color": "#f59e0b",
                                    "filter": "drop-shadow(0 0 6px #f59e0b)",
                                }
                            ),
                            rx.text(
                                "Asset Operations",
                                style={
                                    "color": "rgba(255, 255, 255, 0.95)",
                                    "font_weight": "600",
                                    "font_size": "1.125rem",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.grid(
                            operation_button("file_plus", "Add Log Collection", "#06b6d4"),
                            operation_button("shield", "Add DAT Update", "#10b981"),
                            operation_button("zap", "Patch System", "#f59e0b"),
                            operation_button("hard_drive", "Capture Recovery Image", "#a78bfa"),
                            columns="2",
                            spacing="3",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    style={
                        "width": "100%",
                        "padding": "1.5rem",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "12px",
                        "backdrop_filter": "blur(16px)",
                    }
                ),
                
                spacing="6",
                width="100%",
            ),
            style={
                "max_width": "600px",
                "width": "90vw",
                "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.98) 0%, rgba(17, 17, 17, 0.98) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "16px",
                "padding": "2rem",
                "box_shadow": "0 16px 64px rgba(0, 0, 0, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.06)",
                "backdrop_filter": "blur(20px) saturate(180%)",
            }
        ),
        open=AssetsState.view_modal_open,
        on_open_change=AssetsState.close_view_modal,
    )