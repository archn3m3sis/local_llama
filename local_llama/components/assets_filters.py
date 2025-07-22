"""Advanced filter components for assets table."""
import reflex as rx
from typing import List, Dict, Any


def search_bar(search_query: str, on_change) -> rx.Component:
    """Create an advanced search bar with animations."""
    return rx.box(
        rx.hstack(
            rx.icon(
                tag="search",
                size=20,
                style={
                    "position": "absolute",
                    "left": "1rem",
                    "top": "50%",
                    "transform": "translateY(-50%)",
                    "color": "rgba(156, 163, 175, 0.6)",
                    "z_index": "1",
                }
            ),
            rx.input(
                placeholder="Search assets by name, serial, barcode, or project...",
                value=search_query,
                on_change=on_change,
                style={
                    "width": "100%",
                    "height": "3rem",
                    "padding": "1rem 1rem 1rem 3rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "backdrop_filter": "blur(12px)",
                    "transition": "all 0.3s ease",
                    "_placeholder": {
                        "color": "rgba(156, 163, 175, 0.5)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "#06b6d4",
                        "box_shadow": "0 0 0 3px rgba(6, 182, 212, 0.1), 0 0 20px rgba(6, 182, 212, 0.2)",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                    }
                }
            ),
            rx.cond(
                search_query != "",
                rx.icon(
                    tag="x",
                    size=20,
                    style={
                        "position": "absolute",
                        "right": "1rem",
                        "top": "50%",
                        "transform": "translateY(-50%)",
                        "color": "rgba(156, 163, 175, 0.6)",
                        "cursor": "pointer",
                        "transition": "color 0.2s ease",
                        "_hover": {
                            "color": "rgba(255, 255, 255, 0.8)",
                        }
                    },
                    on_click=lambda: on_change(""),
                ),
                rx.fragment(),
            ),
            position="relative",
            width="100%",
        ),
        width="100%",
    )


def filter_dropdown(
    label: str,
    value: str,
    options: List[Dict[str, Any]],
    on_change,
    icon: str = "filter"
) -> rx.Component:
    """Create a styled filter dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                label,
                style={
                    "font_size": "0.75rem",
                    "font_weight": "600",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "color": "rgba(156, 163, 175, 0.8)",
                    "margin_bottom": "0.25rem",
                }
            ),
            rx.select(
                options,
                placeholder="Select...",
                value=value,
                on_change=on_change,
                style={
                    "width": "100%",
                    "padding": "0.5rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "6px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "0.875rem",
                    "backdrop_filter": "blur(12px)",
                    "cursor": "pointer",
                    "transition": "all 0.3s ease",
                    "_focus": {
                        "outline": "none",
                        "border_color": "#06b6d4",
                        "box_shadow": "0 0 0 3px rgba(6, 182, 212, 0.1)",
                    },
                    "_hover": {
                        "border_color": "rgba(255, 255, 255, 0.2)",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                    }
                }
            ),
            spacing="0",
            align="start",
            width="100%",
        ),
        flex="1",
    )


def filter_chip(label: str, count: int, is_active: bool = False, on_click=None) -> rx.Component:
    """Create a filter chip with count."""
    return rx.button(
        rx.hstack(
            rx.text(
                label,
                style={
                    "font_size": "0.813rem",
                    "font_weight": "500",
                }
            ),
            rx.box(
                rx.text(
                    str(count),
                    style={
                        "font_size": "0.75rem",
                        "font_weight": "600",
                    }
                ),
                style={
                    "padding": "0.125rem 0.5rem",
                    "background": rx.cond(
                        is_active,
                        "rgba(255, 255, 255, 0.2)",
                        "rgba(255, 255, 255, 0.1)"
                    ),
                    "border_radius": "9999px",
                }
            ),
            spacing="2",
            align="center",
        ),
        style={
            "padding": "0.5rem 1rem",
            "background": rx.cond(
                is_active,
                "linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%)",
                "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)"
            ),
            "border": rx.cond(
                is_active,
                "1px solid rgba(6, 182, 212, 0.4)",
                "1px solid rgba(255, 255, 255, 0.1)"
            ),
            "border_radius": "9999px",
            "color": rx.cond(
                is_active,
                "#06b6d4",
                "rgba(255, 255, 255, 0.9)"
            ),
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "_hover": {
                "transform": "translateY(-1px)",
                "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.2)",
                "border_color": rx.cond(
                    is_active,
                    "rgba(6, 182, 212, 0.6)",
                    "rgba(255, 255, 255, 0.2)"
                ),
            }
        },
        on_click=on_click,
    )


def filter_stats(stats: Dict[str, int], active_filter: str, on_filter) -> rx.Component:
    """Create filter statistics chips."""
    return rx.hstack(
        rx.foreach(
            list(stats.items()),
            lambda item: filter_chip(
                label=item[0],
                count=item[1],
                is_active=active_filter == item[0],
                on_click=lambda: on_filter(item[0])
            )
        ),
        spacing="2",
        wrap="wrap",
    )


def column_selector(visible_columns: List[str], all_columns: List[tuple], on_toggle) -> rx.Component:
    """Create a column visibility selector."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.button(
                rx.icon(tag="columns_3", size=16),
                rx.text("Columns", style={"margin_left": "0.5rem"}),
                style={
                    "padding": "0.5rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "6px",
                    "color": "rgba(255, 255, 255, 0.9)",
                    "font_size": "0.875rem",
                    "cursor": "pointer",
                    "display": "flex",
                    "align_items": "center",
                    "gap": "0.5rem",
                    "transition": "all 0.2s ease",
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    }
                }
            )
        ),
        rx.popover.content(
            rx.vstack(
                rx.text(
                    "Visible Columns",
                    style={
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                        "color": "rgba(255, 255, 255, 0.95)",
                    }
                ),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.checkbox(
                                checked=col[0] in visible_columns,
                                on_change=lambda checked, col_id=col[0]: on_toggle(col_id),
                                style={"accent_color": "#06b6d4"}
                            ),
                            rx.text(
                                col[1],
                                style={
                                    "font_size": "0.875rem",
                                    "color": "rgba(229, 231, 235, 0.9)",
                                }
                            ),
                            spacing="2",
                            width="100%",
                        )
                        for col in all_columns
                    ],
                    spacing="2",
                    width="100%",
                ),
                spacing="3",
                style={
                    "padding": "1rem",
                    "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.95) 0%, rgba(17, 17, 17, 0.95) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "backdrop_filter": "blur(20px)",
                    "min_width": "200px",
                }
            ),
        )
    )