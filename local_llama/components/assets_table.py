"""Advanced assets table component with stunning visuals."""
import reflex as rx
from typing import Dict, List, Any
from ..states.assets_state import AssetsState


def table_header_cell(title: str, column: str, sort_column: str, sort_direction: str, on_sort) -> rx.Component:
    """Create an interactive table header cell with sorting."""
    
    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(
                title,
                style={
                    "font_weight": "700",
                    "font_size": "0.875rem",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "color": rx.cond(
                        sort_column == column,
                        "rgba(255, 255, 255, 0.95)",
                        "rgba(255, 255, 255, 0.8)"
                    ),
                }
            ),
            rx.cond(
                sort_column == column,
                rx.icon(
                    tag=rx.cond(sort_direction == "asc", "chevron_up", "chevron_down"),
                    size=16,
                    style={
                        "color": "#06b6d4",
                        "filter": "drop-shadow(0 0 8px #06b6d4)",
                    }
                ),
                rx.icon(
                    tag="chevrons_up_down",
                    size=16,
                    style={
                        "color": "rgba(156, 163, 175, 0.5)",
                        "opacity": "0",
                        "transition": "opacity 0.2s ease",
                    }
                ),
            ),
            spacing="2",
            align="center",
            cursor="pointer",
            _hover={
                "& svg": {"opacity": "1"},
            },
            on_click=lambda: on_sort(column),
        ),
        style={
            "padding": "1rem 1.5rem",
            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
            "border_bottom": "2px solid rgba(255, 255, 255, 0.1)",
            "position": "sticky",
            "top": "0",
            "z_index": "10",
            "backdrop_filter": "blur(20px) saturate(180%)",
            "transition": "all 0.3s ease",
            "_hover": {
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
            }
        }
    )


def table_cell(content: Any, is_bold: bool = False, color: str = None) -> rx.Component:
    """Create a table cell with consistent styling."""
    return rx.table.cell(
        rx.text(
            content,
            style={
                "color": color or ("rgba(255, 255, 255, 0.95)" if is_bold else "rgba(229, 231, 235, 0.9)"),
                "font_weight": "600" if is_bold else "400",
                "font_size": "0.875rem",
                "white_space": "nowrap",
                "overflow": "hidden",
                "text_overflow": "ellipsis",
                "max_width": "200px",
            }
        ),
        style={
            "padding": "1rem 1.5rem",
            "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
        }
    )


def action_button(icon: str, color: str, tooltip: str, on_click=None) -> rx.Component:
    """Create an action button with tooltip."""
    return rx.tooltip(
        rx.button(
            rx.icon(
                tag=icon,
                size=16,
                style={"color": color}
            ),
            style={
                "background": f"linear-gradient(135deg, {color}20 0%, {color}10 100%)",
                "border": f"1px solid {color}40",
                "border_radius": "6px",
                "padding": "0.5rem",
                "cursor": "pointer",
                "transition": "all 0.2s ease",
                "_hover": {
                    "background": f"linear-gradient(135deg, {color}30 0%, {color}20 100%)",
                    "border_color": color,
                    "transform": "translateY(-1px)",
                    "box_shadow": f"0 4px 12px {color}20",
                }
            },
            on_click=on_click,
        ),
        content=tooltip,
    )


