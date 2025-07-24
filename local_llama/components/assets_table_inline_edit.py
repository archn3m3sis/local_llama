"""Advanced assets table component with inline editing."""
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
            "z_index": "20",
            "backdrop_filter": "blur(20px) saturate(180%)",
            "-webkit-backdrop-filter": "blur(20px) saturate(180%)",
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
                "text_align": "left",
            }
        ),
        style={
            "padding": "1rem 1.5rem",
            "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
            "text_align": "left",
        }
    )


def edit_cell_dropdown(field: str, value: str, options: List[str]) -> rx.Component:
    """Create an editable table cell with dropdown."""
    return rx.table.cell(
        rx.select(
            options,
            value=value,
            on_change=lambda new_val: AssetsState.update_edit_field(field, new_val),
            style={
                "width": "100%",
                "padding": "0.5rem",
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border": "1px solid rgba(6, 182, 212, 0.4)",
                "border_radius": "6px",
                "color": "rgba(255, 255, 255, 0.95)",
                "font_size": "0.875rem",
                "cursor": "pointer",
                "_focus": {
                    "border_color": "#06b6d4",
                    "box_shadow": "0 0 0 2px rgba(6, 182, 212, 0.2)",
                }
            }
        ),
        style={
            "padding": "0.5rem 1rem",
            "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(6, 182, 212, 0.02) 100%)",
            "border_bottom": "2px solid rgba(6, 182, 212, 0.3)",
        }
    )


