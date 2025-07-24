"""Asset delete confirmation modal component."""
import reflex as rx
from ..states.assets_state import AssetsState


def asset_delete_modal() -> rx.Component:
    """Create the asset delete confirmation modal."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header with warning icon
                rx.center(
                    rx.hstack(
                        rx.icon(
                            tag="triangle_alert",
                            size=24,
                            style={
                                "color": "#ef4444",
                                "filter": "drop-shadow(0 0 8px #ef4444)",
                            }
                        ),
                        rx.text(
                            "DROP DB Record Confirmation",
                            style={
                                "font_size": "1.5rem",
                                "font_weight": "700",
                                "color": "#ef4444",
                                "text_shadow": "0 0 20px rgba(239, 68, 68, 0.5)",
                            }
                        ),
                        spacing="3",
                        align="center",
                    ),
                    width="100%",
                    style={
                        "margin_bottom": "1rem",
                    }
                ),
                
                # Warning message
                rx.box(
                    rx.vstack(
                        rx.text(
                            "You are about to request the removal of a record from the IAMS database.",
                            style={
                                "color": "rgba(255, 255, 255, 0.95)",
                                "font_weight": "600",
                                "font_size": "1rem",
                                "text_align": "center",
                            }
                        ),
                        rx.center(
                            rx.box(
                                rx.hstack(
                                    rx.icon(
                                        tag="server",
                                        size=20,
                                        style={"color": "#ef4444"}
                                    ),
                                    rx.text(
                                        f"Asset: {AssetsState.delete_asset_name}",
                                        style={
                                            "color": "rgba(255, 255, 255, 0.9)",
                                            "font_weight": "500",
                                            "font_size": "1.125rem",
                                        }
                                    ),
                                    spacing="2",
                                    align="center",
                                    justify="center",
                                ),
                                style={
                                    "padding": "1rem 2rem",
                                    "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%)",
                                    "border": "1px solid rgba(239, 68, 68, 0.3)",
                                    "border_radius": "8px",
                                    "display": "inline-block",
                                }
                            ),
                            width="100%",
                            style={
                                "margin": "1rem 0",
                            }
                        ),
                        rx.text(
                            "This action cannot be undone. To confirm deletion, please type exactly:",
                            style={
                                "color": "rgba(229, 231, 235, 0.9)",
                                "font_size": "0.875rem",
                                "text_align": "center",
                            }
                        ),
                        rx.center(
                            rx.code(
                                f"delete {AssetsState.delete_asset_name}",
                                style={
                                    "color": "#ef4444",
                                    "font_family": "monospace",
                                    "font_size": "1.125rem",
                                    "font_weight": "600",
                                    "padding": "0.75rem 1.5rem",
                                    "background": "rgba(239, 68, 68, 0.1)",
                                    "border": "2px dashed rgba(239, 68, 68, 0.4)",
                                    "border_radius": "8px",
                                    "display": "inline-block",
                                }
                            ),
                            width="100%",
                            style={
                                "margin": "1rem 0",
                            }
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    style={
                        "padding": "1.5rem",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "12px",
                        "backdrop_filter": "blur(16px) saturate(180%)",
                        "-webkit-backdrop-filter": "blur(16px) saturate(180%)",
                        "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.06)",
                    }
                ),
                
                # Confirmation input
                rx.input(
                    placeholder="Type the confirmation text here...",
                    value=AssetsState.delete_confirmation_text,
                    on_change=AssetsState.set_delete_confirmation_text,
                    style={
                        "width": "100%",
                        "height": "3rem",
                        "padding": "0.5rem 1.25rem",
                        "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)",
                        "border": "2px solid rgba(239, 68, 68, 0.3)",
                        "border_radius": "8px",
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1rem",
                        "line_height": "1.5",
                        "font_family": "monospace",
                        "transition": "all 0.2s ease",
                        "_focus": {
                            "border_color": "#ef4444",
                            "box_shadow": "0 0 0 3px rgba(239, 68, 68, 0.2)",
                            "outline": "none",
                            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%)",
                        },
                        "_placeholder": {
                            "color": "rgba(156, 163, 175, 0.6)",
                        }
                    }
                ),
                
                # Action buttons
                rx.hstack(
                    rx.button(
                        "Cancel",
                        on_click=AssetsState.close_delete_modal,
                        style={
                            "padding": "0.75rem 1.5rem",
                            "background": "linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(107, 114, 128, 0.1) 100%)",
                            "border": "1px solid rgba(107, 114, 128, 0.4)",
                            "border_radius": "8px",
                            "color": "rgba(229, 231, 235, 0.9)",
                            "font_weight": "500",
                            "cursor": "pointer",
                            "transition": "all 0.2s ease",
                            "_hover": {
                                "background": "linear-gradient(135deg, rgba(107, 114, 128, 0.3) 0%, rgba(107, 114, 128, 0.2) 100%)",
                                "border_color": "rgba(107, 114, 128, 0.6)",
                                "transform": "translateY(-1px)",
                            }
                        }
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.hstack(
                            rx.icon(
                                tag="trash_2",
                                size=16,
                                style={"color": "#fff"}
                            ),
                            rx.text(
                                "Submit Removal Request",
                                style={
                                    "color": "#fff",
                                    "font_weight": "600",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        on_click=AssetsState.submit_delete_request,
                        disabled=~AssetsState.delete_confirmation_valid,
                        style={
                            "padding": "0.75rem 1.5rem",
                            "background": rx.cond(
                                AssetsState.delete_confirmation_valid,
                                "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                                "linear-gradient(135deg, rgba(107, 114, 128, 0.3) 0%, rgba(107, 114, 128, 0.2) 100%)"
                            ),
                            "border": rx.cond(
                                AssetsState.delete_confirmation_valid,
                                "1px solid #ef4444",
                                "1px solid rgba(107, 114, 128, 0.3)"
                            ),
                            "border_radius": "8px",
                            "cursor": rx.cond(
                                AssetsState.delete_confirmation_valid,
                                "pointer",
                                "not-allowed"
                            ),
                            "opacity": rx.cond(
                                AssetsState.delete_confirmation_valid,
                                "1",
                                "0.5"
                            ),
                            "transition": "all 0.2s ease",
                            "_hover": rx.cond(
                                AssetsState.delete_confirmation_valid,
                                {
                                    "background": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)",
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.3)",
                                },
                                {}
                            ),
                        }
                    ),
                    width="100%",
                    spacing="4",
                ),
                
                spacing="6",
                width="100%",
            ),
            style={
                "max_width": "500px",
                "width": "90vw",
                "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.8) 0%, rgba(17, 17, 17, 0.9) 100%)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "16px",
                "padding": "2rem",
                "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.06)",
                "backdrop_filter": "blur(20px) saturate(180%)",
                "-webkit-backdrop-filter": "blur(20px) saturate(180%)",
                "position": "relative",
                "overflow": "hidden",
                "_before": {
                    "content": '""',
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "right": "0",
                    "bottom": "0",
                    "background": "linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, transparent 100%)",
                    "pointer_events": "none",
                    "z_index": "0",
                },
            }
        ),
        open=AssetsState.delete_modal_open,
        on_open_change=AssetsState.close_delete_modal,
    )