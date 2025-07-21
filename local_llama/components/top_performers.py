"""Top performers components for dashboard."""
import reflex as rx


def performer_bar(name: str, count: int, max_count: int, rank: int) -> rx.Component:
    """Create a single performer bar."""
    percentage = (count / max_count * 100) if max_count > 0 else 0
    
    # Rank colors
    rank_colors = {
        1: "#fbbf24",  # Gold
        2: "#9ca3af",  # Silver
        3: "#f97316",  # Bronze
    }
    rank_color = rank_colors.get(rank, "#06b6d4")
    
    return rx.hstack(
        rx.text(
            str(rank),
            style={
                "color": rank_color,
                "font_weight": "700",
                "font_size": "1.25rem",
                "width": "30px",
                "text_align": "center",
                "filter": f"drop-shadow(0 0 10px {rank_color})" if rank <= 3 else "none",
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
                    str(count),
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
                        "width": f"{percentage}%",
                        "height": "100%",
                        "background": f"linear-gradient(90deg, {rank_color} 0%, {rank_color}80 100%)",
                        "border_radius": "4px",
                        "transition": "width 1s ease-out",
                        "box_shadow": f"0 0 10px {rank_color}40",
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


def top_performers_panel(employees: list[dict], title: str = "Top Performers") -> rx.Component:
    """Create the top performers panel."""
    max_count = max([emp["count"] for emp in employees]) if employees else 1
    
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
                *[
                    performer_bar(
                        name=emp["name"],
                        count=emp["count"],
                        max_count=max_count,
                        rank=idx + 1
                    )
                    for idx, emp in enumerate(employees)
                ],
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