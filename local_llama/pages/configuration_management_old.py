"""Configuration Management page with software catalog display."""
import reflex as rx
from ..components.universal_background import page_wrapper
from ..components.metallic_text import metallic_title
from ..states.configuration_management_state import ConfigurationManagementState
from ..components.shared_styles import CARD_STYLE

def software_version_badge(version: str, is_latest: bool = False) -> rx.Component:
    """Create a version badge with modern styling."""
    return rx.box(
        rx.text(
            f"v{version}",
            style={
                "color": "rgba(255, 255, 255, 0.95)" if is_latest else "rgba(255, 255, 255, 0.7)",
                "font_size": "0.75rem",
                "font_weight": "600",
                "letter_spacing": "0.025em",
            }
        ),
        style={
            "padding": "0.25rem 0.75rem",
            "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 100%)" if is_latest else "rgba(255, 255, 255, 0.1)",
            "border": f"1px solid {'rgba(99, 102, 241, 0.5)' if is_latest else 'rgba(255, 255, 255, 0.2)'}",
            "border_radius": "9999px",
            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.3)" if is_latest else "none",
        }
    )

def compliance_indicator(is_compliant: bool) -> rx.Component:
    """Create a compliance status indicator."""
    return rx.hstack(
        rx.icon(
            tag="shield-check" if is_compliant else "shield-alert",
            size=16,
            color="#10b981" if is_compliant else "#ef4444",
        ),
        rx.text(
            "DoD Compliant" if is_compliant else "Non-Compliant",
            style={
                "color": "#10b981" if is_compliant else "#ef4444",
                "font_size": "0.875rem",
                "font_weight": "500",
            }
        ),
        spacing="2",
        align="center",
    )

