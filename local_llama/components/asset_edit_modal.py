"""Asset Edit Modal Component"""
import reflex as rx
from ..states.assets_state import AssetsState


def asset_edit_modal() -> rx.Component:
    """Modal for editing asset details."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading(
                        "Edit Asset",
                        size="5",
                        weight="bold",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x"),
                            size="1",
                            radius="full",
                            variant="ghost",
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                
                rx.divider(),
                
                # Form fields
                rx.form(
                    rx.vstack(
                        # Asset Name
                        rx.vstack(
                            rx.text("Asset Name", size="2", weight="medium"),
                            rx.input(
                                value=AssetsState.edit_asset_name,
                                on_change=AssetsState.set_edit_asset_name,
                                placeholder="Enter asset name",
                                size="3",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Project Selection
                        rx.vstack(
                            rx.text("Project", size="2", weight="medium"),
                            rx.select(
                                AssetsState.projects,
                                value=AssetsState.edit_project,
                                on_change=AssetsState.set_edit_project,
                                placeholder="Select project",
                                size="3",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Building and Floor
                        rx.hstack(
                            rx.vstack(
                                rx.text("Building", size="2", weight="medium"),
                                rx.select(
                                    AssetsState.buildings,
                                    value=AssetsState.edit_building,
                                    on_change=AssetsState.set_edit_building,
                                    placeholder="Select building",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Floor", size="2", weight="medium"),
                                rx.select(
                                    AssetsState.floors,
                                    value=AssetsState.edit_floor,
                                    on_change=AssetsState.set_edit_floor,
                                    placeholder="Select floor",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        
                        # System Type and OS
                        rx.hstack(
                            rx.vstack(
                                rx.text("System Type", size="2", weight="medium"),
                                rx.select(
                                    AssetsState.systypes,
                                    value=AssetsState.edit_systype,
                                    on_change=AssetsState.set_edit_systype,
                                    placeholder="Select system type",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Operating System", size="2", weight="medium"),
                                rx.select(
                                    AssetsState.operating_systems,
                                    value=AssetsState.edit_os,
                                    on_change=AssetsState.set_edit_os,
                                    placeholder="Select OS",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        
                        # Serial Number and Barcode
                        rx.hstack(
                            rx.vstack(
                                rx.text("Serial Number", size="2", weight="medium"),
                                rx.input(
                                    value=AssetsState.edit_serial_no,
                                    on_change=AssetsState.set_edit_serial_no,
                                    placeholder="Enter serial number",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Barcode", size="2", weight="medium"),
                                rx.input(
                                    value=AssetsState.edit_barcode,
                                    on_change=AssetsState.set_edit_barcode,
                                    placeholder="Enter barcode",
                                    size="3",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            width="100%",
                            spacing="3",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=AssetsState.save_asset_changes,
                    width="100%",
                ),
                
                rx.divider(),
                
                # Action buttons
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color="gray",
                            size="3",
                        ),
                    ),
                    rx.button(
                        "Save Changes",
                        type="submit",
                        variant="solid",
                        size="3",
                        on_click=AssetsState.save_asset_changes,
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                
                spacing="4",
                width="100%",
            ),
            style={
                "max_width": "600px",
                "padding": "24px",
            },
        ),
        open=AssetsState.edit_modal_open,
    )