"""State management for the Playbook page."""
import reflex as rx
from typing import List, Dict, Optional
from datetime import datetime


class PlaybookState(rx.State):
    """State for the Playbook page."""
    
    # Search and filtering
    search_query: str = ""
    selected_category: str = "All"
    
    # Available categories
    categories: List[str] = [
        "All",
        "Incident Response",
        "Maintenance",
        "Compliance",
        "Emergency",
        "Security",
        "Operations",
        "Training"
    ]
    
    # Sample recent playbooks data
    recent_playbooks: List[Dict] = [
        {
            "title": "Active Directory Compromise Response",
            "category": "Incident Response",
            "description": "Step-by-step procedure for responding to AD compromise incidents",
            "status": "published",
            "updated": "2 hours ago"
        },
        {
            "title": "Monthly System Patching Procedure",
            "category": "Maintenance",
            "description": "Standard operating procedure for monthly security updates",
            "status": "published",
            "updated": "1 day ago"
        },
        {
            "title": "STIG Compliance Validation",
            "category": "Compliance",
            "description": "Automated checks and manual validation steps for STIG compliance",
            "status": "draft",
            "updated": "3 days ago"
        },
        {
            "title": "Power Outage Recovery",
            "category": "Emergency",
            "description": "Emergency procedures for system recovery after power loss",
            "status": "published",
            "updated": "1 week ago"
        },
        {
            "title": "New Employee Security Onboarding",
            "category": "Security",
            "description": "Security checklist and procedures for new employee setup",
            "status": "published",
            "updated": "2 weeks ago"
        }
    ]
    
    # Modal states
    create_modal_open: bool = False
    template_gallery_open: bool = False
    import_export_open: bool = False
    
    def load_playbooks(self):
        """Load playbooks from database."""
        # TODO: Implement database loading
        print("Loading playbooks...")
    
    def set_search_query(self, value: str):
        """Update search query."""
        self.search_query = value
        # TODO: Implement search filtering
    
    def set_selected_category(self, category: str):
        """Set the selected category filter."""
        self.selected_category = category
        # TODO: Implement category filtering
    
    def filter_by_category(self, category: str):
        """Filter playbooks by category."""
        self.selected_category = category
        # TODO: Implement filtering logic
    
    def open_create_modal(self):
        """Open the create playbook modal."""
        self.create_modal_open = True
    
    def close_create_modal(self):
        """Close the create playbook modal."""
        self.create_modal_open = False
    
    def open_template_gallery(self):
        """Open the template gallery modal."""
        self.template_gallery_open = True
    
    def close_template_gallery(self):
        """Close the template gallery modal."""
        self.template_gallery_open = False
    
    def open_import_export(self):
        """Open the import/export modal."""
        self.import_export_open = True
    
    def close_import_export(self):
        """Close the import/export modal."""
        self.import_export_open = False
    
    def create_playbook(self, title: str, category: str, content: str):
        """Create a new playbook."""
        # TODO: Implement playbook creation
        print(f"Creating playbook: {title} in category {category}")
        self.create_modal_open = False
    
    def import_playbooks(self, file_data: str):
        """Import playbooks from file."""
        # TODO: Implement import functionality
        print("Importing playbooks...")
        self.import_export_open = False
    
    def export_playbooks(self, format: str = "json"):
        """Export playbooks to file."""
        # TODO: Implement export functionality
        print(f"Exporting playbooks as {format}")
        self.import_export_open = False
    
    def scroll_carousel_left(self):
        """Scroll the carousel left."""
        rx.call_script("""
            const carousel = document.getElementById('playbook-carousel');
            if (carousel) {
                carousel.scrollBy({
                    left: -320,
                    behavior: 'smooth'
                });
            }
        """)
    
    def scroll_carousel_right(self):
        """Scroll the carousel right."""
        rx.call_script("""
            const carousel = document.getElementById('playbook-carousel');
            if (carousel) {
                carousel.scrollBy({
                    left: 320,
                    behavior: 'smooth'
                });
            }
        """)