import reflex as rx
from ..states.vm_state import VMState


def vm_table() -> rx.Component:
    """Modern table displaying virtual machine records."""
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
                    "Virtual Machine Fleet",
                    font_size="1.5rem",
                    font_weight="600",
                    color="white",
                ),
                spacing="3",
                align="center",
            ),
            rx.button(
                rx.icon(tag="refresh-cw", size=18),
                on_click=VMState.load_virtual_machines,
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
                len(VMState.virtual_machines) == 0,
                # Empty state
                rx.center(
                    rx.vstack(
                        rx.icon(
                            tag="server",
                            size=48,
                            color="rgba(255, 255, 255, 0.3)",
                        ),
                        rx.text(
                            "No virtual machines found",
                            color="rgba(255, 255, 255, 0.5)",
                            font_size="1.1rem",
                        ),
                        rx.text(
                            "Create your first VM using the form above",
                            color="rgba(255, 255, 255, 0.3)",
                            font_size="0.9rem",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    padding="3rem",
                ),
                # Table
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                # VM ID column
                                rx.table.column_header_cell(
                                    rx.text("VM ID", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="80px",
                                    style={"text_align": "center"}
                                ),
                                # Asset column
                                rx.table.column_header_cell(
                                    rx.text("Asset", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="150px",
                                ),
                                # Project column
                                rx.table.column_header_cell(
                                    rx.text("Project", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="100px",
                                ),
                                # VM Type column
                                rx.table.column_header_cell(
                                    rx.text("VM Type", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="150px",
                                ),
                                # Virtualization Server column
                                rx.table.column_header_cell(
                                    rx.text("Server", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="150px",
                                ),
                                # Creator column
                                rx.table.column_header_cell(
                                    rx.text("Created By", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="120px",
                                ),
                                # Specifications column
                                rx.table.column_header_cell(
                                    rx.text("Specs", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="120px",
                                ),
                                # Scans column
                                rx.table.column_header_cell(
                                    rx.text("Scans", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="100px",
                                    style={"text_align": "center"}
                                ),
                                # Status column
                                rx.table.column_header_cell(
                                    rx.text("Status", color="rgba(255, 255, 255, 0.9)", font_weight="600"),
                                    width="200px",
                                ),
                                style={
                                    "background": "rgba(255, 255, 255, 0.05)",
                                    "border_bottom": "1px solid rgba(255, 255, 255, 0.1)",
                                }
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                VMState.virtual_machines,
                                lambda vm, index: rx.table.row(
                                    # VM ID
                                    rx.table.cell(
                                        rx.text(
                                            vm["virtmachine_id"], 
                                            color="rgba(59, 130, 246, 0.9)",
                                            font_weight="600",
                                            font_size="0.9rem",
                                        ),
                                        style={"text_align": "center"}
                                    ),
                                    # Asset Name
                                    rx.table.cell(
                                        rx.text(
                                            vm["asset_name"], 
                                            color="white",
                                            font_size="0.9rem",
                                        ),
                                    ),
                                    # Project Name
                                    rx.table.cell(
                                        rx.text(
                                            vm["project_name"], 
                                            color="rgba(255, 255, 255, 0.8)",
                                            font_size="0.9rem",
                                        ),
                                    ),
                                    # VM Type
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(
                                                vm["vm_type"], 
                                                color="white",
                                                font_size="0.8rem",
                                                font_weight="500",
                                            ),
                                            padding="0.3rem 0.6rem",
                                            background="rgba(139, 92, 246, 0.2)",
                                            border="1px solid rgba(139, 92, 246, 0.4)",
                                            border_radius="6px",
                                        ),
                                    ),
                                    # Virtualization Server
                                    rx.table.cell(
                                        rx.text(
                                            vm["virt_source"], 
                                            color="rgba(16, 185, 129, 0.9)",
                                            font_size="0.9rem",
                                            font_weight="500",
                                        ),
                                    ),
                                    # Creator
                                    rx.table.cell(
                                        rx.text(
                                            vm["creator_name"], 
                                            color="rgba(255, 255, 255, 0.8)",
                                            font_size="0.9rem",
                                        ),
                                    ),
                                    # Specifications
                                    rx.table.cell(
                                        rx.vstack(
                                            rx.cond(
                                                vm["ram_gb"],
                                                rx.text(f"{vm['ram_gb']}GB RAM", color="rgba(255, 255, 255, 0.7)", font_size="0.8rem"),
                                                rx.text("- GB RAM", color="rgba(255, 255, 255, 0.4)", font_size="0.8rem"),
                                            ),
                                            rx.cond(
                                                vm["cpu_cores"],
                                                rx.text(f"{vm['cpu_cores']} Cores", color="rgba(255, 255, 255, 0.7)", font_size="0.8rem"),
                                                rx.text("- Cores", color="rgba(255, 255, 255, 0.4)", font_size="0.8rem"),
                                            ),
                                            rx.cond(
                                                vm["disk_size_gb"],
                                                rx.text(f"{vm['disk_size_gb']}GB Disk", color="rgba(255, 255, 255, 0.7)", font_size="0.8rem"),
                                                rx.text("- GB Disk", color="rgba(255, 255, 255, 0.4)", font_size="0.8rem"),
                                            ),
                                            spacing="1",
                                            align="start",
                                        ),
                                    ),
                                    # Scans
                                    rx.table.cell(
                                        rx.hstack(
                                            rx.cond(
                                                vm["acas_scan"],
                                                rx.icon(tag="check", size=16, color="rgba(34, 197, 94, 0.9)"),
                                                rx.icon(tag="x", size=16, color="rgba(239, 68, 68, 0.7)"),
                                            ),
                                            rx.cond(
                                                vm["scap_scan"],
                                                rx.icon(tag="check", size=16, color="rgba(34, 197, 94, 0.9)"),
                                                rx.icon(tag="x", size=16, color="rgba(239, 68, 68, 0.7)"),
                                            ),
                                            spacing="2",
                                            justify="center",
                                        ),
                                        style={"text_align": "center"}
                                    ),
                                    # Status
                                    rx.table.cell(
                                        rx.box(
                                            rx.text(
                                                vm["vm_status"], 
                                                color=rx.cond(
                                                    vm["vm_status"].contains("Fully Functional"),
                                                    "rgba(34, 197, 94, 0.9)",
                                                    rx.cond(
                                                        vm["vm_status"].contains("Machine Created"),
                                                        "rgba(245, 158, 11, 0.9)",
                                                        "rgba(239, 68, 68, 0.9)"
                                                    )
                                                ),
                                                font_size="0.8rem",
                                                font_weight="500",
                                            ),
                                            padding="0.3rem 0.6rem",
                                            background=rx.cond(
                                                vm["vm_status"].contains("Fully Functional"),
                                                "rgba(34, 197, 94, 0.1)",
                                                rx.cond(
                                                    vm["vm_status"].contains("Machine Created"),
                                                    "rgba(245, 158, 11, 0.1)",
                                                    "rgba(239, 68, 68, 0.1)"
                                                )
                                            ),
                                            border=rx.cond(
                                                vm["vm_status"].contains("Fully Functional"),
                                                "1px solid rgba(34, 197, 94, 0.3)",
                                                rx.cond(
                                                    vm["vm_status"].contains("Machine Created"),
                                                    "1px solid rgba(245, 158, 11, 0.3)",
                                                    "1px solid rgba(239, 68, 68, 0.3)"
                                                )
                                            ),
                                            border_radius="6px",
                                        ),
                                    ),
                                    style={
                                        "border_bottom": "1px solid rgba(255, 255, 255, 0.05)",
                                        "_hover": {"background": "rgba(255, 255, 255, 0.02)"},
                                    }
                                )
                            )
                        ),
                        size="2",
                        variant="surface",
                        style={
                            "background": "rgba(255, 255, 255, 0.02)",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "12px",
                            "overflow": "hidden",
                        }
                    ),
                    height="600px",
                ),
            ),
            width="100%",
        ),
        
        # Pagination
        rx.cond(
            VMState.total_pages > 1,
            rx.hstack(
                rx.text(
                    f"Showing {(VMState.current_page - 1) * VMState.items_per_page + 1}-{rx.cond(VMState.current_page * VMState.items_per_page > VMState.total_vms, VMState.total_vms, VMState.current_page * VMState.items_per_page)} of {VMState.total_vms} VMs",
                    color="rgba(255, 255, 255, 0.6)",
                    font_size="0.9rem",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon(tag="chevron-left", size=16),
                        size="2",
                        variant="ghost",
                        on_click=VMState.prev_page,
                        disabled=VMState.current_page == 1,
                        style={
                            "color": "rgba(255, 255, 255, 0.7)",
                            "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                            "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                        },
                    ),
                    rx.text(
                        f"Page {VMState.current_page} of {VMState.total_pages}",
                        color="white",
                        font_size="0.9rem",
                        padding="0 1rem",
                    ),
                    rx.button(
                        rx.icon(tag="chevron-right", size=16),
                        size="2",
                        variant="ghost",
                        on_click=VMState.next_page,
                        disabled=VMState.current_page == VMState.total_pages,
                        style={
                            "color": "rgba(255, 255, 255, 0.7)",
                            "_hover": {"color": "white", "background": "rgba(255, 255, 255, 0.1)"},
                            "_disabled": {"color": "rgba(255, 255, 255, 0.3)", "cursor": "not-allowed"},
                        },
                    ),
                    spacing="2",
                    align="center",
                ),
                justify="between",
                width="100%",
                padding="1rem 0",
            ),
        ),
        
        width="100%",
        spacing="0",
        on_mount=VMState.load_virtual_machines,
    )