def edit_cell_input(field: str, value: str) -> rx.Component:
    """Create an editable table cell with input field."""
    return rx.table.cell(
        rx.input(
            value=value,
            on_change=lambda new_val: AssetsState.update_edit_field(field, new_val),
            style={
                "width": "100%",
                "padding": "0.5rem",
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border": "1px solid rgba(6, 182, 212, 0.4)",
                "border_radius": "6px",
                "color": "rgba(255, 255, 255, 0.95)",
                "font_size": "0.875rem",
                "_focus": {
                    "border_color": "#06b6d4",
                    "box_shadow": "0 0 0 2px rgba(6, 182, 212, 0.2)",
                }
            }
        ),
        style={
            "padding": "0.5rem 1rem",
            "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(6, 182, 212, 0.02) 100%)",
            "border_bottom": "2px solid rgba(6, 182, 212, 0.3)",
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


def edit_row(asset: Dict[str, Any], is_selected: bool, on_select) -> rx.Component:
    """Create an edit row for inline editing."""
    return rx.fragment(
        # Main row with edit fields
        rx.table.row(
            # Selection checkbox
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
                    "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(6, 182, 212, 0.02) 100%)",
                    "border_bottom": "2px solid rgba(6, 182, 212, 0.3)",
                }
            ),
            # Asset ID (non-editable)
            table_cell(asset["asset_id"], True, "#06b6d4"),
            # Asset Name (editable)
            edit_cell_input("asset_name", AssetsState.edit_asset_name),
            # Project (dropdown) - using edit list without "All" option
            edit_cell_dropdown("project", AssetsState.edit_project, AssetsState.edit_projects),
            # Building (dropdown)
            edit_cell_dropdown("building", AssetsState.edit_building, AssetsState.edit_buildings),
            # Floor (dropdown)
            edit_cell_dropdown("floor", AssetsState.edit_floor, AssetsState.floors),
            # System Type (dropdown)
            edit_cell_dropdown("systype", AssetsState.edit_systype, AssetsState.edit_systypes),
            # Operating System (dropdown)
            edit_cell_dropdown("os", AssetsState.edit_os, AssetsState.edit_operating_systems),
            # Serial Number (editable)
            edit_cell_input("serial_no", AssetsState.edit_serial_no),
            # Barcode (editable)
            edit_cell_input("barcode", AssetsState.edit_barcode),
            # Actions
            rx.table.cell(
                rx.hstack(
                    action_button("check", "#10b981", "Save Changes", on_click=AssetsState.save_inline_changes),
                    action_button("x", "#ef4444", "Cancel", on_click=AssetsState.cancel_edit),
                    spacing="2",
                ),
                style={
                    "padding": "1rem",
                    "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(6, 182, 212, 0.02) 100%)",
                    "border_bottom": "2px solid rgba(6, 182, 212, 0.3)",
                }
            ),
            style={
                "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
                "transition": "all 0.3s ease",
                "box_shadow": "0 4px 12px rgba(6, 182, 212, 0.2)",
            }
        ),
        # Expansion row with additional edit message
        rx.table.row(
            rx.table.cell(
                rx.hstack(
                    rx.icon(
                        tag="info",
                        size=16,
                        style={
                            "color": "#06b6d4",
                            "filter": "drop-shadow(0 0 4px #06b6d4)",
                        }
                    ),
                    rx.text(
                        "Editing asset - make your changes and click Save to confirm or Cancel to discard",
                        style={
                            "color": "rgba(6, 182, 212, 0.9)",
                            "font_size": "0.875rem",
                            "font_style": "italic",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                col_span=11,
                style={
                    "padding": "1rem 2rem",
                    "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(6, 182, 212, 0.04) 100%)",
                    "border_bottom": "2px solid rgba(6, 182, 212, 0.3)",
                    "border_left": "4px solid #06b6d4",
                }
            ),
        )
    )


def normal_row(asset: Dict[str, Any], is_selected: bool, on_select) -> rx.Component:
    """Create a normal display row."""
    return rx.table.row(
        # Selection checkbox
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
                "text_align": "left",
            }
        ),
        # Data columns
        table_cell(asset["asset_id"], True, "#06b6d4"),
        rx.table.cell(
            rx.text(
                asset["asset_name"],
                style={
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_weight": "600",
                    "font_size": "0.875rem",
                    "white_space": "nowrap",
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "max_width": "150px",
                    "text_align": "left",
                }
            ),
            style={
                "padding": "1rem 1.5rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
                "text_align": "left",
            }
        ),
        rx.table.cell(
            rx.text(
                asset["project"],
                style={
                    "color": "#10b981",
                    "font_weight": "400",
                    "font_size": "0.875rem",
                    "white_space": "nowrap",
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "max_width": "150px",
                    "text_align": "left",
                }
            ),
            style={
                "padding": "1rem 1.5rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
                "text_align": "left",
            }
        ),
        rx.table.cell(
            rx.hstack(
                rx.image(
                    src="/icons/building-24-filled.svg",
                    alt="Building",
                    style={
                        "width": "20px",
                        "height": "20px",
                        "filter": "brightness(0) saturate(100%) invert(83%) sepia(15%) saturate(1187%) hue-rotate(213deg) brightness(95%) contrast(92%)",  # Makes it purple like #a78bfa
                        "display": "inline-block",
                    }
                ),
                rx.text(
                    asset["building"],
                    style={
                        "color": "#a78bfa",
                        "font_weight": "400",
                        "font_size": "0.875rem",
                        "white_space": "nowrap",
                        "overflow": "hidden",
                        "text_overflow": "ellipsis",
                    }
                ),
                spacing="2",
                align="center",
                justify="start",
            ),
            style={
                "padding": "1rem 1.5rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
                "text_align": "left",
            }
        ),
        rx.table.cell(
            rx.hstack(
                rx.image(
                    src="/icons/3d-stairs.svg",
                    alt="Floor",
                    style={
                        "width": "20px",
                        "height": "20px",
                        "filter": "brightness(0) saturate(100%) invert(75%) sepia(10%) saturate(200%) hue-rotate(180deg) brightness(90%) contrast(85%)",  # Makes it gray like the text
                        "display": "inline-block",
                    }
                ),
                rx.text(
                    asset["floor"],
                    style={
                        "color": "rgba(229, 231, 235, 0.9)",
                        "font_weight": "400",
                        "font_size": "0.875rem",
                        "white_space": "nowrap",
                        "overflow": "hidden",
                        "text_overflow": "ellipsis",
                        "min_width": "60px",
                    }
                ),
                spacing="2",
                align="center",
                justify="start",
            ),
            style={
                "padding": "1rem 1.5rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
                "text_align": "left",
            }
        ),
        table_cell(asset["systype"], False, "#f59e0b"),
        table_cell(asset["os"], False, None),
        table_cell(asset["serial_no"], False, None),
        table_cell(asset["barcode"], False, None),
        # Actions
        rx.table.cell(
            rx.hstack(
                action_button("eye", "#06b6d4", "View Details", on_click=lambda: AssetsState.open_view_modal(asset["asset_id"])),
                action_button("pencil", "#10b981", "Edit Asset", on_click=lambda: AssetsState.start_inline_edit(asset["asset_id"])),
                action_button("trash_2", "#ef4444", "Delete Asset", on_click=lambda: AssetsState.open_delete_modal(asset["asset_id"])),
                spacing="2",
            ),
            style={
                "padding": "1rem",
                "border_bottom": "1px solid rgba(55, 65, 81, 0.3)",
                "text_align": "left",
            }
        ),
        style={
            "background": rx.cond(
                is_selected,
                "linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
                "transparent"
            ),
            "transition": "all 0.2s ease",
            "_hover": {
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
            },
            "position": "relative",
        },
    )


def asset_row_with_edit(asset: Dict[str, Any], is_selected: bool, is_editing: bool, on_select) -> rx.Component:
    """Create a table row for an asset with inline editing capability."""
    return rx.cond(
        is_editing,
        edit_row(asset, is_selected, on_select),
        normal_row(asset, is_selected, on_select)
    )


def assets_table_inline(
    assets: List[Dict[str, Any]], 
    selected_rows: List[str],
    select_all: bool,
    sort_column: str,
    sort_direction: str,
    editing_asset_id: str,
    on_select,
    on_sort,
    on_select_all
) -> rx.Component:
    """Create the main assets table with inline editing."""
    
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
                            "z_index": "20",
                            "backdrop_filter": "blur(20px) saturate(180%)",
                            "-webkit-backdrop-filter": "blur(20px) saturate(180%)",
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
                    lambda asset: asset_row_with_edit(
                        asset=asset,
                        is_selected=selected_rows.contains(asset["asset_id"]),
                        is_editing=editing_asset_id == asset["asset_id"],
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
            "overflow_x": "auto",
            "overflow_y": "auto",
            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
            "backdrop_filter": "blur(16px) saturate(180%) brightness(0.9)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": "12px",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.06)",
            "max_height": "500px",  # Reduced to ensure pagination is visible
            "height": "500px",
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