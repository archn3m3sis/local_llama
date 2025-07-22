import reflex as rx
try:
    import reflex_type_animation as ta
except ImportError:
    ta = None  # Handle gracefully for offline mode
from reflex.experimental import ClientStateVar
from ..components.metallic_text import metallic_title, metallic_text
from ..components.dashboard_stats import stats_grid
from ..components.activity_chart import activity_timeline_chart, activity_donut_chart
from ..components.recent_activity import recent_activity_panel
from ..components.top_performers import top_performers_panel, project_activity_panel
from ..components.performance_breakdown import performance_breakdown_panel
from ..components.asset_stats import asset_stats_panel
from ..states.dashboard_state import DashboardState

# Tab state
ActiveDashboardTab = ClientStateVar.create("dashboard_tab", 0)
DashboardTabs = [
    ["Industrial Summary", "home"],
    ["Performance Breakdown", "users"]
]

def dashboard_tabs() -> rx.Component:
    """Create the tab navigation component."""
    return rx.box(
        rx.hstack(
            rx.foreach(
                DashboardTabs,
                lambda tab, i: rx.button(
                    rx.icon(
                        tag=tab[1],
                        width="16px",
                        height="16px",
                        color=rx.cond(
                            ActiveDashboardTab.value == i,
                            "rgba(255, 255, 255, 0.95)",
                            "rgba(156, 163, 175, 0.8)",
                        ),
                    ),
                    rx.text(
                        tab[0],
                        color=rx.cond(
                            ActiveDashboardTab.value == i,
                            "rgba(255, 255, 255, 0.95)",
                            "rgba(156, 163, 175, 0.8)",
                        ),
                        font_size="0.875rem",
                        font_weight="600",
                    ),
                    on_click=[rx.call_function(ActiveDashboardTab.set_value(i))],
                    background=rx.cond(
                        ActiveDashboardTab.value == i,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.05) 100%)",
                        "transparent",
                    ),
                    style={
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "white_space": "nowrap",
                        "padding": "0.75rem 1.25rem",
                        "gap": "0.5rem",
                        "cursor": "pointer",
                        "border_radius": "0.5rem",
                        "transition": "all 0.3s ease",
                        "border": rx.cond(
                            ActiveDashboardTab.value == i,
                            "1px solid rgba(55, 65, 81, 0.5)",
                            "1px solid transparent",
                        ),
                        "box_shadow": rx.cond(
                            ActiveDashboardTab.value == i,
                            "0 4px 20px rgba(0, 0, 0, 0.3)",
                            "none",
                        ),
                        "_hover": {
                            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%)",
                            "transform": "translateY(-1px)",
                        },
                    },
                ),
            ),
            spacing="3",
            style={
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 50%, rgba(255, 255, 255, 0.03) 100%)",
                "backdrop_filter": "blur(16px) saturate(180%) brightness(0.9)",
                "-webkit-backdrop-filter": "blur(16px) saturate(180%) brightness(0.9)",
                "padding": "0.5rem",
                "border_radius": "0.75rem",
                "border": "1px solid rgba(255, 255, 255, 0.08)",
                "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.04)",
            },
        ),
        margin_bottom="2rem",
    )


