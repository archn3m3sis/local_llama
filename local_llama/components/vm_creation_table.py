"""Virtual Machine Creation Table Component."""
import reflex as rx
from ..states.vm_creation_table_state import VMCreationTableState
from .vm_edit_modal import vm_edit_modal

def vm_creation_table() -> rx.Component:
    """Virtual Machine Creation table component."""
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
                    tag="server",
                    size=24,
                    color="white",
                ),
                rx.text(
                    "Virtual Machine Records",
                    font_size="1.5rem",
                    font_weight="600",
                    color="white",
                ),
                spacing="3",
                align="center",
            ),
            rx.button(
                rx.icon(tag="refresh-cw", size=18),
                on_click=VMCreationTableState.load_vm_records,
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
                VMCreationTableState.loading,
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
                            "Loading virtual machines...",
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
                                # Status indicator column
                                rx.table.column_header_cell(
                                    "",
                                    width="40px",
                                    style={"text_align": "center"}
                                ),
                                # ID column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("ID"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "virtmachine_id",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("virtmachine_id"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Creator column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Creator"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "creator",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("creator"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Asset column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Asset"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "asset_name",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("asset_name"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Project column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Project"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "project_name",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("project_name"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Source column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Source"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "virt_source",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("virt_source"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Type column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Type"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "vm_type",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("vm_type"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Status column
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.text("Status"),
                                        rx.icon(
                                            tag=rx.cond(
                                                VMCreationTableState.sort_column == "vm_status",
                                                rx.cond(
                                                    VMCreationTableState.sort_order == "asc",
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
                                    on_click=lambda: VMCreationTableState.sort_records("vm_status"),
                                    style={
                                        "_hover": {"background": "rgba(255, 255, 255, 0.08)"},
                                        "user_select": "none",
                                    }
                                ),
                                # Specs column
                                rx.table.column_header_cell("Specs"),
                                # Scans column
                                rx.table.column_header_cell("Scans"),
                                # Actions column
                                rx.table.column_header_cell("Actions", width="100px"),
                                style={
                                    "background": "rgba(255, 255, 255, 0.05)",
                                    "border_bottom": "1px solid rgba(255, 255, 255, 0.1)",
                                }
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                VMCreationTableState.current_page_records,
                                lambda record: rx.table.row(
                                    # Status indicator cell
                                    rx.table.cell(
                                        rx.hstack(
                                            # Status icon - Green play for ready, Orange pause for waiting scans
                                            rx.box(
                                                rx.cond(
                                                    record["is_ready"],
                                                    rx.icon(
                                                        tag="play",
                                                        size=14,
                                                        color="#00ff88",
                                                        style={
                                                            "filter": "drop-shadow(0 0 4px #00ff88) drop-shadow(0 0 8px #00ff88)",
                                                            "animation": "readyPulse 2s ease-in-out infinite",
                                                            "@keyframes readyPulse": {
                                                                "0%": {
                                                                    "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                    "opacity": "0.8"
                                                                },
                                                                "50%": {
                                                                    "filter": "drop-shadow(0 0 6px #00ff88) drop-shadow(0 0 12px #00ff88)",
                                                                    "opacity": "1"
                                                                },
                                                                "100%": {
                                                                    "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                    "opacity": "0.8"
                                                                }
                                                            }
                                                        }
                                                    ),
                                                    rx.cond(
                                                        record["is_waiting_scans"],
                                                        rx.icon(
                                                            tag="scan_barcode",
                                                            size=14,
                                                            color="#88ff00",
                                                            style={
                                                                "filter": "drop-shadow(0 0 4px #88ff00) drop-shadow(0 0 8px #88ff00)",
                                                                "animation": "waitingPulse 2s ease-in-out infinite",
                                                                "@keyframes waitingPulse": {
                                                                    "0%": {
                                                                        "filter": "drop-shadow(0 0 2px #88ff00) drop-shadow(0 0 4px #88ff00)",
                                                                        "opacity": "0.8"
                                                                    },
                                                                    "50%": {
                                                                        "filter": "drop-shadow(0 0 6px #88ff00) drop-shadow(0 0 12px #88ff00)",
                                                                        "opacity": "1"
                                                                    },
                                                                    "100%": {
                                                                        "filter": "drop-shadow(0 0 2px #88ff00) drop-shadow(0 0 4px #88ff00)",
                                                                        "opacity": "0.8"
                                                                    }
                                                                }
                                                            }
                                                        ),
                                                        rx.cond(
                                                            record["is_testing"],
                                                            rx.icon(
                                                                tag="flask-conical",
                                                                size=14,
                                                                color="#ff8800",
                                                                style={
                                                                    "filter": "drop-shadow(0 0 4px #ff8800) drop-shadow(0 0 8px #ff8800)",
                                                                    "animation": "testingPulse 2s ease-in-out infinite",
                                                                    "@keyframes testingPulse": {
                                                                        "0%": {
                                                                            "filter": "drop-shadow(0 0 2px #ff8800) drop-shadow(0 0 4px #ff8800)",
                                                                            "opacity": "0.8"
                                                                        },
                                                                        "50%": {
                                                                            "filter": "drop-shadow(0 0 6px #ff8800) drop-shadow(0 0 12px #ff8800)",
                                                                            "opacity": "1"
                                                                        },
                                                                        "100%": {
                                                                            "filter": "drop-shadow(0 0 2px #ff8800) drop-shadow(0 0 4px #ff8800)",
                                                                            "opacity": "0.8"
                                                                        }
                                                                    }
                                                                }
                                                            ),
                                                            rx.cond(
                                                                record["is_broken"],
                                                                rx.icon(
                                                                    tag="wrench",
                                                                    size=14,
                                                                    color="#ff0000",
                                                                    style={
                                                                        "filter": "drop-shadow(0 0 4px #ff0000) drop-shadow(0 0 8px #ff0000)",
                                                                        "animation": "brokenPulse 2s ease-in-out infinite",
                                                                        "@keyframes brokenPulse": {
                                                                            "0%": {
                                                                                "filter": "drop-shadow(0 0 2px #ff0000) drop-shadow(0 0 4px #ff0000)",
                                                                                "opacity": "0.8"
                                                                            },
                                                                            "50%": {
                                                                                "filter": "drop-shadow(0 0 6px #ff0000) drop-shadow(0 0 12px #ff0000)",
                                                                                "opacity": "1"
                                                                            },
                                                                            "100%": {
                                                                                "filter": "drop-shadow(0 0 2px #ff0000) drop-shadow(0 0 4px #ff0000)",
                                                                                "opacity": "0.8"
                                                                            }
                                                                        }
                                                                    }
                                                                ),
                                                                rx.box()  # Empty when not in any special status
                                                            )
                                                        )
                                                    )
                                                ),
                                                width="14px",
                                                height="14px",
                                                display="flex",
                                                align_items="center",
                                                justify_content="center"
                                            ),
                                            # Green pulsating dot for recent entries
                                            rx.cond(
                                                record["is_recent"],
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
                                            # Yellow copy icon for duplicates
                                            rx.box(
                                                rx.cond(
                                                    record["is_duplicate"],
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
                                            spacing="2",
                                            align="center",
                                            justify="center",
                                        ),
                                        text_align="center",
                                        vertical_align="middle",
                                        padding="0.5rem",
                                    ),
                                    # ID cell
                                    rx.table.cell(
                                        rx.text(
                                            record["virtmachine_id"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    # Creator cell
                                    rx.table.cell(
                                        rx.vstack(
                                            rx.text(
                                                record["creator"],
                                                font_size="0.875rem",
                                                color="rgba(255, 255, 255, 0.9)",
                                                font_weight="500",
                                            ),
                                            rx.text(
                                                f"ID: {record['employee_id']}",
                                                font_size="0.75rem",
                                                color="rgba(255, 255, 255, 0.5)",
                                            ),
                                            spacing="0",
                                        )
                                    ),
                                    # Asset cell
                                    rx.table.cell(
                                        rx.vstack(
                                            rx.text(
                                                record["asset_name"],
                                                font_size="0.875rem",
                                                color="rgba(255, 255, 255, 0.9)",
                                                font_weight="500",
                                            ),
                                            rx.text(
                                                record["barcode"],
                                                font_size="0.75rem",
                                                color="rgba(255, 255, 255, 0.5)",
                                            ),
                                            spacing="0",
                                        )
                                    ),
                                    # Project cell
                                    rx.table.cell(
                                        rx.text(
                                            record["project_name"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    # Source cell
                                    rx.table.cell(
                                        rx.text(
                                            record["virt_source"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    # Type cell
                                    rx.table.cell(
                                        rx.text(
                                            record["vm_type"],
                                            font_size="0.875rem",
                                            color="rgba(255, 255, 255, 0.9)",
                                        )
                                    ),
                                    # Status cell
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(
                                                record["vm_status"],
                                                font_size="0.75rem",
                                                font_weight="500",
                                            ),
                                            padding="0.25rem 0.75rem",
                                            border_radius="12px",
                                            background=rx.cond(
                                                record["status_color"] == "green",
                                                "rgba(34, 197, 94, 0.2)",
                                                rx.cond(
                                                    record["status_color"] == "yellow",
                                                    "rgba(251, 146, 60, 0.2)",
                                                    "rgba(239, 68, 68, 0.2)"
                                                )
                                            ),
                                            border=rx.cond(
                                                record["status_color"] == "green",
                                                "1px solid rgba(34, 197, 94, 0.3)",
                                                rx.cond(
                                                    record["status_color"] == "yellow",
                                                    "1px solid rgba(251, 146, 60, 0.3)",
                                                    "1px solid rgba(239, 68, 68, 0.3)"
                                                )
                                            ),
                                            color=rx.cond(
                                                record["status_color"] == "green",
                                                "rgba(134, 239, 172, 1)",
                                                rx.cond(
                                                    record["status_color"] == "yellow",
                                                    "rgba(253, 186, 116, 1)",
                                                    "rgba(252, 165, 165, 1)"
                                                )
                                            ),
                                        )
                                    ),
                                    # Specs cell
                                    rx.table.cell(
                                        rx.text(
                                            f"{record['ram_mb']}MB | {record['cpu_cores']}C | {record['disk_size_mb']}MB",
                                            font_size="0.75rem",
                                            color="rgba(255, 255, 255, 0.7)",
                                        )
                                    ),
                                    # Scans cell
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.icon(
                                                tag=rx.cond(
                                                    record["acas_scan"],
                                                    "shield-check",
                                                    "shield-x"
                                                ),
                                                size=16,
                                                color=rx.cond(
                                                    record["acas_scan"],
                                                    "#00ff88",
                                                    "#ff4444"
                                                ),
                                                style=rx.cond(
                                                    record["acas_scan"],
                                                    {
                                                        "filter": "drop-shadow(0 0 4px #00ff88) drop-shadow(0 0 8px #00ff88)",
                                                        "animation": "scanPulseGreen 3s ease-in-out infinite",
                                                        "@keyframes scanPulseGreen": {
                                                            "0%": {
                                                                "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                "opacity": "0.8"
                                                            },
                                                            "50%": {
                                                                "filter": "drop-shadow(0 0 6px #00ff88) drop-shadow(0 0 12px #00ff88)",
                                                                "opacity": "1"
                                                            },
                                                            "100%": {
                                                                "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                "opacity": "0.8"
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "filter": "drop-shadow(0 0 4px #ff4444) drop-shadow(0 0 8px #ff4444)",
                                                        "animation": "scanPulseRed 3s ease-in-out infinite",
                                                        "@keyframes scanPulseRed": {
                                                            "0%": {
                                                                "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                "opacity": "0.8"
                                                            },
                                                            "50%": {
                                                                "filter": "drop-shadow(0 0 6px #ff4444) drop-shadow(0 0 12px #ff4444)",
                                                                "opacity": "1"
                                                            },
                                                            "100%": {
                                                                "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                "opacity": "0.8"
                                                            }
                                                        }
                                                    }
                                                ),
                                            ),
                                            rx.icon(
                                                tag=rx.cond(
                                                    record["scap_scan"],
                                                    "file-check",
                                                    "file-x"
                                                ),
                                                size=16,
                                                color=rx.cond(
                                                    record["scap_scan"],
                                                    "#00ff88",
                                                    "#ff4444"
                                                ),
                                                style=rx.cond(
                                                    record["scap_scan"],
                                                    {
                                                        "filter": "drop-shadow(0 0 4px #00ff88) drop-shadow(0 0 8px #00ff88)",
                                                        "animation": "scanPulseGreen2 3s ease-in-out infinite",
                                                        "@keyframes scanPulseGreen2": {
                                                            "0%": {
                                                                "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                "opacity": "0.8"
                                                            },
                                                            "50%": {
                                                                "filter": "drop-shadow(0 0 6px #00ff88) drop-shadow(0 0 12px #00ff88)",
                                                                "opacity": "1"
                                                            },
                                                            "100%": {
                                                                "filter": "drop-shadow(0 0 2px #00ff88) drop-shadow(0 0 4px #00ff88)",
                                                                "opacity": "0.8"
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "filter": "drop-shadow(0 0 4px #ff4444) drop-shadow(0 0 8px #ff4444)",
                                                        "animation": "scanPulseRed2 3s ease-in-out infinite",
                                                        "@keyframes scanPulseRed2": {
                                                            "0%": {
                                                                "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                "opacity": "0.8"
                                                            },
                                                            "50%": {
                                                                "filter": "drop-shadow(0 0 6px #ff4444) drop-shadow(0 0 12px #ff4444)",
                                                                "opacity": "1"
                                                            },
                                                            "100%": {
                                                                "filter": "drop-shadow(0 0 2px #ff4444) drop-shadow(0 0 4px #ff4444)",
                                                                "opacity": "0.8"
                                                            }
                                                        }
                                                    }
                                                ),
                                            ),
                                            spacing="3",
                                            align="center",
                                        )
                                    ),
                                    # Actions cell
                                    rx.table.cell(
                                        rx.button(
                                            rx.hstack(
                                                rx.icon(tag="pencil", size=16),
                                                rx.text("Edit", size="2"),
                                                spacing="1",
                                                align="center",
                                            ),
                                            size="2",
                                            variant="ghost",
                                            on_click=VMCreationTableState.open_edit_modal(record["virtmachine_id"]),
                                            style={
                                                "background": "rgba(59, 130, 246, 0.1)",
                                                "border": "1px solid rgba(59, 130, 246, 0.2)",
                                                "color": "rgba(147, 197, 253, 1)",
                                                "_hover": {
                                                    "background": "rgba(59, 130, 246, 0.2)",
                                                    "border": "1px solid rgba(59, 130, 246, 0.3)",
                                                    "transform": "scale(1.05)",
                                                    "box_shadow": "0 0 10px rgba(59, 130, 246, 0.3)",
                                                },
                                                "cursor": "pointer",
                                                "padding": "0.5rem 0.75rem",
                                                "border_radius": "6px",
                                            }
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
                f"Showing {VMCreationTableState.current_page_start} - {VMCreationTableState.current_page_end} of {VMCreationTableState.total_records} records",
                font_size="0.875rem",
                color="rgba(255, 255, 255, 0.7)",
            ),
            
            # Right side - Navigation controls
            rx.hstack(
                # First page button
                rx.button(
                    rx.icon(tag="chevrons-left", size=16),
                    on_click=lambda: VMCreationTableState.go_to_page(1),
                    disabled=VMCreationTableState.current_page == 1,
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
                    on_click=VMCreationTableState.prev_page,
                    disabled=VMCreationTableState.current_page == 1,
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
                    f"Page {VMCreationTableState.current_page} of {VMCreationTableState.total_pages}",
                    font_size="0.875rem",
                    color="rgba(255, 255, 255, 0.9)",
                    margin="0 1rem",
                ),
                # Next page button
                rx.button(
                    rx.icon(tag="chevron-right", size=16),
                    on_click=VMCreationTableState.next_page,
                    disabled=VMCreationTableState.current_page == VMCreationTableState.total_pages,
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
                    on_click=lambda: VMCreationTableState.go_to_page(VMCreationTableState.total_pages),
                    disabled=VMCreationTableState.current_page == VMCreationTableState.total_pages,
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
        
        # Edit Modal
        vm_edit_modal(),
        
        width="90%",
        max_width="1400px",
        margin="0 auto",
        on_mount=VMCreationTableState.load_vm_records,
    )