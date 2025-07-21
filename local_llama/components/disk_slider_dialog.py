"""Disk Slider Dialog Component."""
import reflex as rx
from ..states.vm_creation_state import VMCreationState

def disk_slider_dialog() -> rx.Component:
    """Modern slider dialog for Disk MB selection."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Dialog Header
                rx.hstack(
                    rx.hstack(
                        rx.icon(
                            tag="hard_drive",
                            size=24,
                            color="rgba(167, 139, 250, 0.9)",
                            style={
                                "filter": "drop-shadow(0 0 8px rgba(167, 139, 250, 0.4))",
                            }
                        ),
                        rx.heading(
                            "Select Disk Size",
                            size="5",
                            weight="bold",
                            color="white",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.icon(
                        tag="x",
                        size=24,
                        cursor="pointer",
                        on_click=VMCreationState.close_disk_dialog,
                        color="rgba(255, 255, 255, 0.7)",
                        _hover={"color": "white"},
                    ),
                    width="100%",
                    align="center",
                    margin_bottom="1.5rem",
                ),
                
                # Current Value Display
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Disk Size",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                        ),
                        rx.hstack(
                            rx.text(
                                VMCreationState.temp_disk_mb,
                                font_size="3rem",
                                font_weight="bold",
                                background="linear-gradient(135deg, #a78bfa 0%, #06b6d4 100%)",
                                background_clip="text",
                                color="transparent",
                            ),
                            rx.text(
                                "MB",
                                font_size="1.5rem",
                                color="rgba(255, 255, 255, 0.8)",
                                margin_left="-0.5rem",
                            ),
                            align="baseline",
                            spacing="2",
                        ),
                        spacing="1",
                        align="center",
                    ),
                    width="100%",
                    padding="1.5rem",
                    background="linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="12px",
                    margin_bottom="2rem",
                    backdrop_filter="blur(10px)",
                ),
                
                # Slider
                rx.vstack(
                    rx.text(
                        "Drag to adjust or type a value",
                        font_size="0.85rem",
                        color="rgba(255, 255, 255, 0.6)",
                        margin_bottom="0.5rem",
                    ),
                    rx.slider(
                        default_value=[262144],
                        min=10240,  # 10 GB minimum
                        max=2097152,  # 2 TB max
                        step=1024,
                        value=VMCreationState.slider_disk_value,
                        on_change=VMCreationState.set_temp_disk_mb_from_slider,
                        width="100%",
                        size="3",
                        style={
                            "& .rt-SliderTrack": {
                                "background": "rgba(255, 255, 255, 0.05)",
                                "height": "10px",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                            },
                            "& .rt-SliderRange": {
                                "background": "linear-gradient(90deg, #a78bfa 0%, #06b6d4 100%)",
                                "box_shadow": "0 0 20px rgba(167, 139, 250, 0.3)",
                            },
                            "& .rt-SliderThumb": {
                                "width": "24px",
                                "height": "24px",
                                "background": "linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)",
                                "border": "2px solid #a78bfa",
                                "box_shadow": "0 0 15px rgba(167, 139, 250, 0.5), inset 0 0 5px rgba(6, 182, 212, 0.3)",
                                "&:hover": {
                                    "box_shadow": "0 0 20px rgba(167, 139, 250, 0.7), inset 0 0 8px rgba(6, 182, 212, 0.5)",
                                    "border_color": "#06b6d4",
                                },
                            },
                        },
                    ),
                    width="100%",
                    spacing="3",
                ),
                
                # Quick Select Buttons
                rx.vstack(
                    rx.text(
                        "Quick Select",
                        font_size="0.9rem",
                        color="rgba(255, 255, 255, 0.7)",
                        margin_bottom="0.5rem",
                    ),
                    rx.hstack(
                        rx.button(
                            "100 GB",
                            on_click=lambda: VMCreationState.set_temp_disk_mb("102400"),
                            size="2",
                            variant="soft",
                            style={
                                "background": rx.cond(
                                    VMCreationState.temp_disk_mb == "102400",
                                    "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                                    "rgba(255, 255, 255, 0.03)"
                                ),
                                "border": rx.cond(
                                    VMCreationState.temp_disk_mb == "102400",
                                    "1px solid rgba(167, 139, 250, 0.3)",
                                    "1px solid rgba(255, 255, 255, 0.08)"
                                ),
                                "color": "rgba(255, 255, 255, 0.9)",
                                "_hover": {
                                    "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%)",
                                    "border": "1px solid rgba(167, 139, 250, 0.4)",
                                    "box_shadow": "0 0 10px rgba(167, 139, 250, 0.2)",
                                },
                            },
                        ),
                        rx.button(
                            "250 GB",
                            on_click=lambda: VMCreationState.set_temp_disk_mb("256000"),
                            size="2",
                            variant="soft",
                            style={
                                "background": rx.cond(
                                    VMCreationState.temp_disk_mb == "256000",
                                    "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                                    "rgba(255, 255, 255, 0.03)"
                                ),
                                "border": rx.cond(
                                    VMCreationState.temp_disk_mb == "256000",
                                    "1px solid rgba(167, 139, 250, 0.3)",
                                    "1px solid rgba(255, 255, 255, 0.08)"
                                ),
                                "color": "rgba(255, 255, 255, 0.9)",
                                "_hover": {
                                    "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%)",
                                    "border": "1px solid rgba(167, 139, 250, 0.4)",
                                    "box_shadow": "0 0 10px rgba(167, 139, 250, 0.2)",
                                },
                            },
                        ),
                        rx.button(
                            "500 GB",
                            on_click=lambda: VMCreationState.set_temp_disk_mb("512000"),
                            size="2",
                            variant="soft",
                            style={
                                "background": rx.cond(
                                    VMCreationState.temp_disk_mb == "512000",
                                    "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                                    "rgba(255, 255, 255, 0.03)"
                                ),
                                "border": rx.cond(
                                    VMCreationState.temp_disk_mb == "512000",
                                    "1px solid rgba(167, 139, 250, 0.3)",
                                    "1px solid rgba(255, 255, 255, 0.08)"
                                ),
                                "color": "rgba(255, 255, 255, 0.9)",
                                "_hover": {
                                    "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%)",
                                    "border": "1px solid rgba(167, 139, 250, 0.4)",
                                    "box_shadow": "0 0 10px rgba(167, 139, 250, 0.2)",
                                },
                            },
                        ),
                        rx.button(
                            "1 TB",
                            on_click=lambda: VMCreationState.set_temp_disk_mb("1048576"),
                            size="2",
                            variant="soft",
                            style={
                                "background": rx.cond(
                                    VMCreationState.temp_disk_mb == "1048576",
                                    "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                                    "rgba(255, 255, 255, 0.03)"
                                ),
                                "border": rx.cond(
                                    VMCreationState.temp_disk_mb == "1048576",
                                    "1px solid rgba(167, 139, 250, 0.3)",
                                    "1px solid rgba(255, 255, 255, 0.08)"
                                ),
                                "color": "rgba(255, 255, 255, 0.9)",
                                "_hover": {
                                    "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%)",
                                    "border": "1px solid rgba(167, 139, 250, 0.4)",
                                    "box_shadow": "0 0 10px rgba(167, 139, 250, 0.2)",
                                },
                            },
                        ),
                        rx.button(
                            "2 TB",
                            on_click=lambda: VMCreationState.set_temp_disk_mb("2097152"),
                            size="2",
                            variant="soft",
                            style={
                                "background": rx.cond(
                                    VMCreationState.temp_disk_mb == "2097152",
                                    "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                                    "rgba(255, 255, 255, 0.03)"
                                ),
                                "border": rx.cond(
                                    VMCreationState.temp_disk_mb == "2097152",
                                    "1px solid rgba(167, 139, 250, 0.3)",
                                    "1px solid rgba(255, 255, 255, 0.08)"
                                ),
                                "color": "rgba(255, 255, 255, 0.9)",
                                "_hover": {
                                    "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%)",
                                    "border": "1px solid rgba(167, 139, 250, 0.4)",
                                    "box_shadow": "0 0 10px rgba(167, 139, 250, 0.2)",
                                },
                            },
                        ),
                        spacing="2",
                        wrap="wrap",
                        width="100%",
                    ),
                    width="100%",
                    margin_top="2rem",
                    spacing="3",
                ),
                
                # Manual Input
                rx.vstack(
                    rx.text(
                        "Or enter manually",
                        font_size="0.9rem",
                        color="rgba(255, 255, 255, 0.7)",
                        margin_bottom="0.5rem",
                    ),
                    rx.input(
                        placeholder="Enter Disk in MB",
                        value=VMCreationState.temp_disk_mb,
                        on_change=VMCreationState.set_temp_disk_mb,
                        type="number",
                        min="10240",
                        max="2097152",
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.03)",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "color": "white",
                            "_focus": {
                                "border": "1px solid rgba(167, 139, 250, 0.5)",
                                "box_shadow": "0 0 0 3px rgba(167, 139, 250, 0.1)",
                                "background": "rgba(255, 255, 255, 0.05)",
                            },
                            "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                        },
                    ),
                    width="100%",
                    margin_top="1.5rem",
                    spacing="3",
                ),
                
                # Action Buttons
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=VMCreationState.cancel_disk_dialog,
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
                            rx.icon(tag="check", size=18),
                            rx.text("Apply"),
                            spacing="2",
                        ),
                        on_click=VMCreationState.apply_disk_dialog,
                        size="3",
                        style={
                            "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%)",
                            "border": "1px solid rgba(167, 139, 250, 0.25)",
                            "color": "white",
                            "font_weight": "600",
                            "border_radius": "8px",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(167, 139, 250, 0.25) 0%, rgba(6, 182, 212, 0.2) 100%)",
                                "border": "1px solid rgba(167, 139, 250, 0.4)",
                                "box_shadow": "0 4px 20px rgba(167, 139, 250, 0.3)",
                                "transform": "translateY(-1px)",
                            },
                        }
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                    margin_top="2rem",
                ),
                
                width="100%",
                spacing="4",
            ),
            style={
                "background": "linear-gradient(135deg, rgba(10, 10, 10, 0.95) 0%, rgba(20, 20, 20, 0.9) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.08)",
                "border_radius": "16px",
                "padding": "2rem",
                "box_shadow": "0 20px 50px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.05)",
                "backdrop_filter": "blur(20px)",
                "max_width": "500px",
                "width": "90%",
            }
        ),
        open=VMCreationState.show_disk_dialog,
    )