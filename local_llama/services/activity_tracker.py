"""User Activity Tracking Service."""
import json
from typing import Optional, Dict, Any
from datetime import datetime
import reflex as rx
from sqlmodel import select
from ..models.user_activity import UserActivity
from ..models.app_user import AppUser


class ActivityTracker:
    """Service for tracking user activities in the application."""
    
    # Activity type constants
    VM_CREATED = "vm_created"
    VM_UPDATED = "vm_updated"
    IMAGE_CAPTURED = "image_captured"
    LOG_ADDED = "log_added"
    DAT_UPDATED = "dat_updated"
    ASSET_CREATED = "asset_created"
    ASSET_UPDATED = "asset_updated"
    
    @staticmethod
    def get_current_user_id() -> Optional[int]:
        """Get the current logged-in user's ID.
        
        This is a placeholder - you'll need to implement this based on your auth system.
        For now, we'll return a default user ID.
        """
        # TODO: Implement actual user ID retrieval from Clerk auth
        # For now, return the first user ID as a placeholder
        try:
            with rx.session() as session:
                user = session.exec(
                    select(AppUser).limit(1)
                ).first()
                return user.id if user else None
        except:
            return None
    
    @staticmethod
    def track_activity(
        activity_type: str,
        description: str,
        related_asset_id: Optional[int] = None,
        related_project_id: Optional[int] = None,
        related_vm_id: Optional[int] = None,
        related_image_id: Optional[int] = None,
        related_log_id: Optional[int] = None,
        related_dat_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
        employee_id: Optional[int] = None
    ) -> bool:
        """Track a user activity.
        
        Args:
            activity_type: Type of activity (use constants defined above)
            description: Human-readable description of the activity
            related_*_id: Optional IDs of related entities
            metadata: Optional dictionary of additional data
            user_id: Override user ID (if not provided, uses current user)
            employee_id: Employee ID if available
            
        Returns:
            True if activity was tracked successfully, False otherwise
        """
        try:
            with rx.session() as session:
                # Get user ID if not provided
                if user_id is None:
                    user_id = ActivityTracker.get_current_user_id()
                
                if user_id is None:
                    print("Warning: No user ID available for activity tracking")
                    return False
                
                # Create activity record
                activity = UserActivity(
                    user_id=user_id,
                    employee_id=employee_id,
                    activity_type=activity_type,
                    activity_description=description,
                    related_asset_id=related_asset_id,
                    related_project_id=related_project_id,
                    related_vm_id=related_vm_id,
                    related_image_id=related_image_id,
                    related_log_id=related_log_id,
                    related_dat_id=related_dat_id,
                    activity_timestamp=datetime.now(),
                    activity_metadata=json.dumps(metadata) if metadata else None
                )
                
                session.add(activity)
                session.commit()
                
                print(f"Activity tracked: {activity_type} - {description}")
                return True
                
        except Exception as e:
            print(f"Error tracking activity: {e}")
            return False
    
    @staticmethod
    def track_vm_creation(vm_id: int, asset_id: int, project_id: int, employee_id: int, vm_type: str):
        """Track VM creation activity."""
        return ActivityTracker.track_activity(
            activity_type=ActivityTracker.VM_CREATED,
            description=f"Created virtual machine (Type: {vm_type})",
            related_vm_id=vm_id,
            related_asset_id=asset_id,
            related_project_id=project_id,
            employee_id=employee_id,
            metadata={"vm_type": vm_type}
        )
    
    @staticmethod
    def track_vm_update(vm_id: int, employee_id: int, changes: Dict[str, Any]):
        """Track VM update activity."""
        change_summary = ", ".join([f"{k}: {v}" for k, v in changes.items()])
        return ActivityTracker.track_activity(
            activity_type=ActivityTracker.VM_UPDATED,
            description=f"Updated virtual machine ({change_summary})",
            related_vm_id=vm_id,
            employee_id=employee_id,
            metadata=changes
        )
    
    @staticmethod
    def track_image_capture(image_id: int, asset_id: int, project_id: int, employee_id: int, method: str):
        """Track image capture activity."""
        return ActivityTracker.track_activity(
            activity_type=ActivityTracker.IMAGE_CAPTURED,
            description=f"Captured image using {method}",
            related_image_id=image_id,
            related_asset_id=asset_id,
            related_project_id=project_id,
            employee_id=employee_id,
            metadata={"imaging_method": method}
        )
    
    @staticmethod
    def track_log_collection(log_id: int, asset_id: int, project_id: int, employee_id: int, log_type: str):
        """Track log collection activity."""
        return ActivityTracker.track_activity(
            activity_type=ActivityTracker.LOG_ADDED,
            description=f"Collected {log_type} logs",
            related_log_id=log_id,
            related_asset_id=asset_id,
            related_project_id=project_id,
            employee_id=employee_id,
            metadata={"log_type": log_type}
        )
    
    @staticmethod
    def track_dat_update(dat_id: int, asset_id: int, project_id: int, employee_id: int, dat_version: str):
        """Track DAT update activity."""
        return ActivityTracker.track_activity(
            activity_type=ActivityTracker.DAT_UPDATED,
            description=f"Updated DAT to version {dat_version}",
            related_dat_id=dat_id,
            related_asset_id=asset_id,
            related_project_id=project_id,
            employee_id=employee_id,
            metadata={"dat_version": dat_version}
        )