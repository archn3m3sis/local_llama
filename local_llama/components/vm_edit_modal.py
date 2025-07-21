"""Virtual Machine Edit Modal Component."""
import reflex as rx
from ..states.vm_creation_table_state import VMCreationTableState

def vm_edit_modal() -> rx.Component:
    """Modal for editing VM properties."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Modal Header
                rx.hstack(
                    rx.heading(
                        f"Edit Virtual Machine #{VMCreationTableState.editing_vm_id}",
                        size="5",
                        weight="bold",
                        color="white",
                    ),
                    rx.spacer(),
                    rx.icon(
                        tag="x",
                        size=24,
                        cursor="pointer",
                        on_click=VMCreationTableState.close_edit_modal,
                        color="rgba(255, 255, 255, 0.7)",
                        _hover={"color": "white"},
                    ),
                    width="100%",
                    align="center",
                    margin_bottom="1rem",
                ),
                
                # VM Status
                rx.vstack(
                    rx.text("VM Status", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        VMCreationTableState.vm_statuses,
                        placeholder="Select status...",
                        value=VMCreationTableState.edit_vm_status,
                        on_change=VMCreationTableState.set_edit_vm_status,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                    margin_bottom="1rem",
                ),
                
                # Hardware Specs
                rx.text("Hardware Specifications", color="rgba(255, 255, 255, 0.8)", font_size="0.95rem", font_weight="500", margin_bottom="0.5rem"),
                rx.hstack(
                    rx.vstack(
                        rx.text("RAM (MB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.input(
                            placeholder="16384",
                            value=VMCreationTableState.edit_ram_mb,
                            on_change=VMCreationTableState.set_edit_ram_mb,
                            width="100%",
                            type="number",
                            min="1",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "white",
                                "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                                "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                            },
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.text("CPU Cores", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.input(
                            placeholder="4",
                            value=VMCreationTableState.edit_cpu_cores,
                            on_change=VMCreationTableState.set_edit_cpu_cores,
                            width="100%",
                            type="number",
                            min="1",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "white",
                                "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                                "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                            },
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.text("Disk (MB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.input(
                            placeholder="262144",
                            value=VMCreationTableState.edit_disk_size_mb,
                            on_change=VMCreationTableState.set_edit_disk_size_mb,
                            width="100%",
                            type="number",
                            min="1",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "white",
                                "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                                "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                            },
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    spacing="3",
                    width="100%",
                    margin_bottom="1.5rem",
                ),
                
                # Security Scans
                rx.vstack(
                    rx.text("Security Scans", color="rgba(255, 255, 255, 0.8)", font_size="0.95rem", font_weight="500"),
                    rx.vstack(
                        rx.hstack(
                            rx.checkbox(
                                checked=VMCreationTableState.edit_acas_scan,
                                on_change=VMCreationTableState.toggle_edit_acas_scan,
                                color_scheme="green",
                            ),
                            rx.text("ACAS Scan Completed", color="rgba(255, 255, 255, 0.8)", font_size="0.85rem"),
                            spacing="2",
                            align="center",
                        ),
                        rx.hstack(
                            rx.checkbox(
                                checked=VMCreationTableState.edit_scap_scan,
                                on_change=VMCreationTableState.toggle_edit_scap_scan,
                                color_scheme="green",
                            ),
                            rx.text("SCAP Scan Completed", color="rgba(255, 255, 255, 0.8)", font_size="0.85rem"),
                            spacing="2",
                            align="center",
                        ),
                        spacing="2",
                    ),
                    width="100%",
                    spacing="2",
                    margin_bottom="1.5rem",
                ),
                
                # Action Buttons
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=VMCreationTableState.close_edit_modal,
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(148, 163, 184, 0.15) 0%, rgba(100, 116, 139, 0.1) 100%)",
                            "border": "1px solid rgba(148, 163, 184, 0.25)",
                            "color": "white",
                            "font_weight": "500",
                            "border_radius": "8px",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(148, 163, 184, 0.25) 0%, rgba(100, 116, 139, 0.2) 100%)",
                                "border": "1px solid rgba(148, 163, 184, 0.4)",
                            },
                        }
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="save", size=18),
                            rx.text("Save Changes"),
                            spacing="2",
                        ),
                        on_click=VMCreationTableState.update_vm,
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.15) 100%)",
                            "border": "1px solid rgba(59, 130, 246, 0.3)",
                            "color": "white",
                            "font_weight": "600",
                            "border_radius": "8px",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.25) 100%)",
                                "border": "1px solid rgba(59, 130, 246, 0.4)",
                                "box_shadow": "0 4px 16px rgba(59, 130, 246, 0.3)",
                            },
                        }
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                
                width="100%",
                spacing="4",
            ),
            style={
                "background": "linear-gradient(135deg, rgba(17, 24, 39, 0.98) 0%, rgba(31, 41, 55, 0.95) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "12px",
                "padding": "2rem",
                "box_shadow": "0 10px 40px rgba(0, 0, 0, 0.5)",
                "max_width": "600px",
                "width": "90%",
            }
        ),
        open=VMCreationTableState.show_edit_modal,
    )