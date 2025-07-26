"""Authentication state management."""
import reflex as rx
from typing import Optional
import os
from sqlmodel import Session, create_engine, select
from ..models.employee import Employee


class AuthState(rx.State):
    """State for managing authentication and user information."""
    
    current_employee_id: Optional[int] = None
    current_employee_name: Optional[str] = None
    current_employee_email: Optional[str] = None
    is_cybersecurity_team: bool = False
    clerk_user_email: Optional[str] = None
    
    def set_clerk_user_email(self, email: str):
        """Set the Clerk user email from the frontend."""
        self.clerk_user_email = email
        self.load_current_user_by_email(email)
    
    def load_current_user_by_email(self, email: str):
        """Load current user information by email."""
        if not email:
            print("No email provided")
            return
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("Database URL not found")
            return
        
        engine = create_engine(database_url)
        with Session(engine) as session:
            # Find employee by email
            employee = session.exec(
                select(Employee).where(Employee.email == email)
            ).first()
            
            if employee:
                self.current_employee_id = employee.id
                self.current_employee_name = f"{employee.first_name} {employee.last_name}"
                self.current_employee_email = employee.email
                
                # Check if user is in cybersecurity team
                # Department 2 is Cybersecurity, or they are Robert Shipp (manager)
                self.is_cybersecurity_team = (
                    employee.department_id == 2 or 
                    employee.email == "robert.shipp.2.civ@army.mil"
                )
                
                print(f"Loaded employee: {self.current_employee_name} (ID: {self.current_employee_id})")
                print(f"Is cybersecurity team: {self.is_cybersecurity_team}")
            else:
                print(f"No employee found for email: {email}")
                # Reset state
                self.current_employee_id = None
                self.current_employee_name = None
                self.current_employee_email = None
                self.is_cybersecurity_team = False