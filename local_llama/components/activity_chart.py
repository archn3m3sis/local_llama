"""Activity chart components for dashboard."""
import reflex as rx
from .shared_styles import CARD_STYLE


def activity_timeline_chart(data: list[dict]) -> rx.Component:
    """Create a timeline chart showing activities over time."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="line_chart",
                    size=20,
                    style={
                        "color": "#06b6d4",
                        "filter": "drop-shadow(0 0 10px #06b6d4)"
                    }
                ),
                rx.text(
                    "Activity Timeline (Last 7 Days)",
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_size": "1.125rem",
                        "font_weight": "600",
                    }
                ),
                spacing="3",
                align="center",
            ),
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
                data=data,
                height=300,
                style={
                    "width": "100%",
                }
            ),
            spacing="4",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
        }
    )


def activity_donut_chart(data: list[dict]) -> rx.Component:
    """Create a donut chart showing activity distribution with neon labels."""
    
    # Create custom label component with neon effect
    def custom_label(entry, index):
        return rx.text(
            entry["name"] + ": " + str(entry["value"]),
            style={
                "fill": entry["fill"],
                "font_size": "0.875rem",
                "font_weight": "600",
                "filter": f"drop-shadow(0 0 8px {entry['fill']})",
                "text_shadow": f"0 0 10px {entry['fill']}",
            }
        )
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="pie_chart",
                    size=20,
                    style={
                        "color": "#a78bfa",
                        "filter": "drop-shadow(0 0 10px #a78bfa)"
                    }
                ),
                rx.text(
                    "Activity Distribution By Action Type",
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_size": "1.125rem",
                        "font_weight": "600",
                    }
                ),
                spacing="3",
                align="center",
            ),
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=data,
                    data_key="value",
                    name_key="name",
                    inner_radius="50%",
                    outer_radius="65%",
                    padding_angle=8,
                    label=True,
                    label_line=True,
                    min_angle=15,
                    cx="50%",
                    cy="50%",
                ),
                rx.recharts.graphing_tooltip(
                    style={
                        "background": "rgba(17, 24, 39, 0.9)",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "box_shadow": "0 4px 20px rgba(0, 0, 0, 0.5)",
                    }
                ),
                height=300,
                margin={"top": 20, "right": 80, "bottom": 20, "left": 80},
                style={
                    "width": "100%",
                    "& .recharts-pie-sector": {
                        "filter": "drop-shadow(0 0 8px rgba(0, 0, 0, 0.5))",
                        "transition": "filter 0.3s ease",
                        "cursor": "pointer",
                    },
                    "& .recharts-pie-sector:hover": {
                        "filter": "drop-shadow(0 0 15px rgba(255, 255, 255, 0.8)) brightness(1.15)",
                        "opacity": "0.95",
                    },
                    # VM Created - Green
                    "& .recharts-layer g:nth-child(1) .recharts-pie-label-line line": {
                        "stroke": "#10b981",
                        "stroke_width": "3px",
                        "filter": "drop-shadow(0 0 8px #10b981)",
                    },
                    # Images - Cyan
                    "& .recharts-layer g:nth-child(2) .recharts-pie-label-line line": {
                        "stroke": "#06b6d4",
                        "stroke_width": "3px",
                        "filter": "drop-shadow(0 0 8px #06b6d4)",
                    },
                    # Logs - Purple
                    "& .recharts-layer g:nth-child(3) .recharts-pie-label-line line": {
                        "stroke": "#a78bfa",
                        "stroke_width": "3px",
                        "filter": "drop-shadow(0 0 8px #a78bfa)",
                    },
                    # DAT Updates - Orange
                    "& .recharts-layer g:nth-child(4) .recharts-pie-label-line line": {
                        "stroke": "#f59e0b",
                        "stroke_width": "3px",
                        "filter": "drop-shadow(0 0 8px #f59e0b)",
                    },
                    "& .recharts-pie-label-text": {
                        "fill": "rgba(255, 255, 255, 0.95)",
                        "font_weight": "600",
                        "font_size": "0.875rem",
                        "filter": "drop-shadow(0 0 4px rgba(0, 0, 0, 0.8))",
                    },
                    "& .recharts-surface": {
                        "overflow": "visible",
                    }
                }
            ),
            # Legend with neon effect
            rx.hstack(
                rx.foreach(
                    data,
                    lambda item: rx.hstack(
                        rx.box(
                            style={
                                "width": "12px",
                                "height": "12px",
                                "background": item["fill"],
                                "border_radius": "2px",
                                "box_shadow": f"0 0 10px {item['fill']}",
                            }
                        ),
                        rx.text(
                            item["name"],
                            style={
                                "color": "rgba(255, 255, 255, 0.9)",
                                "font_size": "0.875rem",
                                "font_weight": "500",
                            }
                        ),
                        spacing="2",
                        align="center",
                    )
                ),
                spacing="4",
                wrap="wrap",
                justify="center",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        style={
            **CARD_STYLE,
            "padding": "1.5rem",
            "position": "relative",
            "overflow": "visible",
            "height": "fit-content",
            "display": "flex",
            "align_items": "stretch",
        }
    )