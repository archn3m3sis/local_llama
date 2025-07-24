"""Assets page with advanced table and filtering."""
import reflex as rx
from ..states.assets_state import AssetsState
from ..components.assets_table_inline_edit import assets_table_inline
from ..components.assets_filters import (
    search_bar, filter_dropdown, filter_stats, column_selector
)
from ..components.shared_styles import CARD_STYLE
from ..components.metallic_text import metallic_title
from ..components.asset_view_modal import asset_view_modal
from ..components.asset_delete_modal import asset_delete_modal


def stats_card(title: str, value: rx.Var | str | int, icon: str, color: str) -> rx.Component:
    """Create a statistics card for assets overview."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag=icon,
                    size=20,
                    style={
                        "color": color,
                        "filter": f"drop-shadow(0 0 8px {color}40)",
                    }
                ),
                rx.text(
                    title,
                    style={
                        "color": "rgba(156, 163, 175, 0.8)",
                        "font_size": "0.75rem",
                        "font_weight": "500",
                        "text_transform": "uppercase",
                        "letter_spacing": "0.05em",
                    }
                ),
                spacing="2",
                align="center",
            ),
            rx.text(
                value if isinstance(value, str) else value.to_string(),
                style={
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "2rem",
                    "font_weight": "700",
                    "line_height": "1",
                    "background": f"linear-gradient(135deg, {color} 0%, rgba(255, 255, 255, 0.9) 100%)",
                    "background_clip": "text",
                    "-webkit-background-clip": "text",
                    "-webkit-text-fill-color": "transparent",
                    "filter": f"drop-shadow(0 0 10px {color}40)",
                }
            ),
            spacing="2",
            align="start",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.25rem",
            "flex": "1",
        }
    )


def pagination_controls() -> rx.Component:
    """Create pagination controls."""
    return rx.hstack(
        # Page size selector
        rx.select(
            ["10", "25", "50", "100"],
            value=AssetsState.page_size.to_string(),
            default_value="25",
            placeholder="25",
            on_change=AssetsState.set_page_size,
            style={
                "width": "120px",
                "min_width": "120px",
                "padding": "0.5rem 0.75rem",
                "padding_right": "2rem",  # Extra space for dropdown arrow
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "6px",
                "color": "rgba(255, 255, 255, 0.95) !important",
                "font_size": "0.875rem",
                "font_weight": "500",
                "cursor": "pointer",
                "appearance": "none",
                "-webkit-appearance": "none",
                "-moz-appearance": "none",
                "background_image": "url('data:image/svg+xml;charset=UTF-8,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27rgba(255,255,255,0.6)%27 stroke-width=%272%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3e%3cpolyline points=%276 9 12 15 18 9%27%3e%3c/polyline%3e%3c/svg%3e')",
                "background_repeat": "no-repeat",
                "background_position": "right 0.5rem center",
                "background_size": "1.25rem",
                "text_align": "left",
                "line_height": "1.5",
                "_hover": {
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                    "border_color": "rgba(255, 255, 255, 0.2)",
                },
                "_focus": {
                    "outline": "none",
                    "border_color": "rgba(6, 182, 212, 0.6)",
                    "box_shadow": "0 0 0 2px rgba(6, 182, 212, 0.2)",
                },
                "& option": {
                    "background": "#1a1a1a",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "padding": "0.5rem",
                },
            }
        ),
        rx.text(
            "items per page",
            style={
                "color": "rgba(156, 163, 175, 0.8)",
                "font_size": "0.875rem",
            }
        ),
        rx.spacer(),
        # Page info
        rx.text(
            rx.cond(
                AssetsState.total_count > 0,
                f"Showing {((AssetsState.page - 1) * AssetsState.page_size + 1).to_string()} - {rx.cond(AssetsState.page * AssetsState.page_size > AssetsState.total_count, AssetsState.total_count, AssetsState.page * AssetsState.page_size).to_string()} of {AssetsState.total_count.to_string()}",
                "No results"
            ),
            style={
                "color": "rgba(229, 231, 235, 0.9)",
                "font_size": "0.875rem",
            }
        ),
        rx.spacer(),
        # Navigation buttons
        rx.button(
            rx.icon(tag="chevron_left", size=16),
            on_click=AssetsState.prev_page,
            disabled=AssetsState.page <= 1,
            style={
                "padding": "0.5rem",
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "6px",
                "color": rx.cond(
                    AssetsState.page <= 1,
                    "rgba(156, 163, 175, 0.4)",
                    "rgba(255, 255, 255, 0.9)"
                ),
                "cursor": rx.cond(AssetsState.page <= 1, "not-allowed", "pointer"),
                "transition": "all 0.2s ease",
                "_hover": rx.cond(
                    AssetsState.page <= 1,
                    {},
                    {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    }
                ),
            }
        ),
        rx.text(
            f"Page {AssetsState.page.to_string()} of {AssetsState.total_pages.to_string()}",
            style={
                "color": "rgba(229, 231, 235, 0.9)",
                "font_size": "0.875rem",
                "margin": "0 1rem",
            }
        ),
        rx.button(
            rx.icon(tag="chevron_right", size=16),
            on_click=AssetsState.next_page,
            disabled=AssetsState.page >= AssetsState.total_pages,
            style={
                "padding": "0.5rem",
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "6px",
                "color": rx.cond(
                    AssetsState.page >= AssetsState.total_pages,
                    "rgba(156, 163, 175, 0.4)",
                    "rgba(255, 255, 255, 0.9)"
                ),
                "cursor": rx.cond(AssetsState.page >= AssetsState.total_pages, "not-allowed", "pointer"),
                "transition": "all 0.2s ease",
                "_hover": rx.cond(
                    AssetsState.page >= AssetsState.total_pages,
                    {},
                    {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    }
                ),
            }
        ),
        width="100%",
        align="center",
        padding="1rem 0",
    )


def export_menu() -> rx.Component:
    """Create export menu dropdown."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon(tag="download", size=16),
                rx.text("Export", style={"margin_left": "0.5rem"}),
                rx.cond(
                    AssetsState.selected_rows.length() > 0,
                    rx.box(
                        rx.text(
                            AssetsState.selected_rows.length().to_string(),
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
                    "border_radius": "6px",
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
                rx.icon(tag="file_text", size=16),
                "Export as CSV",
                on_click=lambda: AssetsState.export_selected("csv"),
            ),
            rx.menu.item(
                rx.icon(tag="file_json", size=16),
                "Export as JSON",
                on_click=lambda: AssetsState.export_selected("json"),
            ),
            rx.menu.item(
                rx.icon(tag="file", size=16),
                "Export as Excel",
                on_click=lambda: AssetsState.export_selected("excel"),
            ),
            rx.menu.separator(),
            rx.menu.item(
                rx.icon(tag="printer", size=16),
                "Print",
                on_click=lambda: AssetsState.export_selected("print"),
            ),
            style={
                "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.95) 0%, rgba(17, 17, 17, 0.95) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "backdrop_filter": "blur(20px)",
            }
        )
    )


