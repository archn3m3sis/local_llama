"""Top performers components for dashboard."""
import reflex as rx


def performer_bar(performer: dict) -> rx.Component:
    """Create a single performer bar."""
    name = performer["name"]
    count = performer["count"]
    rank = performer["rank"]
    percentage = performer["percentage"]
    rank_color = performer["rank_color"]
    
    return rx.hstack(
        rx.text(
            rank.to_string(),
            style={
                "color": rank_color,
                "font_weight": "700",
                "font_size": "1.25rem",
                "width": "30px",
                "text_align": "center",
                "filter": "drop-shadow(0 0 10px currentColor)",
            }
        ),
        rx.vstack(
            rx.hstack(
                rx.text(
                    name,
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_weight": "600",
                        "font_size": "0.875rem",
                    }
                ),
                rx.text(
                    count.to_string(),
                    style={
                        "color": "rgba(156, 163, 175, 0.9)",
                        "font_weight": "500",
                        "font_size": "0.875rem",
                    }
                ),
                width="100%",
                justify="between",
            ),
            rx.box(
                rx.box(
                    style={
                        "width": percentage.to(str) + "%",
                        "height": "100%",
                        "background": rank_color,
                        "border_radius": "4px",
                        "transition": "width 1s ease-out",
                        "box_shadow": "0 0 10px rgba(0, 0, 0, 0.4)",
                    }
                ),
                style={
                    "width": "100%",
                    "height": "8px",
                    "background": "rgba(55, 65, 81, 0.5)",
                    "border_radius": "4px",
                    "overflow": "hidden",
                }
            ),
            spacing="2",
            width="100%",
        ),
        spacing="3",
        width="100%",
        padding="0.75rem",
    )


def top_performers_panel(performers: list[dict], title: str = "Top Performers") -> rx.Component:
    """Create the top performers panel."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag="trophy",
                    size=20,
                    style={
                        "color": "#fbbf24",
                        "filter": "drop-shadow(0 0 10px #fbbf24)"
                    }
                ),
                rx.text(
                    title,
                    style={
                        "color": "rgba(255, 255, 255, 0.9)",
                        "font_size": "1.125rem",
                        "font_weight": "600",
                    }
                ),
                spacing="3",
                align="center",
            ),
            rx.vstack(
                rx.foreach(performers, performer_bar),
                spacing="2",
                width="100%",
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


def project_activity_panel(projects: list[dict]) -> rx.Component:
    """Create the project activity panel."""
    return top_performers_panel(projects, title="Most Active Projects")