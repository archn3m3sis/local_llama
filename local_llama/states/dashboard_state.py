"""State management for Dashboard page."""
import reflex as rx
from sqlmodel import select, func, and_
from datetime import datetime, timedelta
from collections import defaultdict
from ..models.user_activity import UserActivity
from ..models.employee import Employee
from ..models.asset import Asset
from ..models.project import Project
from ..models.virtual_machine import VirtualMachine
from ..models.image_collection import ImageCollection
from ..models.log_collection import LogCollection
from ..models.dat_update import DatUpdate
from ..models.operating_system import OperatingSystem


class DashboardState(rx.State):
    """State for Dashboard analytics and visualizations."""
    
    # Activity summary data
    total_activities: int = 0
    activities_today: int = 0
    activities_this_week: int = 0
    activities_this_month: int = 0
    
    # Asset statistics
    total_assets: int = 0
    total_projects: int = 0
    total_operating_systems: int = 0
    
    # Month-over-month comparisons
    total_activities_last_month: int = 0
    activities_today_last_month: int = 0
    activities_this_week_last_month: int = 0
    activities_this_month_last_month: int = 0
    
    # Activity by type
    vm_creations: int = 0
    image_captures: int = 0
    log_collections: int = 0
    dat_updates: int = 0
    
    # Donut chart data
    activity_donut_data: list[dict] = []
    
    # Activity by employee
    top_employees: list[dict] = []
    
    # Activity by project
    project_activities: list[dict] = []
    
    # Employee performance breakdown
    employee_performance_breakdown: list[dict] = []
    
    # Recent activities
    recent_activities: list[dict] = []
    
    # Time series data for charts
    activity_timeline: list[dict] = []
    
    # Loading state
    is_loading: bool = False
    
    async def load_dashboard_data(self):
        """Load all dashboard data."""
        self.is_loading = True
        yield
        
        try:
            with rx.session() as session:
                now = datetime.now()
                today = now.replace(hour=0, minute=0, second=0, microsecond=0)
                week_ago = today - timedelta(days=7)
                month_ago = today - timedelta(days=30)
                
                # Get total activities
                self.total_activities = session.exec(
                    select(func.count(UserActivity.activity_id))
                ).one()
                
                # Get activities today
                self.activities_today = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_timestamp >= today)
                ).one()
                
                # Get activities this week
                self.activities_this_week = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_timestamp >= week_ago)
                ).one()
                
                # Get activities this month
                self.activities_this_month = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_timestamp >= month_ago)
                ).one()
                
                # Calculate last month's data for comparisons
                last_month_start = month_ago - timedelta(days=30)
                last_month_end = month_ago
                
                # Total activities as of last month
                self.total_activities_last_month = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_timestamp < month_ago)
                ).one()
                
                # Activities on same day last month
                last_month_today = today - timedelta(days=30)
                last_month_tomorrow = last_month_today + timedelta(days=1)
                self.activities_today_last_month = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(and_(
                        UserActivity.activity_timestamp >= last_month_today,
                        UserActivity.activity_timestamp < last_month_tomorrow
                    ))
                ).one()
                
                # Activities in same week last month
                last_month_week_start = week_ago - timedelta(days=30)
                last_month_week_end = today - timedelta(days=30)
                self.activities_this_week_last_month = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(and_(
                        UserActivity.activity_timestamp >= last_month_week_start,
                        UserActivity.activity_timestamp < last_month_week_end
                    ))
                ).one()
                
                # Activities in the previous month period
                self.activities_this_month_last_month = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(and_(
                        UserActivity.activity_timestamp >= last_month_start,
                        UserActivity.activity_timestamp < last_month_end
                    ))
                ).one()
                
                # Count by activity type
                self.vm_creations = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_type == "vm_created")
                ).one()
                
                self.image_captures = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_type == "image_captured")
                ).one()
                
                self.log_collections = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_type == "log_added")
                ).one()
                
                self.dat_updates = session.exec(
                    select(func.count(UserActivity.activity_id))
                    .where(UserActivity.activity_type == "dat_updated")
                ).one()
                
                # Create donut chart data
                self.activity_donut_data = [
                    {"name": "VM Created", "value": self.vm_creations, "fill": "#10b981"},
                    {"name": "Images", "value": self.image_captures, "fill": "#06b6d4"},
                    {"name": "Logs", "value": self.log_collections, "fill": "#a78bfa"},
                    {"name": "DAT Updates", "value": self.dat_updates, "fill": "#f59e0b"},
                ]
                
                # Get top 5 employees by activity count
                employee_activities = session.exec(
                    select(
                        UserActivity.employee_id,
                        func.count(UserActivity.activity_id).label("activity_count")
                    )
                    .where(UserActivity.employee_id.isnot(None))
                    .group_by(UserActivity.employee_id)
                    .order_by(func.count(UserActivity.activity_id).desc())
                    .limit(5)
                ).all()
                
                # Process employee data
                self.top_employees = []
                max_emp_count = max([count for _, count in employee_activities]) if employee_activities else 1
                
                # Rank colors
                rank_colors = ["#fbbf24", "#9ca3af", "#f97316", "#06b6d4", "#06b6d4"]
                
                for idx, (emp_id, count) in enumerate(employee_activities):
                    employee = session.exec(
                        select(Employee).where(Employee.id == emp_id)
                    ).first()
                    if employee:
                        self.top_employees.append({
                            "name": f"{employee.first_name} {employee.last_name}",
                            "count": count,
                            "rank": idx + 1,
                            "percentage": (count / max_emp_count * 100) if max_emp_count > 0 else 0,
                            "rank_color": rank_colors[idx] if idx < len(rank_colors) else "#06b6d4"
                        })
                
                # Get activities by project
                project_activities = session.exec(
                    select(
                        UserActivity.related_project_id,
                        func.count(UserActivity.activity_id).label("activity_count")
                    )
                    .where(UserActivity.related_project_id.isnot(None))
                    .group_by(UserActivity.related_project_id)
                    .order_by(func.count(UserActivity.activity_id).desc())
                    .limit(5)
                ).all()
                
                # Process project data
                self.project_activities = []
                max_proj_count = max([count for _, count in project_activities]) if project_activities else 1
                
                for idx, (proj_id, count) in enumerate(project_activities):
                    project = session.exec(
                        select(Project).where(Project.project_id == proj_id)
                    ).first()
                    if project:
                        self.project_activities.append({
                            "name": project.project_name,
                            "count": count,
                            "rank": idx + 1,
                            "percentage": (count / max_proj_count * 100) if max_proj_count > 0 else 0,
                            "rank_color": rank_colors[idx] if idx < len(rank_colors) else "#06b6d4"
                        })
                
                # Calculate employee performance breakdown
                self.employee_performance_breakdown = []
                
                # Get all employees with any activity
                employee_ids_with_activity = session.exec(
                    select(UserActivity.employee_id).distinct()
                    .where(UserActivity.employee_id.isnot(None))
                ).all()
                
                for emp_id in employee_ids_with_activity:
                    employee = session.exec(
                        select(Employee).where(Employee.id == emp_id)
                    ).first()
                    
                    if employee:
                        # Get total actions for this employee
                        total_actions = session.exec(
                            select(func.count(UserActivity.activity_id))
                            .where(UserActivity.employee_id == emp_id)
                        ).one()
                        
                        if total_actions > 0:
                            # Count each activity type
                            vm_count = session.exec(
                                select(func.count(UserActivity.activity_id))
                                .where(and_(
                                    UserActivity.employee_id == emp_id,
                                    UserActivity.activity_type == "vm_created"
                                ))
                            ).one()
                            
                            image_count = session.exec(
                                select(func.count(UserActivity.activity_id))
                                .where(and_(
                                    UserActivity.employee_id == emp_id,
                                    UserActivity.activity_type == "image_captured"
                                ))
                            ).one()
                            
                            log_count = session.exec(
                                select(func.count(UserActivity.activity_id))
                                .where(and_(
                                    UserActivity.employee_id == emp_id,
                                    UserActivity.activity_type == "log_added"
                                ))
                            ).one()
                            
                            dat_count = session.exec(
                                select(func.count(UserActivity.activity_id))
                                .where(and_(
                                    UserActivity.employee_id == emp_id,
                                    UserActivity.activity_type == "dat_updated"
                                ))
                            ).one()
                            
                            # Calculate percentages
                            self.employee_performance_breakdown.append({
                                "name": f"{employee.first_name} {employee.last_name}",
                                "total_actions": total_actions,
                                "vm_percentage": round((vm_count / total_actions) * 100, 1),
                                "image_percentage": round((image_count / total_actions) * 100, 1),
                                "log_percentage": round((log_count / total_actions) * 100, 1),
                                "dat_percentage": round((dat_count / total_actions) * 100, 1),
                            })
                
                # Sort by total actions descending
                self.employee_performance_breakdown.sort(key=lambda x: x["total_actions"], reverse=True)
                
                # Get asset statistics
                self.total_assets = session.exec(
                    select(func.count(Asset.asset_id))
                ).one()
                
                self.total_projects = session.exec(
                    select(func.count(Project.project_id))
                ).one()
                
                # Get unique operating systems that are actually used by assets
                # This will be used for the "System Types" count on the dashboard
                self.total_operating_systems = session.exec(
                    select(func.count(func.distinct(Asset.os_id)))
                    .where(Asset.os_id.isnot(None))
                ).one()
                
                # Get recent activities (last 10)
                recent = session.exec(
                    select(UserActivity)
                    .order_by(UserActivity.activity_timestamp.desc())
                    .limit(10)
                ).all()
                
                self.recent_activities = []
                for activity in recent:
                    # Get employee name
                    employee_name = "Unknown"
                    if activity.employee_id:
                        employee = session.exec(
                            select(Employee).where(Employee.id == activity.employee_id)
                        ).first()
                        if employee:
                            employee_name = f"{employee.first_name} {employee.last_name}"
                    
                    self.recent_activities.append({
                        "timestamp": activity.activity_timestamp.strftime("%Y-%m-%d %H:%M"),
                        "employee": employee_name,
                        "type": activity.activity_type.replace("_", " ").title(),
                        "description": activity.activity_description
                    })
                
                # Get activity timeline (last 7 days)
                timeline_data = defaultdict(lambda: {"vm": 0, "image": 0, "log": 0, "dat": 0})
                
                for i in range(7):
                    day = today - timedelta(days=i)
                    next_day = day + timedelta(days=1)
                    
                    # Count activities for this day
                    day_activities = session.exec(
                        select(UserActivity.activity_type, func.count(UserActivity.activity_id))
                        .where(
                            and_(
                                UserActivity.activity_timestamp >= day,
                                UserActivity.activity_timestamp < next_day
                            )
                        )
                        .group_by(UserActivity.activity_type)
                    ).all()
                    
                    day_str = day.strftime("%Y-%m-%d")
                    for activity_type, count in day_activities:
                        if activity_type == "vm_created":
                            timeline_data[day_str]["vm"] = count
                        elif activity_type == "image_captured":
                            timeline_data[day_str]["image"] = count
                        elif activity_type == "log_added":
                            timeline_data[day_str]["log"] = count
                        elif activity_type == "dat_updated":
                            timeline_data[day_str]["dat"] = count
                
                # Convert timeline data to list format
                self.activity_timeline = []
                for i in range(6, -1, -1):  # Reverse order for chronological display
                    day = today - timedelta(days=i)
                    day_str = day.strftime("%Y-%m-%d")
                    day_display = day.strftime("%b %d")
                    
                    self.activity_timeline.append({
                        "date": day_display,
                        "vm": timeline_data[day_str]["vm"],
                        "image": timeline_data[day_str]["image"],
                        "log": timeline_data[day_str]["log"],
                        "dat": timeline_data[day_str]["dat"]
                    })
                
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
        finally:
            self.is_loading = False
            yield