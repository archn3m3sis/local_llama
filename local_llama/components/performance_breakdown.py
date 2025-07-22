"""Performance breakdown component showing employee action type distribution."""
import reflex as rx
from .shared_styles import CARD_STYLE


def employee_performance_card(employee_data: dict) -> rx.Component:
    """Create a card showing an employee's action type breakdown."""
    return rx.box(
        rx.vstack(
            # Employee name and total actions
            rx.hstack(
                rx.text(
                    employee_data["name"],
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1.125rem",
                        "font_weight": "600",
                    }
                ),
                rx.text(
                    employee_data["total_actions"].to_string() + " total actions",
                    style={
                        "color": "rgba(156, 163, 175, 0.9)",
                        "font_size": "0.875rem",
                    }
                ),
                width="100%",
                justify="between",
                align="center",
            ),
            
            # Stacked percentage bar
            rx.box(
                rx.hstack(
                    # VM Created
                    rx.tooltip(
                        rx.box(
                            style={
                                "width": employee_data["vm_percentage"].to(str) + "%",
                                "height": "100%",
                                "background": "#10b981",
                                "transition": "all 0.3s ease",
                            }
                        ),
                        content="VM Created",
                    ),
                    # Images
                    rx.tooltip(
                        rx.box(
                            style={
                                "width": employee_data["image_percentage"].to(str) + "%",
                                "height": "100%",
                                "background": "#06b6d4",
                                "transition": "all 0.3s ease",
                            }
                        ),
                        content="Images",
                    ),
                    # Logs
                    rx.tooltip(
                        rx.box(
                            style={
                                "width": employee_data["log_percentage"].to(str) + "%",
                                "height": "100%",
                                "background": "#a78bfa",
                                "transition": "all 0.3s ease",
                            }
                        ),
                        content="Logs",
                    ),
                    # DAT Updates
                    rx.tooltip(
                        rx.box(
                            style={
                                "width": employee_data["dat_percentage"].to(str) + "%",
                                "height": "100%",
                                "background": "#f59e0b",
                                "transition": "all 0.3s ease",
                            }
                        ),
                        content="DAT Updates",
                    ),
                    spacing="0",
                    width="100%",
                    height="100%",
                ),
                style={
                    "width": "100%",
                    "height": "12px",
                    "background": "rgba(55, 65, 81, 0.5)",
                    "border_radius": "6px",
                    "overflow": "hidden",
                }
            ),
            
            # Action type legend
            rx.hstack(
                # VM Created
                rx.hstack(
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "background": "#10b981",
                            "border_radius": "2px",
                        }
                    ),
                    rx.text(
                        "VM: " + employee_data["vm_percentage"].to(str) + "%",
                        style={
                            "color": "rgba(156, 163, 175, 0.9)",
                            "font_size": "0.75rem",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                # Images
                rx.hstack(
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "background": "#06b6d4",
                            "border_radius": "2px",
                        }
                    ),
                    rx.text(
                        "Images: " + employee_data["image_percentage"].to(str) + "%",
                        style={
                            "color": "rgba(156, 163, 175, 0.9)",
                            "font_size": "0.75rem",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                # Logs
                rx.hstack(
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "background": "#a78bfa",
                            "border_radius": "2px",
                        }
                    ),
                    rx.text(
                        "Logs: " + employee_data["log_percentage"].to(str) + "%",
                        style={
                            "color": "rgba(156, 163, 175, 0.9)",
                            "font_size": "0.75rem",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                # DAT Updates
                rx.hstack(
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "background": "#f59e0b",
                            "border_radius": "2px",
                        }
                    ),
                    rx.text(
                        "DAT: " + employee_data["dat_percentage"].to(str) + "%",
                        style={
                            "color": "rgba(156, 163, 175, 0.9)",
                            "font_size": "0.75rem",
                        }
                    ),
                    spacing="2",
                    align="center",
                ),
                spacing="3",
                width="100%",
                wrap="wrap",
            ),
            
            spacing="4",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "_hover": {
                **CARD_STYLE["_hover"],
                "border_color": "rgba(96, 165, 250, 0.3)",
            }
        }
    )


def performance_breakdown_panel(employees: list[dict], timeline_data: list[dict]) -> rx.Component:
    """Create the performance breakdown panel showing all employees."""
    return rx.vstack(
        # Employee Performance Breakdown Section
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="users",
                    size=24,
                    style={
                        "color": "#06b6d4",
                        "filter": "drop-shadow(0 0 10px #06b6d4)"
                    }
                ),
                rx.text(
                    "Employee Performance Breakdown",
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1.5rem",
                        "font_weight": "700",
                    }
                ),
                spacing="3",
                align="center",
            ),
            rx.grid(
                rx.foreach(
                    employees,
                    employee_performance_card
                ),
                columns=rx.breakpoints({
                    "initial": "1",
                    "md": "2",
                    "xl": "3"
                }),
                spacing="4",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        
        # Weekly Performance Timeline Section
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="trending_up",
                    size=24,
                    style={
                        "color": "#10b981",
                        "filter": "drop-shadow(0 0 10px #10b981)"
                    }
                ),
                rx.text(
                    "Weekly Performance Timeline",
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1.5rem",
                        "font_weight": "700",
                    }
                ),
                spacing="3",
                align="center",
            ),
            rx.box(
                rx.recharts.line_chart(
                    rx.recharts.line(
                        data_key="vm",
                        stroke="#10b981",
                        stroke_width=2,
                    ),
                    rx.recharts.line(
                        data_key="image",
                        stroke="#06b6d4",
                        stroke_width=2,
                    ),
                    rx.recharts.line(
                        data_key="log",
                        stroke="#a78bfa",
                        stroke_width=2,
                    ),
                    rx.recharts.line(
                        data_key="dat",
                        stroke="#f59e0b",
                        stroke_width=2,
                    ),
                    rx.recharts.x_axis(data_key="date"),
                    rx.recharts.y_axis(),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", opacity=0.3),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.legend(),
                    data=timeline_data,
                    height=350,
                    style={
                        "width": "100%",
                    }
                ),
                style={
                    **CARD_STYLE,
                    "padding": "1.5rem",
                    "width": "100%",
                }
            ),
            spacing="4",
            width="100%",
        ),
        
        spacing="6",
        width="100%",
    )