def asset_row(asset: Dict[str, Any], is_selected: bool, on_select) -> rx.Component:
    """Create a table row for an asset with selection and actions."""
    row_content = []
    
    # Selection checkbox
    row_content.append(
        rx.table.cell(
            rx.checkbox(
                checked=is_selected,
                on_change=lambda: on_select(asset["asset_id"]),
                style={
                    "accent_color": "#06b6d4",
                    "cursor": "pointer",
                }
            ),
            style={
                "padding": "1rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
            }
        )
    )
    
    # Data columns - show all columns
    # Asset ID
    row_content.append(
        table_cell(asset["asset_id"], True, "#06b6d4")
    )
    
    # Asset Name
    row_content.append(
        table_cell(asset["asset_name"], True, None)
    )
    
    # Project
    row_content.append(
        table_cell(asset["project"], False, "#10b981")
    )
    
    # Building
    row_content.append(
        table_cell(asset["building"], False, "#a78bfa")
    )
    
    # Floor
    row_content.append(
        table_cell(asset["floor"], False, None)
    )
    
    # System Type
    row_content.append(
        table_cell(asset["systype"], False, "#f59e0b")
    )
    
    # Operating System
    row_content.append(
        table_cell(asset["os"], False, None)
    )
    
    # Serial Number
    row_content.append(
        table_cell(asset["serial_no"], False, None)
    )
    
    # Barcode
    row_content.append(
        table_cell(asset["barcode"], False, None)
    )
    
    # Actions
    row_content.append(
        rx.table.cell(
            rx.hstack(
                action_button("eye", "#06b6d4", "View Details"),
                action_button("pencil", "#10b981", "Edit Asset", on_click=lambda: AssetsState.open_edit_modal(asset["asset_id"])),
                action_button("trash_2", "#ef4444", "Delete Asset"),
                spacing="2",
            ),
            style={
                "padding": "1rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
            }
        )
    )
    
    return rx.table.row(
        *row_content,
        style={
            "background": rx.cond(
                is_selected,
                "linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
                "transparent"
            ),
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
            }
        }
    )


def assets_table(
    assets: List[Dict[str, Any]], 
    selected_rows: List[str],
    select_all: bool,
    sort_column: str,
    sort_direction: str,
    on_select,
    on_sort,
    on_select_all
) -> rx.Component:
    """Create the main assets table with all features."""
    
    # Column definitions
    columns = [
        ("asset_id", "ID"),
        ("asset_name", "Asset Name"),
        ("project", "Project"),
        ("building", "Building"),
        ("floor", "Floor"),
        ("systype", "System Type"),
        ("os", "Operating System"),
        ("serial_no", "Serial Number"),
        ("barcode", "Barcode"),
        ("actions", "Actions"),
    ]
    
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        rx.checkbox(
                            checked=select_all,
                            on_change=on_select_all,
                            style={
                                "accent_color": "#06b6d4",
                                "cursor": "pointer",
                            }
                        ),
                        style={
                            "padding": "1rem",
                            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                            "border_bottom": "2px solid rgba(255, 255, 255, 0.1)",
                            "position": "sticky",
                            "top": "0",
                            "z_index": "10",
                            "backdrop_filter": "blur(20px) saturate(180%)",
                        }
                    ),
                    *[
                        table_header_cell(
                            title=title,
                            column=col,
                            sort_column=sort_column,
                            sort_direction=sort_direction,
                            on_sort=on_sort
                        )
                        for col, title in columns
                    ],
                )
            ),
            rx.table.body(
                rx.foreach(
                    assets,
                    lambda asset: asset_row(
                        asset=asset,
                        is_selected=selected_rows.contains(asset["asset_id"]),
                        on_select=on_select
                    )
                )
            ),
            style={
                "width": "100%",
                "border_collapse": "separate",
                "border_spacing": "0",
            }
        ),
        style={
            "width": "100%",
            "overflow": "auto",
            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
            "backdrop_filter": "blur(16px) saturate(180%) brightness(0.9)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": "12px",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.06)",
            "max_height": "600px",
            "position": "relative",
            "&::-webkit-scrollbar": {
                "width": "12px",
                "height": "12px",
            },
            "&::-webkit-scrollbar-track": {
                "background": "rgba(0, 0, 0, 0.2)",
                "border_radius": "6px",
            },
            "&::-webkit-scrollbar-thumb": {
                "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.4) 0%, rgba(6, 182, 212, 0.2) 100%)",
                "border_radius": "6px",
                "border": "2px solid rgba(0, 0, 0, 0.2)",
            },
            "&::-webkit-scrollbar-thumb:hover": {
                "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.6) 0%, rgba(6, 182, 212, 0.4) 100%)",
            },
        }
    )