def overview_tab() -> rx.Component:
    """Overview tab content with stats grid and recent activity."""
    # Calculate month-over-month comparisons
    total_comparison_percent = rx.cond(
        DashboardState.total_activities_last_month > 0,
        ((DashboardState.total_activities - DashboardState.total_activities_last_month) * 100.0 / DashboardState.total_activities_last_month),
        100.0
    )
    total_comparison_count = DashboardState.total_activities - DashboardState.total_activities_last_month
    
    today_comparison_percent = rx.cond(
        DashboardState.activities_today_last_month > 0,
        ((DashboardState.activities_today - DashboardState.activities_today_last_month) * 100.0 / DashboardState.activities_today_last_month),
        rx.cond(DashboardState.activities_today > 0, 100.0, 0.0)
    )
    today_comparison_count = DashboardState.activities_today - DashboardState.activities_today_last_month
    
    week_comparison_percent = rx.cond(
        DashboardState.activities_this_week_last_month > 0,
        ((DashboardState.activities_this_week - DashboardState.activities_this_week_last_month) * 100.0 / DashboardState.activities_this_week_last_month),
        rx.cond(DashboardState.activities_this_week > 0, 100.0, 0.0)
    )
    week_comparison_count = DashboardState.activities_this_week - DashboardState.activities_this_week_last_month
    
    month_comparison_percent = rx.cond(
        DashboardState.activities_this_month_last_month > 0,
        ((DashboardState.activities_this_month - DashboardState.activities_this_month_last_month) * 100.0 / DashboardState.activities_this_month_last_month),
        rx.cond(DashboardState.activities_this_month > 0, 100.0, 0.0)
    )
    month_comparison_count = DashboardState.activities_this_month - DashboardState.activities_this_month_last_month
    
    stats = [
        {
            "title": "Total Completed Actions",
            "value": DashboardState.total_activities,
            "icon": "activity",
            "color": "#06b6d4",
            "comparison_percent": total_comparison_percent,
            "comparison_count": total_comparison_count
        },
        {
            "title": "TODAY'S ACTIVITY",
            "value": DashboardState.activities_today,
            "icon": "calendar",
            "color": "#10b981",
            "comparison_percent": today_comparison_percent,
            "comparison_count": today_comparison_count
        },
        {
            "title": "WEEK TO DATE ACTIVITY",
            "value": DashboardState.activities_this_week,
            "icon": "calendar_days",
            "color": "#a78bfa",
            "comparison_percent": week_comparison_percent,
            "comparison_count": week_comparison_count
        },
        {
            "title": "MONTH TO DATE ACTIVITY",
            "value": DashboardState.activities_this_month,
            "icon": "calendar_range",
            "color": "#f59e0b",
            "comparison_percent": month_comparison_percent,
            "comparison_count": month_comparison_count
        }
    ]
    return rx.vstack(
        stats_grid(stats),
        rx.hstack(
            rx.box(
                recent_activity_panel(DashboardState.recent_activities),
                style={"flex": "1", "display": "flex", "flex_direction": "column"}
            ),
            rx.box(
                activity_donut_chart(DashboardState.activity_donut_data),
                style={"flex": "1", "display": "flex", "flex_direction": "column"}
            ),
            spacing="4",
            width="100%",
            align="stretch",
            style={"min_height": "450px"}
        ),
        spacing="6",
        width="100%",
    )




def performance_breakdown_tab() -> rx.Component:
    """Performance breakdown tab content."""
    return performance_breakdown_panel(
        DashboardState.employee_performance_breakdown,
        DashboardState.activity_timeline
    )




def Dashboard() -> rx.Component:
    
    return rx.fragment(
        # Asset stats panel (positioned absolutely)
        asset_stats_panel(
            DashboardState.total_assets,
            DashboardState.total_projects,
            DashboardState.total_operating_systems
        ),
        
        # Main content
        rx.vstack(
            # Massive 3D chrome metallic title
            metallic_title("Industrial Cyber Dashboard"),
            
            # Tab navigation
            dashboard_tabs(),
        
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
            # Tab content with bottom spacing
            rx.vstack(
                rx.box(
                    rx.cond(
                        ActiveDashboardTab.value == 0,
                        overview_tab(),
                        performance_breakdown_tab()
                    ),
                    width="100%",
                    min_height="500px",
                ),
                # Invisible spacer to push content up
                rx.box(
                    height="10rem",
                    width="100%",
                    background="transparent",
                ),
                spacing="0",
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
        right="0",
        min_height="100vh",
        z_index="10",
        on_mount=DashboardState.load_dashboard_data,
        )
    )