def software_catalog_table() -> rx.Component:
    """Create the main software catalog table - simplified version."""
    return rx.box(
        rx.vstack(
            # Header with title
            rx.hstack(
                rx.text(
                    "Software Catalog",
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1.5rem",
                        "font_weight": "700",
                        "background": "linear-gradient(135deg, #ffffff 0%, #e0e0e0 50%, #ffffff 100%)",
                        "background_clip": "text",
                        "-webkit-background-clip": "text",
                        "-webkit-text-fill-color": "transparent",
                        "filter": "drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3))",
                    }
                ),
                rx.spacer(),
                # Clear filters button
                rx.button(
                    rx.icon(tag="x", size=16),
                    "Clear All Filters",
                    on_click=ConfigurationManagementState.clear_all_filters,
                    style={
                        "padding": "0.5rem 1rem",
                        "background": "rgba(239, 68, 68, 0.1)",
                        "border": "1px solid rgba(239, 68, 68, 0.3)",
                        "border_radius": "6px",
                        "color": "rgba(239, 68, 68, 0.9)",
                        "font_size": "0.875rem",
                        "font_weight": "500",
                        "cursor": "pointer",
                        "display": "flex",
                        "align_items": "center",
                        "gap": "0.5rem",
                        "margin_right": "1rem",
                        "_hover": {
                            "background": "rgba(239, 68, 68, 0.2)",
                            "border_color": "rgba(239, 68, 68, 0.5)",
                        }
                    }
                ),
                # View mode toggle buttons
                rx.hstack(
                    rx.button(
                        "Catalog View",
                        on_click=ConfigurationManagementState.set_catalog_view,
                        style={
                            "padding": "0.5rem 1rem",
                            "background": rx.cond(
                                ConfigurationManagementState.view_mode == "catalog",
                                "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 100%)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": rx.cond(
                                ConfigurationManagementState.view_mode == "catalog",
                                "1px solid rgba(99, 102, 241, 0.5)",
                                "1px solid rgba(255, 255, 255, 0.1)"
                            ),
                            "border_radius": "6px 0 0 6px",
                            "color": "rgba(255, 255, 255, 0.9)",
                            "font_size": "0.875rem",
                            "font_weight": "500",
                            "cursor": "pointer",
                        }
                    ),
                    rx.button(
                        "Asset View",
                        on_click=ConfigurationManagementState.set_asset_view,
                        style={
                            "padding": "0.5rem 1rem",
                            "background": rx.cond(
                                ConfigurationManagementState.view_mode == "asset",
                                "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 100%)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": rx.cond(
                                ConfigurationManagementState.view_mode == "asset",
                                "1px solid rgba(99, 102, 241, 0.5)",
                                "1px solid rgba(255, 255, 255, 0.1)"
                            ),
                            "border_radius": "0 6px 6px 0",
                            "color": "rgba(255, 255, 255, 0.9)",
                            "font_size": "0.875rem",
                            "font_weight": "500",
                            "cursor": "pointer",
                        }
                    ),
                    spacing="0",
                ),
                width="100%",
                align="center",
                style={"margin_bottom": "1.5rem"},
            ),
            
            # Search bar
            rx.input(
                placeholder="Search software...",
                value=ConfigurationManagementState.software_search,
                on_change=ConfigurationManagementState.set_software_search,
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "0.875rem",
                    "margin_bottom": "1rem",
                    "_placeholder": {"color": "rgba(156, 163, 175, 0.5)"},
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            
            # Software count or selection prompt with pagination info
            rx.hstack(
                rx.text(
                    rx.cond(
                        ConfigurationManagementState.view_mode == "catalog",
                        f"Total Software: {ConfigurationManagementState.total_software}",
                        rx.cond(
                            ConfigurationManagementState.selected_asset == "",
                            "Please select a project and asset to view software",
                            f"Software for {ConfigurationManagementState.selected_asset}: {ConfigurationManagementState.filtered_software_count}"
                        )
                    ),
                    style={
                        "color": "rgba(156, 163, 175, 0.8)",
                        "font_size": "0.875rem",
                    }
                ),
                rx.spacer(),
                rx.text(
                    ConfigurationManagementState.page_info,
                    style={
                        "color": "rgba(156, 163, 175, 0.6)",
                        "font_size": "0.875rem",
                    }
                ),
                width="100%",
                align="center",
                margin_bottom="1rem",
            ),
            
            # Simplified table display
            rx.box(
                rx.cond(
                    ConfigurationManagementState.has_software,
                    rx.vstack(
                        # Table header with sortable columns
                        rx.hstack(
                            # Icon column header (empty for now)
                            rx.box(
                                style={"width": "40px"},
                            ),
                            rx.hstack(
                                rx.text("Software Name", style={"color": "rgba(156, 163, 175, 0.8)", "font_weight": "600", "font_size": "0.875rem"}),
                                rx.icon(
                                    tag=rx.cond(
                                        ConfigurationManagementState.sort_column == "name",
                                        rx.cond(
                                            ConfigurationManagementState.sort_ascending,
                                            "chevron-up",
                                            "chevron-down"
                                        ),
                                        "chevrons-up-down"
                                    ),
                                    size=14,
                                    color="rgba(156, 163, 175, 0.6)",
                                ),
                                style={"width": "30%", "cursor": "pointer"},
                                align="center",
                                spacing="2",
                                on_click=ConfigurationManagementState.sort_by_name,
                            ),
                            rx.hstack(
                                rx.text("Vendor", style={"color": "rgba(156, 163, 175, 0.8)", "font_weight": "600", "font_size": "0.875rem"}),
                                rx.icon(
                                    tag=rx.cond(
                                        ConfigurationManagementState.sort_column == "vendor",
                                        rx.cond(
                                            ConfigurationManagementState.sort_ascending,
                                            "chevron-up",
                                            "chevron-down"
                                        ),
                                        "chevrons-up-down"
                                    ),
                                    size=14,
                                    color="rgba(156, 163, 175, 0.6)",
                                ),
                                style={"width": "20%", "cursor": "pointer"},
                                align="center",
                                spacing="2",
                                on_click=ConfigurationManagementState.sort_by_vendor,
                            ),
                            rx.hstack(
                                rx.text("Category", style={"color": "rgba(156, 163, 175, 0.8)", "font_weight": "600", "font_size": "0.875rem"}),
                                rx.icon(
                                    tag=rx.cond(
                                        ConfigurationManagementState.sort_column == "category",
                                        rx.cond(
                                            ConfigurationManagementState.sort_ascending,
                                            "chevron-up",
                                            "chevron-down"
                                        ),
                                        "chevrons-up-down"
                                    ),
                                    size=14,
                                    color="rgba(156, 163, 175, 0.6)",
                                ),
                                style={"width": "15%", "cursor": "pointer"},
                                align="center",
                                spacing="2",
                                on_click=ConfigurationManagementState.sort_by_category,
                            ),
                            rx.text("Version", style={"width": "15%", "color": "rgba(156, 163, 175, 0.8)", "font_weight": "600", "font_size": "0.875rem"}),
                            rx.text("Compliance", style={"width": "20%", "color": "rgba(156, 163, 175, 0.8)", "font_weight": "600", "font_size": "0.875rem"}),
                            width="100%",
                            padding="1rem",
                            style={"border_bottom": "1px solid rgba(255, 255, 255, 0.1)"},
                        ),
                        # Software list
                        rx.scroll_area(
                            rx.vstack(
                                rx.foreach(
                                    ConfigurationManagementState.paginated_software,
                                    lambda sw, idx: rx.hstack(
                                        # Icon column (placeholder for now)
                                        rx.box(
                                            rx.icon(
                                                tag=rx.cond(
                                                    sw["army_gold_master"],
                                                    "shield-check",  # Shield icon for Army Gold Master
                                                    rx.cond(
                                                        sw["dod_compliant"],
                                                        "check-circle",  # Check icon for DoD compliant
                                                        rx.cond(
                                                            sw["compliance_status"] == "POTENTIAL HAZARD",
                                                            "triangle-alert",  # Alert icon for potential hazard
                                                            "circle"  # Default circle icon
                                                        )
                                                    )
                                                ),
                                                size=16,
                                                color=rx.cond(
                                                    sw["army_gold_master"],
                                                    "#10b981",  # Green for Army Gold Master
                                                    rx.cond(
                                                        sw["dod_compliant"],
                                                        "#3b82f6",  # Blue for DoD compliant
                                                        rx.cond(
                                                            sw["compliance_status"] == "POTENTIAL HAZARD",
                                                            "#ef4444",  # Red for potential hazard
                                                            "rgba(156, 163, 175, 0.4)"  # Gray default
                                                        )
                                                    )
                                                ),
                                            ),
                                            style={"width": "40px", "text_align": "center"},
                                        ),
                                        rx.text(
                                            sw["name"], 
                                            style={
                                                "width": "30%", 
                                                "color": "rgba(255, 255, 255, 0.9)",
                                                "font_size": "0.875rem",
                                                "white_space": "nowrap",
                                                "overflow": "hidden",
                                                "text_overflow": "ellipsis",
                                            }
                                        ),
                                        rx.text(
                                            sw["vendor"], 
                                            style={
                                                "width": "20%", 
                                                "color": "rgba(156, 163, 175, 0.8)",
                                                "font_size": "0.875rem",
                                            }
                                        ),
                                        rx.text(
                                            sw["category"], 
                                            style={
                                                "width": "15%", 
                                                "color": "rgba(156, 163, 175, 0.8)",
                                                "font_size": "0.875rem",
                                            }
                                        ),
                                        rx.text(
                                            sw["latest_version"], 
                                            style={
                                                "width": "15%", 
                                                "color": "rgba(99, 102, 241, 0.8)",
                                                "font_size": "0.875rem",
                                            }
                                        ),
                                        rx.text(
                                            rx.cond(
                                                sw["dod_compliant"],
                                                "✓ Compliant",
                                                "✗ Non-Compliant"
                                            ),
                                            style={
                                                "width": "20%", 
                                                "color": rx.cond(
                                                    sw["dod_compliant"],
                                                    "#10b981",
                                                    "#ef4444"
                                                ),
                                                "font_size": "0.875rem",
                                            }
                                        ),
                                        width="100%",
                                        padding="0.75rem 1rem",
                                        style={
                                            "border_bottom": "1px solid rgba(255, 255, 255, 0.05)",
                                            "_hover": {
                                                "background": "rgba(255, 255, 255, 0.02)",
                                            }
                                        }
                                    )
                                ),
                                spacing="0",
                                width="100%",
                            ),
                            style={
                                "height": "400px",
                                "width": "100%",
                            }
                        ),
                        width="100%",
                    ),
                    rx.text(
                        "No software found",
                        style={
                            "color": "rgba(156, 163, 175, 0.5)",
                            "font_size": "0.875rem",
                            "font_style": "italic",
                            "text_align": "center",
                            "padding": "2rem",
                        }
                    )
                ),
                style={
                    "width": "100%",
                    "min_height": "400px",
                    "background": "rgba(0, 0, 0, 0.2)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                }
            ),
            
            # Pagination controls
            rx.cond(
                ConfigurationManagementState.has_software,
                rx.hstack(
                    rx.button(
                        rx.icon(tag="chevron-left", size=16),
                        "Previous",
                        on_click=ConfigurationManagementState.prev_page,
                        disabled=ConfigurationManagementState.current_page == 1,
                        style={
                            "padding": "0.5rem 1rem",
                            "background": rx.cond(
                                ConfigurationManagementState.current_page == 1,
                                "rgba(255, 255, 255, 0.02)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "6px",
                            "color": rx.cond(
                                ConfigurationManagementState.current_page == 1,
                                "rgba(156, 163, 175, 0.4)",
                                "rgba(255, 255, 255, 0.9)"
                            ),
                            "font_size": "0.875rem",
                            "font_weight": "500",
                            "cursor": rx.cond(
                                ConfigurationManagementState.current_page == 1,
                                "not-allowed",
                                "pointer"
                            ),
                            "_hover": {
                                "background": rx.cond(
                                    ConfigurationManagementState.current_page == 1,
                                    "rgba(255, 255, 255, 0.02)",
                                    "rgba(255, 255, 255, 0.08)"
                                ),
                            }
                        }
                    ),
                    
                    rx.spacer(),
                    
                    rx.text(
                        f"Page {ConfigurationManagementState.current_page} of {ConfigurationManagementState.total_pages}",
                        style={
                            "color": "rgba(156, 163, 175, 0.8)",
                            "font_size": "0.875rem",
                            "font_weight": "500",
                        }
                    ),
                    
                    rx.spacer(),
                    
                    rx.button(
                        "Next",
                        rx.icon(tag="chevron-right", size=16),
                        on_click=ConfigurationManagementState.next_page,
                        disabled=ConfigurationManagementState.current_page == ConfigurationManagementState.total_pages,
                        style={
                            "padding": "0.5rem 1rem",
                            "background": rx.cond(
                                ConfigurationManagementState.current_page == ConfigurationManagementState.total_pages,
                                "rgba(255, 255, 255, 0.02)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "6px",
                            "color": rx.cond(
                                ConfigurationManagementState.current_page == ConfigurationManagementState.total_pages,
                                "rgba(156, 163, 175, 0.4)",
                                "rgba(255, 255, 255, 0.9)"
                            ),
                            "font_size": "0.875rem",
                            "font_weight": "500",
                            "cursor": rx.cond(
                                ConfigurationManagementState.current_page == ConfigurationManagementState.total_pages,
                                "not-allowed",
                                "pointer"
                            ),
                            "_hover": {
                                "background": rx.cond(
                                    ConfigurationManagementState.current_page == ConfigurationManagementState.total_pages,
                                    "rgba(255, 255, 255, 0.02)",
                                    "rgba(255, 255, 255, 0.08)"
                                ),
                            }
                        }
                    ),
                    width="100%",
                    align="center",
                    margin_top="1rem",
                ),
                rx.box()  # Empty box when no software
            ),
            
            spacing="4",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "2rem",
            "width": "100%",
        }
    )

def asset_selector() -> rx.Component:
    """Create a modern asset selector dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                "Select Asset",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "margin_bottom": "0.5rem",
                }
            ),
            rx.select(
                ConfigurationManagementState.available_assets,
                value=ConfigurationManagementState.selected_asset,
                on_change=ConfigurationManagementState.set_selected_asset,
                placeholder="Select an asset...",
                disabled=ConfigurationManagementState.selected_project == "All Projects",
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "font_weight": "500",
                    "cursor": rx.cond(
                        ConfigurationManagementState.selected_project == "All Projects",
                        "not-allowed",
                        "pointer"
                    ),
                    "opacity": rx.cond(
                        ConfigurationManagementState.selected_project == "All Projects",
                        "0.5",
                        "1"
                    ),
                    "_hover": {
                        "background": rx.cond(
                            ConfigurationManagementState.selected_project == "All Projects",
                            "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                            "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)"
                        ),
                        "border_color": rx.cond(
                            ConfigurationManagementState.selected_project == "All Projects",
                            "rgba(255, 255, 255, 0.1)",
                            "rgba(255, 255, 255, 0.2)"
                        ),
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            spacing="0",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "width": "100%",
        }
    )

def project_selector() -> rx.Component:
    """Create a modern project selector dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                "Select Project",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "margin_bottom": "0.5rem",
                }
            ),
            rx.select(
                ConfigurationManagementState.project_options,
                value=ConfigurationManagementState.selected_project,
                on_change=ConfigurationManagementState.set_selected_project,
                placeholder="Select a project...",
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "font_weight": "500",
                    "cursor": "pointer",
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            spacing="0",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "width": "100%",
        }
    )

def category_selector() -> rx.Component:
    """Create a modern category selector dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                "Filter by Category",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "margin_bottom": "0.5rem",
                }
            ),
            rx.select(
                ConfigurationManagementState.category_options,
                value=ConfigurationManagementState.selected_category,
                on_change=ConfigurationManagementState.set_selected_category,
                placeholder="All categories...",
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "font_weight": "500",
                    "cursor": "pointer",
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            spacing="0",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "width": "100%",
        }
    )

def compliance_selector() -> rx.Component:
    """Create a modern compliance status selector dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                "Compliance Status",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "margin_bottom": "0.5rem",
                }
            ),
            rx.select(
                ConfigurationManagementState.compliance_options,
                value=ConfigurationManagementState.selected_compliance,
                on_change=ConfigurationManagementState.set_selected_compliance,
                placeholder="All statuses...",
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "font_weight": "500",
                    "cursor": "pointer",
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            spacing="0",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "width": "100%",
        }
    )

