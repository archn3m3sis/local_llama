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


class DashboardState(rx.State):
    """State for Dashboard analytics and visualizations."""
    
    # Activity summary data
    total_activities: int = 0
    activities_today: int = 0
    activities_this_week: int = 0
    activities_this_month: int = 0
    
    # Activity by type
    vm_creations: int = 0
    image_captures: int = 0
    log_collections: int = 0
    dat_updates: int = 0
    
    # Activity by employee
    top_employees: list[dict] = []
    
    # Activity by project
    project_activities: list[dict] = []
    
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
                
                self.top_employees = []
                for emp_id, count in employee_activities:
                    employee = session.exec(
                        select(Employee).where(Employee.id == emp_id)
                    ).first()
                    if employee:
                        self.top_employees.append({
                            "name": f"{employee.first_name} {employee.last_name}",
                            "count": count
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
                
                self.project_activities = []
                for proj_id, count in project_activities:
                    project = session.exec(
                        select(Project).where(Project.project_id == proj_id)
                    ).first()
                    if project:
                        self.project_activities.append({
                            "name": project.project_name,
                            "count": count
                        })
                
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