def Assets() -> rx.Component:
    """The main assets page with advanced table."""
    return rx.fragment(
        rx.box(
        rx.vstack(
        # Page header
        metallic_title("Industrial Assets Management"),
        
        # Stats overview
        rx.hstack(
            stats_card(
                "Total Assets",
                AssetsState.total_count,
                "server",
                "#06b6d4"
            ),
            stats_card(
                "Projects",
                AssetsState.project_count,
                "folder",
                "#10b981"
            ),
            stats_card(
                "Buildings",
                AssetsState.building_count,
                "building",
                "#a78bfa"
            ),
            stats_card(
                "Operating Systems",
                AssetsState.os_count,
                "cpu",
                "#f59e0b"
            ),
            spacing="4",
            width="100%",
            style={"margin_bottom": "2rem"}
        ),
        
        # Search and filters section
        rx.box(
            rx.vstack(
                # Search bar
                search_bar(
                    search_query=AssetsState.search_query,
                    on_change=AssetsState.set_search_query
                ),
                
                # Filter dropdowns
                rx.hstack(
                    filter_dropdown(
                        label="Project",
                        value=AssetsState.filter_project,
                        options=AssetsState.projects,
                        on_change=AssetsState.set_filter_project,
                        icon="folder"
                    ),
                    filter_dropdown(
                        label="Building",
                        value=AssetsState.filter_building,
                        options=AssetsState.buildings,
                        on_change=AssetsState.set_filter_building,
                        icon="building"
                    ),
                    filter_dropdown(
                        label="System Type",
                        value=AssetsState.filter_systype,
                        options=AssetsState.systypes,
                        on_change=AssetsState.set_filter_systype,
                        icon="cpu"
                    ),
                    filter_dropdown(
                        label="Operating System",
                        value=AssetsState.filter_os,
                        options=AssetsState.operating_systems,
                        on_change=AssetsState.set_filter_os,
                        icon="monitor"
                    ),
                    rx.button(
                        rx.icon(tag="x", size=16),
                        "Clear Filters",
                        on_click=AssetsState.clear_filters,
                        style={
                            "padding": "0.5rem 1rem",
                            "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%)",
                            "border": "1px solid rgba(239, 68, 68, 0.4)",
                            "border_radius": "6px",
                            "color": "#ef4444",
                            "font_size": "0.875rem",
                            "cursor": "pointer",
                            "display": "flex",
                            "align_items": "center",
                            "gap": "0.5rem",
                            "transition": "all 0.2s ease",
                            "margin_top": "auto",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(239, 68, 68, 0.2) 100%)",
                                "border_color": "rgba(239, 68, 68, 0.6)",
                            }
                        }
                    ),
                    spacing="4",
                    width="100%",
                    align="end",
                ),
                spacing="4",
            ),
            style={
                **CARD_STYLE,
                "padding": "1.5rem",
                "margin_bottom": "2rem",
            }
        ),
        
        # Table controls
        rx.hstack(
            rx.text(
                rx.cond(
                    AssetsState.selected_rows.length() > 0,
                    f"{AssetsState.selected_rows.length().to_string()} selected",
                    ""
                ),
                style={
                    "color": "#06b6d4",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                }
            ),
            rx.spacer(),
            export_menu(),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        # Main table
        rx.cond(
            AssetsState.is_loading,
            rx.center(
                rx.box(
                    rx.spinner(
                        size="3",
                        style={"color": "#06b6d4"}
                    ),
                    rx.text(
                        "Loading assets...",
                        style={
                            "color": "rgba(156, 163, 175, 0.8)",
                            "font_size": "0.875rem",
                            "margin_top": "1rem",
                        }
                    ),
                    style={
                        "text_align": "center",
                    }
                ),
                style={"height": "400px"}
            ),
            assets_table_inline(
                assets=AssetsState.paginated_assets,
                selected_rows=AssetsState.selected_rows,
                select_all=AssetsState.is_current_page_selected,
                sort_column=AssetsState.sort_column,
                sort_direction=AssetsState.sort_direction,
                editing_asset_id=AssetsState.editing_asset_id,
                on_select=AssetsState.toggle_row_selection,
                on_sort=AssetsState.sort_by_column,
                on_select_all=AssetsState.toggle_select_all
            )
        ),
        
        # Pagination
        pagination_controls(),
        
        spacing="4",
        width="100%",
        padding="3em",
        padding_top="4em",
        padding_bottom="8em",  # Increased bottom padding for space
        on_mount=AssetsState.load_assets_data,
    ),
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow_y="auto",
        z_index="10",
    ),
    # Add the view modal
    asset_view_modal(),
    # Add the delete modal
    asset_delete_modal(),
    )