def vendor_selector() -> rx.Component:
    """Create a modern vendor selector dropdown."""
    return rx.box(
        rx.vstack(
            rx.text(
                "Filter by Vendor",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "font_weight": "500",
                    "text_transform": "uppercase",
                    "letter_spacing": "0.05em",
                    "margin_bottom": "0.5rem",
                }
            ),
            rx.select(
                ConfigurationManagementState.vendor_options,
                value=ConfigurationManagementState.selected_vendor,
                on_change=ConfigurationManagementState.set_selected_vendor,
                placeholder="All vendors...",
                style={
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "8px",
                    "color": "rgba(255, 255, 255, 0.95)",
                    "font_size": "1rem",
                    "font_weight": "500",
                    "cursor": "pointer",
                    "_hover": {
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        "border_color": "rgba(255, 255, 255, 0.2)",
                    },
                    "_focus": {
                        "outline": "none",
                        "border_color": "rgba(99, 102, 241, 0.5)",
                        "box_shadow": "0 0 0 3px rgba(99, 102, 241, 0.1)",
                    },
                }
            ),
            spacing="0",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "width": "100%",
        }
    )

def ConfigurationManagement() -> rx.Component:
    """Configuration Management page with software catalog."""
    return rx.vstack(
        # Massive metallic title matching other pages
        metallic_title("IAMS - Configuration Management"),
        
        # Descriptive text matching other pages
        rx.text(
            "Manage software inventory and track version history across all assets",
            color="gray.400",
            font_size="1.1rem",
            margin_bottom="2em",
            margin_top="-1.5em",
            style={
                "text_align": "center"
            }
        ),
        
        # Content container with max width
        rx.box(
            rx.vstack(
                # Selectors row
                rx.hstack(
                    project_selector(),
                    rx.cond(
                        ConfigurationManagementState.view_mode == "asset",
                        asset_selector(),
                        vendor_selector()  # Show vendor selector in catalog view
                    ),
                    category_selector(),
                    compliance_selector(),
                    spacing="4",
                    width="100%",
                    style={"margin_bottom": "2rem"},
                ),
                
                # Main content area
                software_catalog_table(),
                
                spacing="4",
                width="100%",
            ),
            max_width="1400px",
            margin="0 auto",
            width="100%",
        ),
        
        spacing="4",
        width="100%",
        padding="3em",
        padding_top="4em",
        padding_bottom="8em",
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow_y="auto",
        z_index="10",
        on_mount=ConfigurationManagementState.on_mount,
    )