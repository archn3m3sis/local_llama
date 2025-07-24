"""State management for the Playbook Editor page."""
import reflex as rx
from typing import List, Optional
from datetime import datetime


class PlaybookEditorState(rx.State):
    """State for the Playbook Editor page."""
    
    # Editor content
    title: str = ""
    content: str = ""
    category: str = ""
    tags: List[str] = []
    tag_input: str = ""
    
    # Editor state
    preview_mode: bool = False
    split_view: bool = False
    auto_saved: bool = False
    
    # Metadata
    status: str = "Draft"
    created_date: str = datetime.now().strftime("%Y-%m-%d")
    modified_date: str = datetime.now().strftime("%Y-%m-%d %H:%M")
    version: int = 1
    
    # Available categories
    categories: List[str] = [
        "Incident Response",
        "Maintenance", 
        "Compliance",
        "Emergency",
        "Security",
        "Operations",
        "Training"
    ]
    
    def set_title(self, value: str):
        """Update the playbook title."""
        self.title = value
        self.auto_save()
    
    def set_content(self, value: str):
        """Update the playbook content."""
        self.content = value
        self.auto_save()
    
    def set_category(self, value: str):
        """Update the playbook category."""
        self.category = value
        self.auto_save()
    
    def set_tag_input(self, value: str):
        """Update the tag input field."""
        self.tag_input = value
    
    def handle_tag_input(self, key: str):
        """Handle keyboard input for tags."""
        if key == "Enter" and self.tag_input.strip():
            if self.tag_input not in self.tags:
                self.tags.append(self.tag_input.strip())
                self.tag_input = ""
                self.auto_save()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the list."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.auto_save()
    
    def toggle_preview(self):
        """Toggle between edit and preview modes."""
        self.preview_mode = not self.preview_mode
    
    def auto_save(self):
        """Trigger auto-save (simulation)."""
        self.auto_saved = True
        self.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        # In real implementation, this would save to database
        # Reset auto-saved indicator after 2 seconds
        rx.call_script("""
            setTimeout(() => {
                window.reflex_updateState({auto_saved: false});
            }, 2000);
        """)
    
    def save_draft(self):
        """Save the playbook as a draft."""
        self.status = "Draft"
        self.auto_save()
        # TODO: Save to database
        rx.toast.success("Draft saved successfully!")
    
    def publish(self):
        """Publish the playbook."""
        if not self.title:
            rx.toast.error("Please add a title before publishing")
            return
        if not self.content:
            rx.toast.error("Please add content before publishing")
            return
        if not self.category:
            rx.toast.error("Please select a category before publishing")
            return
            
        self.status = "Published"
        self.version += 1
        self.auto_save()
        # TODO: Save to database with published status
        rx.toast.success("Playbook published successfully!")
    
    def export_markdown(self):
        """Export the playbook as a markdown file."""
        # Create markdown content with metadata
        export_content = f"""---
title: {self.title}
category: {self.category}
tags: {', '.join(self.tags)}
status: {self.status}
version: {self.version}
created: {self.created_date}
modified: {self.modified_date}
---

{self.content}
"""
        # TODO: Implement actual file download
        rx.download(
            data=export_content,
            filename=f"{self.title.lower().replace(' ', '_')}_playbook.md"
        )
    
    def duplicate_playbook(self):
        """Create a duplicate of the current playbook."""
        # TODO: Create new playbook with same content but new ID
        rx.toast.info("Playbook duplicated - editing new copy")
        self.title = f"{self.title} (Copy)"
        self.status = "Draft"
        self.version = 1
        self.created_date = datetime.now().strftime("%Y-%m-%d")
        self.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Formatting functions
    def format_bold(self):
        """Apply bold formatting."""
        self.insert_formatting("**", "**")
    
    def format_italic(self):
        """Apply italic formatting."""
        self.insert_formatting("*", "*")
    
    def format_underline(self):
        """Apply underline formatting."""
        self.insert_formatting("<u>", "</u>")
    
    def format_code(self):
        """Apply code formatting."""
        self.insert_formatting("`", "`")
    
    def format_header(self, level: int):
        """Apply header formatting."""
        prefix = "#" * level + " "
        self.insert_at_line_start(prefix)
    
    def format_bullet_list(self):
        """Apply bullet list formatting."""
        self.insert_at_line_start("- ")
    
    def format_numbered_list(self):
        """Apply numbered list formatting."""
        self.insert_at_line_start("1. ")
    
    def format_checklist(self):
        """Apply checklist formatting."""
        self.insert_at_line_start("- [ ] ")
    
    def format_blockquote(self):
        """Apply blockquote formatting."""
        self.insert_at_line_start("> ")
    
    def insert_link(self):
        """Insert a link."""
        # In a real implementation, this would open a modal
        self.insert_formatting("[", "](url)")
    
    def insert_image(self):
        """Insert an image."""
        # In a real implementation, this would open an upload modal
        self.insert_formatting("![", "](image-url)")
    
    def insert_table(self):
        """Insert a table template."""
        table_template = """
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
"""
        self.content += table_template
    
    def insert_formatting(self, prefix: str, suffix: str):
        """Helper to insert formatting around selected text."""
        # In a real implementation, this would handle text selection
        # For now, just append to content
        self.content += f"{prefix}text{suffix}"
    
    def insert_at_line_start(self, prefix: str):
        """Helper to insert text at the start of the current line."""
        # In a real implementation, this would handle cursor position
        # For now, just append on a new line
        if self.content and not self.content.endswith("\n"):
            self.content += "\n"
        self.content += prefix