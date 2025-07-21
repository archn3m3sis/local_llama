"""Activity chart components for dashboard."""
import reflex as rx


def activity_timeline_chart(data: list[dict]) -> rx.Component:
    """Create a timeline chart showing activities over time."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="chart",
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
            "background": "rgba(17, 24, 39, 0.6)",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(55, 65, 81, 0.5)",
            "border_radius": "12px",
            "padding": "1.5rem",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
        }
    )


def activity_donut_chart(vm: int, image: int, log: int, dat: int) -> rx.Component:
    """Create a donut chart showing activity distribution."""
    data = [
        {"name": "VM Created", "value": vm, "fill": "#10b981"},
        {"name": "Images", "value": image, "fill": "#06b6d4"},
        {"name": "Logs", "value": log, "fill": "#a78bfa"},
        {"name": "DAT Updates", "value": dat, "fill": "#f59e0b"},
    ]
    
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
                    "Activity Distribution",
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
                    inner_radius="60%",
                    outer_radius="80%",
                    padding_angle=5,
                ),
                rx.recharts.graphing_tooltip(),
                height=300,
                style={
                    "width": "100%",
                }
            ),
            spacing="4",
            width="100%",
        ),
        style={
            "background": "rgba(17, 24, 39, 0.6)",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(55, 65, 81, 0.5)",
            "border_radius": "12px",
            "padding": "1.5rem",
            "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
        }
    )