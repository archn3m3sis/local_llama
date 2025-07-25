"""State management for the Playbook Editor page."""
import reflex as rx
from typing import List, Optional
from datetime import datetime


class PlaybookEditorState(rx.State):
    """State for the Playbook Editor page."""
    
    # Editor content
    title: str = "Sample Incident Response Playbook"
    content: str = """# Sample Incident Response Playbook

This is a **sample playbook** to demonstrate the markdown editor.

## Overview

This playbook provides step-by-step guidance for handling security incidents.

## Prerequisites

- Access to incident response tools
- Communication channels established
- Team members assigned

## Response Steps

### 1. Initial Assessment

- [ ] Identify the nature of the incident
- [ ] Determine severity level
- [ ] Notify relevant stakeholders

### 2. Containment

```bash
# Example: Isolate affected systems
sudo iptables -A INPUT -s suspicious_ip -j DROP
```

### 3. Investigation

| Task | Owner | Status |
|------|-------|--------|
| Log Analysis | Security Team | Pending |
| Forensics | IR Team | In Progress |
| Root Cause | Lead Analyst | Not Started |

### 4. Recovery

1. Restore from clean backups
2. Apply security patches
3. Monitor for recurrence

> **Important:** Document all actions taken during the incident response process.

## Contact Information

- Security Team: security@example.com
- On-call: +1-555-0123

---

*Last updated: {datetime.now().strftime("%Y-%m-%d")}*
"""
    category: str = "Incident Response"
    tags: List[str] = ["security", "incident", "response"]
    tag_input: str = ""
    
    # Editor state
    preview_mode: bool = False
    split_view: bool = False
    auto_saved: bool = False
    show_source: bool = False  # For WYSIWYG editor
    is_public: bool = False  # Personal/Public toggle
    
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
    
    def toggle_show_source(self):
        """Toggle showing markdown source in WYSIWYG editor."""
        self.show_source = not self.show_source
    
    def set_is_public(self, value: bool):
        """Set whether the playbook is public or personal."""
        self.is_public = value
        self.auto_save()
    
    def auto_save(self):
        """Trigger auto-save (simulation)."""
        self.auto_saved = True
        self.modified_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        # In real implementation, this would save to database
        # Note: Auto-save indicator would normally reset after a delay
    
    def save_draft(self):
        """Save the playbook as a draft."""
        self.status = "Draft"
        self.auto_save()
        # TODO: Save to database
        rx.toast.success("Draft saved successfully!")
    
    def publish_playbook(self):
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
    
    def load_template(self, template_type: str):
        """Load a template based on type."""
        templates = {
            "incident": """# Incident Response Playbook

## Overview
This playbook provides step-by-step guidance for handling security incidents.

## Incident Classification
- [ ] Security Breach
- [ ] Data Leak
- [ ] Malware Infection
- [ ] Unauthorized Access
- [ ] Other: _______________

## Initial Response Steps

### 1. Detection and Analysis
- [ ] Identify the incident type
- [ ] Determine the scope and impact
- [ ] Document initial findings
- [ ] Assign severity level (Critical/High/Medium/Low)

### 2. Containment
- [ ] Isolate affected systems
- [ ] Preserve evidence
- [ ] Prevent further damage
- [ ] Document actions taken

### 3. Eradication
- [ ] Remove malicious code/access
- [ ] Patch vulnerabilities
- [ ] Update security controls
- [ ] Verify remediation

### 4. Recovery
- [ ] Restore systems from clean backups
- [ ] Monitor for recurrence
- [ ] Validate system integrity
- [ ] Return to normal operations

### 5. Post-Incident Activities
- [ ] Complete incident report
- [ ] Conduct lessons learned session
- [ ] Update security procedures
- [ ] Share threat intelligence

## Contact Information
- Security Team: security@company.com
- On-Call: +1-555-0123
- Management: management@company.com
""",
            "audit": """# Security Audit Playbook

## Audit Overview
**Audit Type:** [System/Application/Network/Compliance]
**Audit Date:** [Date]
**Auditor:** [Name]

## Pre-Audit Checklist
- [ ] Define audit scope
- [ ] Gather system documentation
- [ ] Identify stakeholders
- [ ] Schedule audit activities
- [ ] Prepare audit tools

## Audit Areas

### 1. Access Control
- [ ] Review user accounts and permissions
- [ ] Check password policies
- [ ] Verify multi-factor authentication
- [ ] Audit privileged access

### 2. Network Security
- [ ] Review firewall rules
- [ ] Check network segmentation
- [ ] Verify encryption protocols
- [ ] Test intrusion detection

### 3. System Configuration
- [ ] Review OS hardening
- [ ] Check patch management
- [ ] Verify logging configuration
- [ ] Audit backup procedures

### 4. Compliance
- [ ] Review policy adherence
- [ ] Check regulatory compliance
- [ ] Verify data protection measures
- [ ] Audit incident response procedures

## Findings Summary
| Finding | Severity | Recommendation | Status |
|---------|----------|----------------|--------|
| | | | |

## Next Steps
1. 
2. 
3. 
""",
            "maintenance": """# System Maintenance Playbook

## Maintenance Window
**Date:** [Date]
**Time:** [Start Time] - [End Time]
**Systems Affected:** [List of systems]
**Impact:** [Description of impact]

## Pre-Maintenance Checklist
- [ ] Send maintenance notification
- [ ] Backup critical data
- [ ] Document current configuration
- [ ] Prepare rollback plan
- [ ] Verify maintenance tools

## Maintenance Tasks

### 1. System Updates
- [ ] Apply OS patches
- [ ] Update applications
- [ ] Upgrade firmware
- [ ] Install security updates

### 2. Configuration Changes
- [ ] Update system settings
- [ ] Modify network configuration
- [ ] Adjust security policies
- [ ] Optimize performance settings

### 3. Health Checks
- [ ] Verify system functionality
- [ ] Test critical services
- [ ] Check system resources
- [ ] Review error logs

### 4. Documentation
- [ ] Update configuration records
- [ ] Document changes made
- [ ] Update system diagrams
- [ ] Record test results

## Post-Maintenance
- [ ] Verify system operation
- [ ] Monitor for issues
- [ ] Send completion notification
- [ ] Update maintenance log

## Rollback Procedure
1. 
2. 
3. 

## Contact Information
- Primary Contact: [Name/Email]
- Backup Contact: [Name/Email]
- Emergency: [Phone]
"""
        }
        
        if template_type in templates:
            self.content = templates[template_type]
            self.title = f"{template_type.capitalize()} Response Playbook"
            self.auto_save()