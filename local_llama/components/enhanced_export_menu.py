"""Enhanced export menu with tabs for current page and all data export."""
import reflex as rx
from typing import Callable


def enhanced_export_menu(
    selected_count: rx.Var,
    on_export_current_page: Callable,
    on_export_all_data: Callable,
    current_page_count: rx.Var,
    total_count: rx.Var
) -> rx.Component:
    """Create an enhanced export menu with tabs for current page and all data.
    
    Args:
        selected_count: Number of selected items
        on_export_current_page: Callback for exporting current page
        on_export_all_data: Callback for exporting all data
        current_page_count: Number of items on current page
        total_count: Total number of items
    """
    return rx.hstack(
        # Current Page Export Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon(tag="file", size=16),
                    rx.text("Current Page", style={"margin_left": "0.5rem"}),
                    rx.text(
                        f"({current_page_count.to_string()})",
                        style={
                            "font_size": "0.75rem",
                            "color": "rgba(156, 163, 175, 0.8)",
                            "margin_left": "0.5rem",
                        }
                    ),
                    rx.cond(
                        selected_count > 0,
                        rx.box(
                            rx.text(
                                selected_count.to_string(),
                                style={
                                    "font_size": "0.75rem",
                                    "font_weight": "600",
                                }
                            ),
                            style={
                                "padding": "0.125rem 0.375rem",
                                "background": "#06b6d4",
                                "border_radius": "9999px",
                                "margin_left": "0.5rem",
                            }
                        ),
                        rx.fragment()
                    ),
                    style={
                        "padding": "0.5rem 1rem",
                        "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%)",
                        "border": "1px solid rgba(6, 182, 212, 0.4)",
                        "border_radius": "6px 0 0 6px",
                        "color": "#06b6d4",
                        "font_size": "0.875rem",
                        "cursor": "pointer",
                        "display": "flex",
                        "align_items": "center",
                        "gap": "0.5rem",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.3) 0%, rgba(6, 182, 212, 0.2) 100%)",
                            "border_color": "rgba(6, 182, 212, 0.6)",
                            "transform": "translateY(-1px)",
                            "box_shadow": "0 4px 12px rgba(6, 182, 212, 0.2)",
                        }
                    }
                )
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.text(
                        rx.cond(
                            selected_count > 0,
                            f"Export {selected_count.to_string()} selected items",
                            f"Export all {current_page_count.to_string()} items on this page"
                        ),
                        style={
                            "font_size": "0.75rem",
                            "color": "rgba(156, 163, 175, 0.8)",
                        }
                    ),
                    disabled=True,
                    style={"cursor": "default", "_hover": {"background": "transparent"}},
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon(tag="file-text", size=16),
                    "Export as CSV",
                    on_click=lambda: on_export_current_page("csv"),
                ),
                rx.menu.item(
                    rx.icon(tag="file-json", size=16),
                    "Export as JSON",
                    on_click=lambda: on_export_current_page("json"),
                ),
                rx.menu.item(
                    rx.icon(tag="file", size=16),
                    "Export as Excel",
                    on_click=lambda: on_export_current_page("excel"),
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon(tag="printer", size=16),
                    "Print Preview",
                    on_click=lambda: on_export_current_page("print"),
                ),
                style={
                    "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.95) 0%, rgba(17, 17, 17, 0.95) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "backdrop_filter": "blur(20px)",
                }
            )
        ),
        
        # All Data Export Menu
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon(tag="database", size=16),
                    rx.text("All Data", style={"margin_left": "0.5rem"}),
                    rx.text(
                        f"({total_count.to_string()})",
                        style={
                            "font_size": "0.75rem",
                            "color": "rgba(156, 163, 175, 0.8)",
                            "margin_left": "0.5rem",
                        }
                    ),
                    style={
                        "padding": "0.5rem 1rem",
                        "background": "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%)",
                        "border": "1px solid rgba(34, 197, 94, 0.4)",
                        "border_radius": "0 6px 6px 0",
                        "color": "#22c55e",
                        "font_size": "0.875rem",
                        "cursor": "pointer",
                        "display": "flex",
                        "align_items": "center",
                        "gap": "0.5rem",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "background": "linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(34, 197, 94, 0.2) 100%)",
                            "border_color": "rgba(34, 197, 94, 0.6)",
                            "transform": "translateY(-1px)",
                            "box_shadow": "0 4px 12px rgba(34, 197, 94, 0.2)",
                        }
                    }
                )
            ),
            rx.menu.content(
                rx.menu.item(
                    rx.text(
                        f"Export all {total_count.to_string()} items (filtered)",
                        style={
                            "font_size": "0.75rem",
                            "color": "rgba(156, 163, 175, 0.8)",
                        }
                    ),
                    disabled=True,
                    style={"cursor": "default", "_hover": {"background": "transparent"}},
                ),
                rx.cond(
                    total_count > 1000,
                    rx.menu.item(
                        rx.hstack(
                            rx.icon(
                                tag="alert-triangle",
                                size=14,
                                color="#f59e0b",
                            ),
                            rx.text(
                                "Large export may take time",
                                style={
                                    "font_size": "0.75rem",
                                    "color": "#f59e0b",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        disabled=True,
                        style={
                            "cursor": "default",
                            "background": "rgba(245, 158, 11, 0.1)",
                            "border": "1px solid rgba(245, 158, 11, 0.3)",
                            "border_radius": "4px",
                            "margin": "0.5rem",
                            "_hover": {"background": "rgba(245, 158, 11, 0.1)"},
                        }
                    ),
                    rx.fragment()
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon(tag="file-text", size=16),
                    "Export as CSV",
                    on_click=lambda: on_export_all_data("csv"),
                ),
                rx.menu.item(
                    rx.icon(tag="file-json", size=16),
                    "Export as JSON",
                    on_click=lambda: on_export_all_data("json"),
                ),
                rx.menu.item(
                    rx.icon(tag="file", size=16),
                    "Export as Excel",
                    on_click=lambda: on_export_all_data("excel"),
                ),
                rx.menu.separator(),
                rx.menu.item(
                    rx.icon(tag="printer", size=16),
                    "Print Preview",
                    on_click=lambda: on_export_all_data("print"),
                ),
                style={
                    "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.95) 0%, rgba(17, 17, 17, 0.95) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "backdrop_filter": "blur(20px)",
                }
            )
        ),
        spacing="0",
    )