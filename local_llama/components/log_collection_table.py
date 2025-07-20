import reflex as rx
from ..states.log_collection_table_state import LogCollectionTableState


def log_collection_table() -> rx.Component:
    """Modern table displaying log collection records."""
    return rx.vstack(
        # Modern divider
        rx.box(
            height="1px",
            width="100%",
            background="linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 20%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 80%, transparent 100%)",
            margin="3rem 0",
            box_shadow="0 0 20px rgba(255, 255, 255, 0.1)",
        ),
        
        # Table header
        rx.hstack(
            rx.hstack(
                rx.icon(
                    tag="table",
                    size=24,
                    color="white",
                ),
                rx.text(
                    "Recent Log Collections",
                    font_size="1.5rem",
                    font_weight="600",
                    color="white",
                ),
                spacing="3",
                align="center",
            ),
            rx.button(
                rx.icon(tag="refresh-cw", size=18),
                on_click=LogCollectionTableState.load_collections,
                size="2",
                variant="ghost",
                style={
                    "color": "rgba(255, 255, 255, 0.7)",
                    "_hover": {
                        "color": "white",
                        "background": "rgba(255, 255, 255, 0.1)",
                    },
                },
            ),
            justify="between",
            width="100%",
            margin_bottom="1.5rem",
        ),
        
        # Table container
        rx.box(
            rx.cond(
                LogCollectionTableState.is_loading,
                # Loading state
                rx.center(
                    rx.hstack(
                        rx.icon(
                            tag="loader",
                            size=20,
                            color="rgba(255, 255, 255, 0.5)",
                            animation="spin 1s linear infinite",
                        ),
                        rx.text(
                            "Loading collections...",
                            color="rgba(255, 255, 255, 0.5)",
                        ),
                        spacing="3",
                    ),
                    padding="3rem",
                ),
                # Table
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                # Status indicator column (for recent entries)
                                rx.table.column_header_cell(
                                    "",  # No header text for the dot column
                                    width="40px",
                                    style={"text_align": "center"}
                                ),
                                # Sortable Date/Time column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Date/Time"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "date",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("date"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Sortable Employee column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Employee"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "employee",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("employee"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Sortable Asset column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Asset"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "asset",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("asset"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Sortable Project column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Project"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "project",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("project"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Sortable Log Type column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Log Type"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "logtype",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("logtype"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Sortable Result column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Result"),
                                        rx.icon(
                                            tag=rx.cond(
                                                LogCollectionTableState.sort_column == "result",
                                                rx.cond(
                                                    LogCollectionTableState.sort_direction == "asc",
                                                    "chevron-up",
                                                    "chevron-down"
                                                ),
                                                "chevrons-up-down"
                                            ),
                                            size=14,
                                            color="rgba(255, 255, 255, 0.5)",
                                        ),
                                        spacing="2",
                                        align="center",
                                        cursor="pointer",
                                    ),
                                    on_click=lambda: LogCollectionTableState.sort_by_column("result"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Non-sortable Comments column
                                rx.table.column_header_cell("Comments"),
                                style={
                                    "background": "rgba(255, 255, 255, 0.05)",
                                    "border_bottom": "1px solid rgba(255, 255, 255, 0.1)",
                                }
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                LogCollectionTableState.collections,
                                lambda collection: rx.table.row(
                                    # Status indicator cell (recent entries, duplicates, and unresolved failures)
                                    rx.table.cell(
                                        rx.hstack(
                                            # Green pulsating dot for recent entries
                                            rx.cond(
                                                collection["is_recent"],
                                                rx.box(
                                                    rx.box(
                                                        width="8px",
                                                        height="8px",
                                                        border_radius="50%",
                                                        background="linear-gradient(45deg, #00ff88, #00cc66)",
                                                        box_shadow="0 0 8px #00ff88, 0 0 16px #00ff88, 0 0 24px #00ff88",
                                                        style={
                                                            "animation": "neonPulse 2s ease-in-out infinite",
                                                            "@keyframes neonPulse": {
                                                                "0%": {
                                                                    "box_shadow": "0 0 5px #00ff88, 0 0 10px #00ff88, 0 0 15px #00ff88",
                                                                    "opacity": "0.8"
                                                                },
                                                                "50%": {
                                                                    "box_shadow": "0 0 10px #00ff88, 0 0 20px #00ff88, 0 0 30px #00ff88",
                                                                    "opacity": "1"
                                                                },
                                                                "100%": {
                                                                    "box_shadow": "0 0 5px #00ff88, 0 0 10px #00ff88, 0 0 15px #00ff88",
                                                                    "opacity": "0.8"
                                                                }
                                                            }
                                                        }
                                                    ),
                                                    width="14px",
                                                    height="14px",
                                                    display="flex",
                                                    align_items="center",
                                                    justify_content="center"
                                                ),
                                                rx.box(width="14px", height="14px")  # Empty box same size when not recent
                                            ),
                                            # Second position: Yellow copy icon for duplicates
                                            rx.box(
                                                rx.cond(
                                                    collection["is_duplicate"],
                                                    rx.icon(
                                                        tag="copy",
                                                        size=14,
                                                        color="#ffff00",
                                                        style={
                                                            "filter": "drop-shadow(0 0 4px #ffff00) drop-shadow(0 0 8px #ffff00)",
                                                            "animation": "duplicatePulse 3s ease-in-out infinite",
                                                            "@keyframes duplicatePulse": {
                                                                "0%": {
                                                                    "filter": "drop-shadow(0 0 2px #ffff00) drop-shadow(0 0 4px #ffff00)",
                                                                    "opacity": "0.7"
                                                                },
                                                                "50%": {
                                                                    "filter": "drop-shadow(0 0 6px #ffff00) drop-shadow(0 0 12px #ffff00)",
                                                                    "opacity": "1"
                                                                },
                                                                "100%": {
                                                                    "filter": "drop-shadow(0 0 2px #ffff00) drop-shadow(0 0 4px #ffff00)",
                                                                    "opacity": "0.7"
                                                                }
                                                            }
                                                        }
                                                    ),
                                                    rx.box()  # Empty when not duplicate
                                                ),
                                                width="14px",
                                                height="14px",
                                                display="flex",
                                                align_items="center",
                                                justify_content="center"
                                            ),
                                            # Third position: Red hard disk icon for unresolved failures
                                            rx.box(
                                                rx.cond(
                                                    collection["is_unresolved_failure"],
                                                    rx.icon(
                                                        tag="hard_drive",
                                                        size=14,
                                                        color="#ff4444",
                                                        style={
                                                            "filter": "drop-shadow(0 0 4px #ff4444) drop-shadow(0 0 8px #ff4444)",
                                                            "animation": "failurePulse 2.5s ease-in-out infinite",
                                                            "@keyframes failurePulse": {
                                                                "0%": {
                                                                    "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                    "opacity": "0.7"
                                                                },
                                                                "50%": {
                                                                    "filter": "drop-shadow(0 0 6px #ff4444) drop-shadow(0 0 12px #ff4444)",
                                                                    "opacity": "1"
                                                                },
                                                                "100%": {
                                                                    "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                    "opacity": "0.7"
                                                                }
                                                            }
                                                        }
                                                    ),
                                                    rx.box()  # Empty when not unresolved failure
                                                ),
                                                width="14px",
                                                height="14px",
                                                display="flex",
                                                align_items="center",
                                                justify_content="center"
                                            ),
                                            spacing="2",
                                            align="center",
                                            justify="center",
                                        ),
                                        text_align="center",
                                        vertical_align="middle",
                                        padding="0.5rem",
                                    ),
                                    # Date/Time cell
                                    rx.table.cell(
                                        rx.text(
                                            collection["date"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            collection["employee"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            collection["asset"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            collection["project"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            collection["logtype"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(
                                                collection["result"],
                                                font_size="0.75rem",
                                                font_weight="500",
                                            ),
                                            padding="0.25rem 0.75rem",
                                            border_radius="12px",
                                            background=rx.cond(
                                                collection["result"] == "Success",
                                                "rgba(34, 197, 94, 0.2)",
                                                rx.cond(
                                                    collection["result"] == "Failed",
                                                    "rgba(239, 68, 68, 0.2)",
                                                    "rgba(251, 146, 60, 0.2)"
                                                )
                                            ),
                                            border=rx.cond(
                                                collection["result"] == "Success",
                                                "1px solid rgba(34, 197, 94, 0.3)",
                                                rx.cond(
                                                    collection["result"] == "Failed",
                                                    "1px solid rgba(239, 68, 68, 0.3)",
                                                    "1px solid rgba(251, 146, 60, 0.3)"
                                                )
                                            ),
                                            color=rx.cond(
                                                collection["result"] == "Success",
                                                "rgba(134, 239, 172, 1)",
                                                rx.cond(
                                                    collection["result"] == "Failed",
                                                    "rgba(252, 165, 165, 1)",
                                                    "rgba(253, 186, 116, 1)"
                                                )
                                            ),
                                        )
                                    ),
                                    rx.table.cell(
                                        rx.text(
                                            collection["comments"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.7)",
                                            max_width="200px",
                                            overflow="hidden",
                                            text_overflow="ellipsis",
                                            white_space="nowrap",
                                        )
                                    ),
                                    _hover={
                                        "background": "rgba(255, 255, 255, 0.02)",
                                    },
                                )
                            ),
                        ),
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.01)",
                            "border": "1px solid rgba(255, 255, 255, 0.05)",
                            "border_radius": "12px",
                            "overflow": "hidden",
                        }
                    ),
                    type="auto",
                    scrollbars="vertical",
                    style={
                        "height": "400px",
                        "width": "100%",
                    }
                ),
            ),
            width="100%",
        ),
        
        # Pagination controls
        rx.hstack(
            # Left side - Record info
            rx.text(
                LogCollectionTableState.records_display_text,
                font_size="0.875rem",
                color="rgba(255, 255, 255, 0.7)",
            ),
            
            # Right side - Navigation controls
            rx.hstack(
                # First page button
                rx.button(
                    rx.icon(tag="chevrons-left", size=16),
                    on_click=LogCollectionTableState.first_page,
                    disabled=LogCollectionTableState.current_page == 1,
                    size="2",
                    variant="ghost",
                    style={
                        "color": "rgba(255, 255, 255, 0.7)",
                        "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                        "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                    },
                ),
                # Previous page button
                rx.button(
                    rx.icon(tag="chevron-left", size=16),
                    on_click=LogCollectionTableState.previous_page,
                    disabled=LogCollectionTableState.current_page == 1,
                    size="2",
                    variant="ghost",
                    style={
                        "color": "rgba(255, 255, 255, 0.7)",
                        "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                        "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                    },
                ),
                # Page info
                rx.text(
                    f"Page {LogCollectionTableState.current_page} of {LogCollectionTableState.total_pages}",
                    font_size="0.875rem",
                    color="rgba(255, 255, 255, 0.9)",
                    margin="0 1rem",
                ),
                # Next page button
                rx.button(
                    rx.icon(tag="chevron-right", size=16),
                    on_click=LogCollectionTableState.next_page,
                    disabled=LogCollectionTableState.current_page == LogCollectionTableState.total_pages,
                    size="2",
                    variant="ghost",
                    style={
                        "color": "rgba(255, 255, 255, 0.7)",
                        "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                        "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                    },
                ),
                # Last page button
                rx.button(
                    rx.icon(tag="chevrons-right", size=16),
                    on_click=LogCollectionTableState.last_page,
                    disabled=LogCollectionTableState.current_page == LogCollectionTableState.total_pages,
                    size="2",
                    variant="ghost",
                    style={
                        "color": "rgba(255, 255, 255, 0.7)",
                        "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                        "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                    },
                ),
                spacing="1",
            ),
            
            justify="between",
            align="center",
            width="100%",
            margin_top="1.5rem",
            padding="1rem",
            border_top="1px solid rgba(255, 255, 255, 0.1)",
        ),
        
        width="90%",
        max_width="1400px",
        margin="0 auto",
        on_mount=LogCollectionTableState.load_collections,
    )