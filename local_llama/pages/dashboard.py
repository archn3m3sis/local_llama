import reflex as rx
import reflex_type_animation as ta
from ..components.metallic_text import metallic_title, metallic_text
from ..components.dashboard_stats import stats_grid
from ..components.activity_chart import activity_timeline_chart, activity_donut_chart
from ..components.recent_activity import recent_activity_panel
from ..components.top_performers import top_performers_panel, project_activity_panel
from ..states.dashboard_state import DashboardState

def Dashboard() -> rx.Component:
    stats = [
        {
            "title": "Total Activities",
            "value": DashboardState.total_activities,
            "icon": "activity",
            "color": "#06b6d4"
        },
        {
            "title": "Today",
            "value": DashboardState.activities_today,
            "icon": "calendar",
            "color": "#10b981"
        },
        {
            "title": "This Week",
            "value": DashboardState.activities_this_week,
            "icon": "calendar_days",
            "color": "#a78bfa"
        },
        {
            "title": "This Month",
            "value": DashboardState.activities_this_month,
            "icon": "calendar_month",
            "color": "#f59e0b"
        }
    ]
    
    return rx.vstack(
        # Massive 3D chrome metallic title
        metallic_title("Industrial Cyber Dashboard"),
        
        # Loading spinner
        rx.cond(
            DashboardState.is_loading,
            rx.center(
                rx.spinner(
                    size="3",
                    style={"color": "#06b6d4"}
                ),
                style={"height": "400px"}
            ),
            rx.vstack(
                # Stats grid
                stats_grid(stats),
                
                # Charts row
                rx.hstack(
                    # Activity timeline
                    rx.box(
                        activity_timeline_chart(DashboardState.activity_timeline),
                        style={"flex": "2"}
                    ),
                    # Donut chart
                    rx.box(
                        activity_donut_chart(
                            vm=DashboardState.vm_creations,
                            image=DashboardState.image_captures,
                            log=DashboardState.log_collections,
                            dat=DashboardState.dat_updates
                        ),
                        style={"flex": "1"}
                    ),
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                
                # Bottom row
                rx.hstack(
                    # Recent activity
                    rx.box(
                        recent_activity_panel(DashboardState.recent_activities),
                        style={"flex": "2"}
                    ),
                    # Top performers and projects
                    rx.vstack(
                        top_performers_panel(DashboardState.top_employees),
                        project_activity_panel(DashboardState.project_activities),
                        spacing="4",
                        style={"flex": "1"}
                    ),
                    spacing="4",
                    width="100%",
                    align="start",
                ),
                
                spacing="6",
                width="100%",
            )
        ),
        
        spacing="6",
        align="start",
        width="100%",
        padding="3em",
        padding_top="4em",
        position="absolute",
        top="0",
        left="0",
        z_index="10",
        on_mount=DashboardState.load_dashboard_data,
    )
