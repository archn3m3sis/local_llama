from typing import Dict, Any
import reflex as rx


class SpeedDialState(rx.State):
    """State for the main speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


def radial_speed_dial() -> rx.Component:
    """Create a radial speed dial component with navigation items."""
    nav_items = [
        {"icon": "book-open", "label": "Log Collection", "route": "/logs"},
        {"icon": "refresh-cw", "label": "DAT Updates", "route": "/dats"},
        {"icon": "monitor", "label": "Device Patching", "route": "/patching"},
        {"icon": "image", "label": "Image Capture", "route": "/images"},
        {"icon": "server", "label": "VM Creation", "route": "/vm_creation"},
        {"icon": "user", "label": "Access Control", "route": "/access"},
        {"icon": "git-branch", "label": "Change Management", "route": "/configuration_management"},
        {"icon": "book", "label": "Playbook Library", "route": "/playbook"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Color scheme for main navigation - cool blues and cyans
        colors = [
            {"bg": "linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(59, 130, 246, 0.4)", "glow": "59, 130, 246"},  # Blue
            {"bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(16, 185, 129, 0.4)", "glow": "16, 185, 129"},  # Green
            {"bg": "linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(124, 58, 237, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(139, 92, 246, 0.4)", "glow": "139, 92, 246"},  # Purple
            {"bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(239, 68, 68, 0.4)", "glow": "239, 68, 68"},  # Red
            {"bg": "linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(217, 119, 6, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(245, 158, 11, 0.4)", "glow": "245, 158, 11"},  # Amber
            {"bg": "linear-gradient(135deg, rgba(6, 182, 212, 0.3) 0%, rgba(8, 145, 178, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(6, 182, 212, 0.4)", "glow": "6, 182, 212"},  # Cyan
            {"bg": "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(99, 102, 241, 0.4)", "glow": "99, 102, 241"},  # Indigo
        ]
        
        color_scheme = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color_scheme["bg"],
                    border=f"2px solid {color_scheme['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                    _hover={
                        "box_shadow": f"0 0 25px rgba({color_scheme['glow']}, 0.6), 0 8px 32px rgba(0, 0, 0, 0.3)",
                        "border": f"2px solid rgba({color_scheme['glow']}, 0.8)",
                        "transform": "scale(1.1)",
                    }
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(SpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                SpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(SpeedDialState.is_open, "auto", "none"),
            on_click=SpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        # Glass backdrop strip for all speed dials
        rx.box(
            position="fixed",
            bottom="0",
            left="0",
            width="100vw",
            height="8rem",
            background="linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.1) 30%, rgba(0, 0, 0, 0.2) 100%)",
            backdrop_filter="blur(20px)",
            z_index="999",  # Behind speed dials and text labels
            pointer_events="none",  # Allow clicks to pass through
        ),
        
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.3)",
            backdrop_filter="blur(2px)",
            z_index="1001",
            opacity=rx.cond(SpeedDialState.is_open, "1", "0"),
            visibility=rx.cond(SpeedDialState.is_open, "visible", "hidden"),
            transition="all 0.3s ease",
            pointer_events=rx.cond(SpeedDialState.is_open, "auto", "none"),
            on_click=SpeedDialState.toggle_speed_dial,
        ),
        
        rx.vstack(
            *reversed(nav_buttons),
            spacing="1",
            position="absolute",
            bottom="5rem",
            left="5rem",
            z_index="1002",
            opacity=rx.cond(SpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                SpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(30px) scale(0.9)"
            ),
            transition="all 0.3s cubic-bezier(0.23, 1, 0.32, 1)",
            pointer_events=rx.cond(SpeedDialState.is_open, "auto", "none"),
        ),
        
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(SpeedDialState.is_open, "x", "menu"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    SpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        SpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=SpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Core Actions",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(SpeedDialState.is_open, "0", "1"),
                transform=rx.cond(SpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
            width="auto",
            min_width="200px",
        ),
        
        position="fixed",
        bottom="2rem",
        left="1rem",
        z_index="1003",
    )


class AnalyticsSpeedDialState(rx.State):
    """State for the analytics speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


class SecuritySpeedDialState(rx.State):
    """State for the security speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


def security_speed_dial() -> rx.Component:
    """Create a security-focused speed dial component with playbook options."""
    nav_items = [
        {"icon": "book", "label": "Playbook Home", "route": "/playbook"},
        {"icon": "file-plus", "label": "Create Playbook", "route": "/playbook/create"},
        {"icon": "folder-open", "label": "Browse Templates", "route": "/playbook/templates"},
        {"icon": "shield", "label": "Security Policies", "route": "/security/policies"},
        {"icon": "triangle-alert", "label": "Incident Response", "route": "/security/incidents"},
        {"icon": "lock", "label": "Access Control", "route": "/security/access"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Color scheme for security - reds and purples
        colors = [
            {"bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(239, 68, 68, 0.4)", "glow": "239, 68, 68"},  # Red
            {"bg": "linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(219, 39, 119, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(236, 72, 153, 0.4)", "glow": "236, 72, 153"},  # Pink
            {"bg": "linear-gradient(135deg, rgba(168, 85, 247, 0.3) 0%, rgba(147, 51, 234, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(168, 85, 247, 0.4)", "glow": "168, 85, 247"},  # Purple
            {"bg": "linear-gradient(135deg, rgba(217, 70, 239, 0.3) 0%, rgba(196, 25, 225, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(217, 70, 239, 0.4)", "glow": "217, 70, 239"},  # Fuchsia
            {"bg": "linear-gradient(135deg, rgba(244, 63, 94, 0.3) 0%, rgba(225, 29, 72, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(244, 63, 94, 0.4)", "glow": "244, 63, 94"},  # Rose
            {"bg": "linear-gradient(135deg, rgba(190, 18, 60, 0.3) 0%, rgba(159, 18, 57, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(190, 18, 60, 0.4)", "glow": "190, 18, 60"},  # Wine
        ]
        
        color_scheme = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color_scheme["bg"],
                    border=f"2px solid {color_scheme['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                    _hover={
                        "box_shadow": f"0 0 25px rgba({color_scheme['glow']}, 0.6), 0 8px 32px rgba(0, 0, 0, 0.3)",
                        "border": f"2px solid rgba({color_scheme['glow']}, 0.8)",
                        "transform": "scale(1.1)",
                    }
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(SecuritySpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                SecuritySpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(SecuritySpeedDialState.is_open, "auto", "none"),
            on_click=SecuritySpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        # Glass backdrop strip
        rx.box(
            style={
                "position": "absolute",
                "right": "-10px",
                "top": "50%",
                "transform": "translateY(-50%)",
                "width": "300px",
                "height": rx.cond(SecuritySpeedDialState.is_open, "400px", "80px"),
                "background": rx.cond(
                    SecuritySpeedDialState.is_open,
                    "linear-gradient(90deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.4) 50%, transparent 100%)",
                    "linear-gradient(90deg, rgba(0, 0, 0, 0.4) 0%, transparent 100%)"
                ),
                "backdrop_filter": "blur(10px)",
                "border_radius": "40px 0 0 40px",
                "transition": "all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                "z_index": "1001",
            }
        ),
        
        # Navigation items
        rx.vstack(
            *nav_buttons,
            spacing="2",
            align="end",
            position="absolute",
            right="80px",
            top="50%",
            transform="translateY(-50%)",
            z_index="1002",
        ),
        
        # Main trigger button
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(SecuritySpeedDialState.is_open, "x", "shield"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    SecuritySpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        SecuritySpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=SecuritySpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Security",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(SecuritySpeedDialState.is_open, "0", "1"),
                transform=rx.cond(SecuritySpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
            width="auto",
            min_width="180px",
        ),
        
        position="fixed",
        bottom="8rem",
        left="1rem",
        z_index="1003",
    )


def analytics_speed_dial() -> rx.Component:
    """Create an analytics-focused speed dial component."""
    nav_items = [
        {"icon": "bar-chart", "label": "Performance Metrics", "route": "/analytics/performance"},
        {"icon": "pie-chart", "label": "Asset Distribution", "route": "/analytics/distribution"},
        {"icon": "trending-up", "label": "Trend Analysis", "route": "/analytics/trends"},
        {"icon": "activity", "label": "Real-time Monitor", "route": "/analytics/realtime"},
        {"icon": "target", "label": "Compliance Score", "route": "/analytics/compliance"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Color scheme for analytics - warm oranges and reds
        colors = [
            {"bg": "linear-gradient(135deg, rgba(251, 146, 60, 0.3) 0%, rgba(249, 115, 22, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(251, 146, 60, 0.4)", "glow": "251, 146, 60"},  # Orange
            {"bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(239, 68, 68, 0.4)", "glow": "239, 68, 68"},  # Red
            {"bg": "linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(217, 119, 6, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(245, 158, 11, 0.4)", "glow": "245, 158, 11"},  # Amber
            {"bg": "linear-gradient(135deg, rgba(255, 99, 71, 0.3) 0%, rgba(255, 69, 58, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(255, 99, 71, 0.4)", "glow": "255, 99, 71"},  # Coral
            {"bg": "linear-gradient(135deg, rgba(234, 179, 8, 0.3) 0%, rgba(202, 138, 4, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(234, 179, 8, 0.4)", "glow": "234, 179, 8"},  # Yellow
        ]
        
        color_scheme = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color_scheme["bg"],
                    border=f"2px solid {color_scheme['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                    _hover={
                        "box_shadow": f"0 0 25px rgba({color_scheme['glow']}, 0.6), 0 8px 32px rgba(0, 0, 0, 0.3)",
                        "border": f"2px solid rgba({color_scheme['glow']}, 0.8)",
                        "transform": "scale(1.1)",
                    }
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(AnalyticsSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                AnalyticsSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(AnalyticsSpeedDialState.is_open, "auto", "none"),
            on_click=AnalyticsSpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.3)",
            backdrop_filter="blur(2px)",
            z_index="1001",
            opacity=rx.cond(AnalyticsSpeedDialState.is_open, "1", "0"),
            visibility=rx.cond(AnalyticsSpeedDialState.is_open, "visible", "hidden"),
            transition="all 0.3s ease",
            pointer_events=rx.cond(AnalyticsSpeedDialState.is_open, "auto", "none"),
            on_click=AnalyticsSpeedDialState.toggle_speed_dial,
        ),
        
        rx.vstack(
            *reversed(nav_buttons),
            spacing="1",
            position="absolute",
            bottom="5rem",
            left="5rem",
            z_index="1002",
            opacity=rx.cond(AnalyticsSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                AnalyticsSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(30px) scale(0.9)"
            ),
            transition="all 0.3s cubic-bezier(0.23, 1, 0.32, 1)",
            pointer_events=rx.cond(AnalyticsSpeedDialState.is_open, "auto", "none"),
        ),
        
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(AnalyticsSpeedDialState.is_open, "x", "bar-chart"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    AnalyticsSpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        AnalyticsSpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(124, 58, 237, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=AnalyticsSpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Analytics",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(AnalyticsSpeedDialState.is_open, "0", "1"),
                transform=rx.cond(AnalyticsSpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
        ),
        
        position="fixed",
        bottom="2rem",
        left="14rem",
        z_index="1003",
    )


class AssetDataSpeedDialState(rx.State):
    """State for the asset data speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


def asset_data_speed_dial() -> rx.Component:
    """Create an asset data focused speed dial component."""
    nav_items = [
        {"icon": "server", "label": "Industrial Assets", "route": "/assets"},
        {"icon": "file-text", "label": "Cradle To Graves", "route": "/cradle-to-grave"},
        {"icon": "clock", "label": "Configuration Timelines", "route": "/configuration-timelines"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Cool tech color palette for asset data
        colors = [
            {"bg": "linear-gradient(135deg, rgba(6, 182, 212, 0.3) 0%, rgba(14, 165, 233, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(6, 182, 212, 0.4)", "glow": "6, 182, 212"},  # Cyan
            {"bg": "linear-gradient(135deg, rgba(20, 184, 166, 0.3) 0%, rgba(13, 148, 136, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(20, 184, 166, 0.4)", "glow": "20, 184, 166"},  # Teal
            {"bg": "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(99, 102, 241, 0.4)", "glow": "99, 102, 241"},  # Indigo
            {"bg": "linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(22, 163, 74, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(34, 197, 94, 0.4)", "glow": "34, 197, 94"},  # Green
            {"bg": "linear-gradient(135deg, rgba(168, 85, 247, 0.3) 0%, rgba(147, 51, 234, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(168, 85, 247, 0.4)", "glow": "168, 85, 247"},  # Purple
            {"bg": "linear-gradient(135deg, rgba(14, 165, 233, 0.3) 0%, rgba(59, 130, 246, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(14, 165, 233, 0.4)", "glow": "14, 165, 233"},  # Blue
        ]
        
        color = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color["bg"],
                    border=f"2px solid {color['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    _hover={
                        "box_shadow": f"0 0 30px rgba({color['glow']}, 0.6), 0 12px 40px rgba(0, 0, 0, 0.4)",
                        "transform": "scale(1.05)",
                        "border": f"2px solid rgba({color['glow']}, 0.6)",
                        "background": color["bg"].replace("0.3)", "0.4)").replace("0.2)", "0.3)"),
                    },
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(AssetDataSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                AssetDataSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(AssetDataSpeedDialState.is_open, "auto", "none"),
            on_click=AssetDataSpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.3)",
            backdrop_filter="blur(2px)",
            z_index="1001",
            opacity=rx.cond(AssetDataSpeedDialState.is_open, "1", "0"),
            visibility=rx.cond(AssetDataSpeedDialState.is_open, "visible", "hidden"),
            transition="all 0.3s ease",
            pointer_events=rx.cond(AssetDataSpeedDialState.is_open, "auto", "none"),
            on_click=AssetDataSpeedDialState.toggle_speed_dial,
        ),
        
        rx.vstack(
            *reversed(nav_buttons),
            spacing="1",
            position="absolute",
            bottom="5rem",
            left="5rem",
            z_index="1002",
            opacity=rx.cond(AssetDataSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                AssetDataSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(30px) scale(0.9)"
            ),
            transition="all 0.3s cubic-bezier(0.23, 1, 0.32, 1)",
            pointer_events=rx.cond(AssetDataSpeedDialState.is_open, "auto", "none"),
        ),
        
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(AssetDataSpeedDialState.is_open, "x", "database"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    AssetDataSpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        AssetDataSpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=AssetDataSpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Asset Data",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(AssetDataSpeedDialState.is_open, "0", "1"),
                transform=rx.cond(AssetDataSpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
        ),
        
        position="fixed",
        bottom="2rem",
        left="24.5rem",
        z_index="1003",
    )


class PlaybookSpeedDialState(rx.State):
    """State for the playbook speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


def playbook_speed_dial() -> rx.Component:
    """Create a playbook-focused speed dial component."""
    nav_items = [
        {"icon": "home", "label": "Playbook Home", "route": "/playbook"},
        {"icon": "pencil", "label": "Playbook Editor", "route": "/playbook/editor"},
        {"icon": "book-open", "label": "SOP Documentation", "route": "/playbook/sop"},
        {"icon": "workflow", "label": "Internal Processes", "route": "/playbook/processes"},
        {"icon": "file-text", "label": "Technical Documentation", "route": "/playbook/technical"},
        {"icon": "user", "label": "Personal Logs", "route": "/playbook/personal"},
        {"icon": "pen-tool", "label": "Create Content", "route": "/playbook/create"},
        {"icon": "code", "label": "Code Snippets", "route": "/playbook/snippets"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Documentation-themed color palette for playbook
        colors = [
            {"bg": "linear-gradient(135deg, rgba(168, 85, 247, 0.3) 0%, rgba(147, 51, 234, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(168, 85, 247, 0.4)", "glow": "168, 85, 247"},  # Purple
            {"bg": "linear-gradient(135deg, rgba(236, 72, 153, 0.3) 0%, rgba(219, 39, 119, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(236, 72, 153, 0.4)", "glow": "236, 72, 153"},  # Pink
            {"bg": "linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(124, 58, 237, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(139, 92, 246, 0.4)", "glow": "139, 92, 246"},  # Violet
            {"bg": "linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(79, 70, 229, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(99, 102, 241, 0.4)", "glow": "99, 102, 241"},  # Indigo
            {"bg": "linear-gradient(135deg, rgba(244, 63, 94, 0.3) 0%, rgba(225, 29, 72, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(244, 63, 94, 0.4)", "glow": "244, 63, 94"},  # Rose
            {"bg": "linear-gradient(135deg, rgba(192, 132, 252, 0.3) 0%, rgba(168, 85, 247, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(192, 132, 252, 0.4)", "glow": "192, 132, 252"},  # Light Purple
        ]
        
        color = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color["bg"],
                    border=f"2px solid {color['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    _hover={
                        "box_shadow": f"0 0 30px rgba({color['glow']}, 0.6), 0 12px 40px rgba(0, 0, 0, 0.4)",
                        "transform": "scale(1.05)",
                        "border": f"2px solid rgba({color['glow']}, 0.6)",
                        "background": color["bg"].replace("0.3)", "0.4)").replace("0.2)", "0.3)"),
                    },
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(PlaybookSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                PlaybookSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(PlaybookSpeedDialState.is_open, "auto", "none"),
            on_click=PlaybookSpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.3)",
            backdrop_filter="blur(2px)",
            z_index="1001",
            opacity=rx.cond(PlaybookSpeedDialState.is_open, "1", "0"),
            visibility=rx.cond(PlaybookSpeedDialState.is_open, "visible", "hidden"),
            transition="all 0.3s ease",
            pointer_events=rx.cond(PlaybookSpeedDialState.is_open, "auto", "none"),
            on_click=PlaybookSpeedDialState.toggle_speed_dial,
        ),
        
        rx.vstack(
            *reversed(nav_buttons),
            spacing="1",
            position="absolute",
            bottom="5rem",
            left="5rem",
            z_index="1002",
            opacity=rx.cond(PlaybookSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                PlaybookSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(30px) scale(0.9)"
            ),
            transition="all 0.3s cubic-bezier(0.23, 1, 0.32, 1)",
            pointer_events=rx.cond(PlaybookSpeedDialState.is_open, "auto", "none"),
        ),
        
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(PlaybookSpeedDialState.is_open, "x", "book"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    PlaybookSpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        PlaybookSpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=PlaybookSpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Playbook",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(PlaybookSpeedDialState.is_open, "0", "1"),
                transform=rx.cond(PlaybookSpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
        ),
        
        position="fixed",
        bottom="2rem",
        left="35.5rem",
        z_index="1003",
    )


class VaultSpeedDialState(rx.State):
    """State for the vault speed dial component."""
    is_open: bool = False
    
    def toggle_speed_dial(self):
        """Toggle the speed dial open/closed state."""
        self.is_open = not self.is_open


def vault_speed_dial() -> rx.Component:
    """Create a vault-focused speed dial component."""
    nav_items = [
        {"icon": "key", "label": "Bitlocker Keys", "route": "/vault/bitlocker"},
        {"icon": "cpu", "label": "BIOS Credentials", "route": "/vault/bios"},
        {"icon": "shield", "label": "Other Credentials", "route": "/vault/credentials"}
    ]
    
    def create_nav_item(item: Dict[str, str], index: int) -> rx.Component:
        delay = f"{(index + 1) * 0.1}s"
        
        # Security-themed color palette for vault
        colors = [
            {"bg": "linear-gradient(135deg, rgba(245, 158, 11, 0.3) 0%, rgba(217, 119, 6, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(245, 158, 11, 0.4)", "glow": "245, 158, 11"},  # Amber
            {"bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(16, 185, 129, 0.4)", "glow": "16, 185, 129"},  # Emerald
            {"bg": "linear-gradient(135deg, rgba(251, 191, 36, 0.3) 0%, rgba(245, 158, 11, 0.2) 50%, rgba(255, 255, 255, 0.1) 100%)", "border": "rgba(251, 191, 36, 0.4)", "glow": "251, 191, 36"},  # Yellow
        ]
        
        color = colors[index % len(colors)]
        
        return rx.link(
            rx.hstack(
                rx.box(
                    rx.icon(
                        tag=item["icon"],
                        size=20,
                        color="white"
                    ),
                    width="3rem",
                    height="3rem",
                    border_radius="50%",
                    background=color["bg"],
                    border=f"2px solid {color['border']}",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                    _hover={
                        "box_shadow": f"0 0 30px rgba({color['glow']}, 0.6), 0 12px 40px rgba(0, 0, 0, 0.4)",
                        "transform": "scale(1.05)",
                        "border": f"2px solid rgba({color['glow']}, 0.6)",
                        "background": color["bg"].replace("0.3)", "0.4)").replace("0.2)", "0.3)"),
                    },
                    transition="all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                ),
                rx.text(
                    item["label"],
                    color="white",
                    font_size="0.875rem",
                    font_weight="500",
                    margin_left="1rem",
                    white_space="nowrap",
                    text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                    _hover={
                        "text_shadow": "0 0 8px rgba(255, 255, 255, 0.5)",
                        "transform": "scale(1.05)",
                    }
                ),
                spacing="1",
                align="center",
                justify="start",
            ),
            href=item["route"],
            style={"text-decoration": "none"},
            opacity=rx.cond(VaultSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                VaultSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(20px) scale(0.8)"
            ),
            transition=f"all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) {delay}",
            pointer_events=rx.cond(VaultSpeedDialState.is_open, "auto", "none"),
            on_click=VaultSpeedDialState.toggle_speed_dial,
        )
    
    nav_buttons = [create_nav_item(item, i) for i, item in enumerate(nav_items)]
    
    return rx.box(
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.3)",
            backdrop_filter="blur(2px)",
            z_index="1001",
            opacity=rx.cond(VaultSpeedDialState.is_open, "1", "0"),
            visibility=rx.cond(VaultSpeedDialState.is_open, "visible", "hidden"),
            transition="all 0.3s ease",
            pointer_events=rx.cond(VaultSpeedDialState.is_open, "auto", "none"),
            on_click=VaultSpeedDialState.toggle_speed_dial,
        ),
        
        rx.vstack(
            *reversed(nav_buttons),
            spacing="1",
            position="absolute",
            bottom="5rem",
            left="5rem",
            z_index="1002",
            opacity=rx.cond(VaultSpeedDialState.is_open, "1", "0"),
            transform=rx.cond(
                VaultSpeedDialState.is_open, 
                "translateY(0) scale(1)", 
                "translateY(30px) scale(0.9)"
            ),
            transition="all 0.3s cubic-bezier(0.23, 1, 0.32, 1)",
            pointer_events=rx.cond(VaultSpeedDialState.is_open, "auto", "none"),
        ),
        
        rx.hstack(
            rx.box(
                rx.icon(
                    tag=rx.cond(VaultSpeedDialState.is_open, "x", "lock"),
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background=rx.cond(
                    VaultSpeedDialState.is_open,
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%), linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
                ),
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="relative",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": rx.cond(
                        VaultSpeedDialState.is_open,
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%), linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.2) 100%)",
                        "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)"
                    ),
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
                on_click=VaultSpeedDialState.toggle_speed_dial,
            ),
            rx.text(
                "Vault",
                color="white",
                font_size="1rem",
                font_weight="600",
                margin_left="1rem",
                opacity=rx.cond(VaultSpeedDialState.is_open, "0", "1"),
                transform=rx.cond(VaultSpeedDialState.is_open, "translateX(-10px)", "translateX(0)"),
                transition="all 0.3s ease",
                text_shadow="0 2px 4px rgba(0, 0, 0, 0.8)",
                white_space="nowrap",
                position="relative",
                z_index="1003",
            ),
            spacing="0",
            align="center",
        ),
        
        position="fixed",
        bottom="2rem",
        left="46rem",
        z_index="1003",
    )


class SearchModalState(rx.State):
    """State for the search modal."""
    is_open: bool = False
    search_query: str = ""
    search_results: list[Dict[str, Any]] = []
    selected_projects: list[str] = []
    selected_tags: list[str] = []
    selected_personnel: list[str] = []
    selected_action_types: list[str] = []
    active_tab: str = "assets"  # assets, documents, actions
    available_projects: list[Dict[str, str]] = [
        {"name": "IFMC", "color": "#10b981"},
        {"name": "STARE", "color": "#ef4444"},
        {"name": "STORM", "color": "#8b5cf6"}, 
        {"name": "SHIELD", "color": "#f59e0b"},
        {"name": "TAGM", "color": "#06b6d4"},
        {"name": "MULTI", "color": "#ec4899"}
    ]
    available_tags: list[Dict[str, str]] = [
        {"name": "#ifmc", "color": "#10b981"},
        {"name": "#tagm", "color": "#06b6d4"},
        {"name": "#multi", "color": "#ec4899"},
        {"name": "#storm", "color": "#8b5cf6"},
        {"name": "#shield", "color": "#f59e0b"},
        {"name": "#stare", "color": "#ef4444"},
        {"name": "#process", "color": "#3b82f6"},
        {"name": "#sop", "color": "#8b5cf6"},
        {"name": "#poam", "color": "#f59e0b"},
        {"name": "#guide", "color": "#10b981"},
        {"name": "#bitlocker", "color": "#6366f1"},
        {"name": "#windows", "color": "#0ea5e9"},
        {"name": "#linux", "color": "#22c55e"},
        {"name": "#article", "color": "#64748b"}
    ]
    available_personnel: list[Dict[str, str]] = [
        {"name": "Kyle Hurston", "color": "#10b981"},
        {"name": "Craig Alleman", "color": "#3b82f6"},
        {"name": "Bob Shipp", "color": "#8b5cf6"},
        {"name": "David Felmlee", "color": "#f59e0b"}
    ]
    available_action_types: list[Dict[str, str]] = [
        {"name": "Image Collection", "color": "#10b981"},
        {"name": "DAT Update", "color": "#ef4444"},
        {"name": "Log Collection", "color": "#3b82f6"},
        {"name": "Asset Patching", "color": "#8b5cf6"},
        {"name": "Content Creation", "color": "#f59e0b"}
    ]
    
    def toggle_search_modal(self):
        """Toggle the search modal open/closed state."""
        self.is_open = not self.is_open
        if not self.is_open:
            self.search_query = ""
            self.search_results = []
            self.selected_projects = []
            self.selected_tags = []
            self.selected_personnel = []
            self.selected_action_types = []
            self.active_tab = "assets"
    
    def set_active_tab(self, tab: str):
        """Set the active search tab and refresh results."""
        self.active_tab = tab
        self.search_query = ""
        self.search_results = []
        self.selected_projects = []
        self.selected_tags = []
        self.selected_personnel = []
        self.selected_action_types = []
    
    def toggle_project_filter(self, project: str):
        """Toggle a project filter on/off."""
        if project in self.selected_projects:
            self.selected_projects = [p for p in self.selected_projects if p != project]
        else:
            self.selected_projects = self.selected_projects + [project]
        self.update_search_query(self.search_query)
    
    def toggle_tag_filter(self, tag: str):
        """Toggle a tag filter on/off."""
        if tag in self.selected_tags:
            self.selected_tags = [t for t in self.selected_tags if t != tag]
        else:
            self.selected_tags = self.selected_tags + [tag]
        self.update_search_query(self.search_query)
    
    def toggle_personnel_filter(self, person: str):
        """Toggle a personnel filter on/off."""
        if person in self.selected_personnel:
            self.selected_personnel = [p for p in self.selected_personnel if p != person]
        else:
            self.selected_personnel = self.selected_personnel + [person]
        self.update_search_query(self.search_query)
    
    def toggle_action_type_filter(self, action_type: str):
        """Toggle an action type filter on/off."""
        if action_type in self.selected_action_types:
            self.selected_action_types = [a for a in self.selected_action_types if a != action_type]
        else:
            self.selected_action_types = self.selected_action_types + [action_type]
        self.update_search_query(self.search_query)
    
    def update_search_query(self, query: str):
        """Update the search query and perform search based on active tab."""
        self.search_query = query
        
        if query.strip() or self.selected_projects or self.selected_tags or self.selected_personnel or self.selected_action_types:
            if self.active_tab == "assets":
                # Asset search results
                base_results = [
                    {"name": f"IFMC-Server-{i:02d}", "type": "Server", "location": "Building A", "project": "IFMC", "category": "asset"} 
                    for i in range(1, 3) if query.lower() in f"ifmc-server-{i:02d}".lower() or not query.strip()
                ] + [
                    {"name": f"STARE-Workstation-{i:02d}", "type": "Workstation", "location": "Building B", "project": "STARE", "category": "asset"} 
                    for i in range(1, 3) if query.lower() in f"stare-workstation-{i:02d}".lower() or not query.strip()
                ] + [
                    {"name": f"STORM-Router-{i:02d}", "type": "Network Device", "location": "Data Center", "project": "STORM", "category": "asset"} 
                    for i in range(1, 3) if query.lower() in f"storm-router-{i:02d}".lower() or not query.strip()
                ]
            
            elif self.active_tab == "documents":
                # Document search results with tag-based filtering
                base_results = [
                    {"name": "IFMC Security Policy.pdf", "type": "Policy Document", "location": "Document Library", "tags": ["#ifmc", "#process", "#sop"], "category": "document"} 
                    if query.lower() in "security policy" or not query.strip() else None,
                    {"name": "TAGM Network Diagram.pdf", "type": "Technical Document", "location": "Document Library", "tags": ["#tagm", "#guide", "#windows"], "category": "document"} 
                    if query.lower() in "network diagram" or not query.strip() else None,
                    {"name": "STORM Playbook.md", "type": "Playbook", "location": "Document Library", "tags": ["#storm", "#sop", "#guide"], "category": "document"} 
                    if query.lower() in "playbook" or not query.strip() else None,
                    {"name": "BitLocker Implementation Guide.docx", "type": "Technical Guide", "location": "Document Library", "tags": ["#bitlocker", "#windows", "#guide"], "category": "document"} 
                    if query.lower() in "bitlocker" or not query.strip() else None,
                    {"name": "Linux Server POAM.xlsx", "type": "POAM Document", "location": "Document Library", "tags": ["#linux", "#poam", "#multi"], "category": "document"} 
                    if query.lower() in "linux" or not query.strip() else None,
                    {"name": "SHIELD Process Article.pdf", "type": "Process Article", "location": "Document Library", "tags": ["#shield", "#process", "#article"], "category": "document"} 
                    if query.lower() in "shield" or not query.strip() else None,
                    {"name": "STARE SOP Manual.pdf", "type": "SOP Document", "location": "Document Library", "tags": ["#stare", "#sop", "#process"], "category": "document"} 
                    if query.lower() in "stare" or not query.strip() else None
                ]
                base_results = [r for r in base_results if r is not None]
            
            elif self.active_tab == "actions":
                # Recent actions search results with personnel and action type data
                base_results = [
                    {"name": "DAT Update - IFMC-Server-01", "type": "DAT Update", "location": "2024-01-15 14:30", "project": "IFMC", "personnel": "Kyle Hurston", "category": "action"} 
                    if query.lower() in "dat update" or not query.strip() else None,
                    {"name": "Log Collection - STARE-Workstation-01", "type": "Log Collection", "location": "2024-01-15 13:45", "project": "STARE", "personnel": "Craig Alleman", "category": "action"} 
                    if query.lower() in "log collection" or not query.strip() else None,
                    {"name": "Image Collection - STORM-Router-01", "type": "Image Collection", "location": "2024-01-15 12:20", "project": "STORM", "personnel": "Bob Shipp", "category": "action"} 
                    if query.lower() in "image collection" or not query.strip() else None,
                    {"name": "Asset Patching - SHIELD-Server-02", "type": "Asset Patching", "location": "2024-01-15 11:30", "project": "SHIELD", "personnel": "David Felmlee", "category": "action"} 
                    if query.lower() in "asset patching" or not query.strip() else None,
                    {"name": "Content Creation - TAGM Documentation", "type": "Content Creation", "location": "2024-01-15 10:15", "project": "TAGM", "personnel": "Kyle Hurston", "category": "action"} 
                    if query.lower() in "content creation" or not query.strip() else None
                ]
                base_results = [r for r in base_results if r is not None]
            
            else:
                base_results = []
            
            # Apply filters based on active tab
            if self.active_tab == "assets":
                # Filter by selected projects for assets
                if self.selected_projects:
                    self.search_results = [
                        result for result in base_results 
                        if result["project"] in self.selected_projects
                    ]
                else:
                    self.search_results = base_results
            elif self.active_tab == "documents":
                # Filter by selected tags for documents
                if self.selected_tags:
                    self.search_results = [
                        result for result in base_results 
                        if any(tag in result["tags"] for tag in self.selected_tags)
                    ]
                else:
                    self.search_results = base_results
            elif self.active_tab == "actions":
                # Filter by selected personnel and action types for actions
                filtered_results = base_results
                if self.selected_personnel:
                    filtered_results = [
                        result for result in filtered_results 
                        if result["personnel"] in self.selected_personnel
                    ]
                if self.selected_action_types:
                    filtered_results = [
                        result for result in filtered_results 
                        if result["type"] in self.selected_action_types
                    ]
                self.search_results = filtered_results
            else:
                self.search_results = base_results
        else:
            self.search_results = []


def right_side_buttons() -> rx.Component:
    """Right side buttons with advanced search modal functionality."""
    return rx.fragment(
        # Home button
        rx.link(
            rx.box(
                rx.icon(
                    tag="home",
                    size=24,
                    color="white",
                ),
                width="4rem",
                height="4rem",
                border_radius="50%",
                background="linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)",
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                position="fixed",
                bottom="2rem",
                right="2rem",
                z_index="1003",
                backdrop_filter="blur(20px)",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
                transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
                _hover={
                    "transform": "scale(1.05)",
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)",
                    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
                },
            ),
            href="/dashboard",
        ),
        
        # Search button with modal trigger
        rx.box(
            rx.icon(
                tag="search",
                size=24,
                color="white",
            ),
            width="4rem",
            height="4rem",
            border_radius="50%",
            background="linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)",
            border="2px solid rgba(255, 255, 255, 0.2)",
            display="flex",
            align_items="center",
            justify_content="center",
            cursor="pointer",
            position="fixed",
            bottom="2rem",
            right="7rem",
            z_index="1003",
            backdrop_filter="blur(20px)",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
            transition="all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)",
            _hover={
                "transform": "scale(1.05)",
                "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)",
                "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.4)",
            },
            on_click=SearchModalState.toggle_search_modal,
        ),
        
        # Advanced Search Modal
        rx.cond(
            SearchModalState.is_open,
            rx.box(
                # Backdrop
                rx.box(
                    position="fixed",
                    top="0",
                    left="0",
                    width="100vw",
                    height="100vh",
                    background="linear-gradient(135deg, rgba(0, 0, 0, 0.4) 0%, rgba(20, 20, 30, 0.5) 50%, rgba(0, 0, 0, 0.4) 100%)",
                    backdrop_filter="blur(8px) saturate(120%)",
                    z_index="1500",
                    on_click=SearchModalState.toggle_search_modal,
                ),
                
                # Modal container
                rx.box(
                    # Header with tabs
                    rx.vstack(
                        # Title and close button
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="search", size=24, color="white"),
                                width="3rem",
                                height="3rem",
                                border_radius="50%",
                                background="linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.2) 100%)",
                                border="1px solid rgba(59, 130, 246, 0.4)",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                backdrop_filter="blur(10px)",
                                box_shadow="0 0 30px rgba(59, 130, 246, 0.3)",
                            ),
                            rx.vstack(
                                rx.text("Universal Search", font_size="1.5rem", font_weight="700", color="white"),
                                rx.text("Search assets, documents, and recent actions", font_size="0.875rem", color="rgba(255, 255, 255, 0.7)"),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.box(
                                rx.icon(tag="x", size=18, color="rgba(255, 255, 255, 0.8)"),
                                width="2.5rem",
                                height="2.5rem",
                                border_radius="50%",
                                background="rgba(255, 255, 255, 0.1)",
                                border="1px solid rgba(255, 255, 255, 0.2)",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                on_click=SearchModalState.toggle_search_modal,
                            ),
                            width="100%",
                            align="center",
                            margin_bottom="1.5rem",
                        ),
                        
                        # Tab navigation
                        rx.hstack(
                            # Assets tab
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="server", size=16, color=rx.cond(SearchModalState.active_tab == "assets", "white", "rgba(255, 255, 255, 0.6)")),
                                    rx.text("Assets", font_size="0.875rem", font_weight="500", color=rx.cond(SearchModalState.active_tab == "assets", "white", "rgba(255, 255, 255, 0.6)")),
                                    spacing="2",
                                    align="center",
                                ),
                                padding="0.75rem 1.5rem",
                                border_radius="0.75rem",
                                background=rx.cond(SearchModalState.active_tab == "assets", "linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 100%)", "rgba(255, 255, 255, 0.05)"),
                                border=rx.cond(SearchModalState.active_tab == "assets", "1px solid rgba(16, 185, 129, 0.5)", "1px solid rgba(255, 255, 255, 0.1)"),
                                cursor="pointer",
                                on_click=SearchModalState.set_active_tab("assets"),
                            ),
                            # Documents tab
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="file-text", size=16, color=rx.cond(SearchModalState.active_tab == "documents", "white", "rgba(255, 255, 255, 0.6)")),
                                    rx.text("Documents", font_size="0.875rem", font_weight="500", color=rx.cond(SearchModalState.active_tab == "documents", "white", "rgba(255, 255, 255, 0.6)")),
                                    spacing="2",
                                    align="center",
                                ),
                                padding="0.75rem 1.5rem",
                                border_radius="0.75rem",
                                background=rx.cond(SearchModalState.active_tab == "documents", "linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(37, 99, 235, 0.2) 100%)", "rgba(255, 255, 255, 0.05)"),
                                border=rx.cond(SearchModalState.active_tab == "documents", "1px solid rgba(59, 130, 246, 0.5)", "1px solid rgba(255, 255, 255, 0.1)"),
                                cursor="pointer",
                                on_click=SearchModalState.set_active_tab("documents"),
                            ),
                            # Recent Actions tab
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="activity", size=16, color=rx.cond(SearchModalState.active_tab == "actions", "white", "rgba(255, 255, 255, 0.6)")),
                                    rx.text("Recent Actions", font_size="0.875rem", font_weight="500", color=rx.cond(SearchModalState.active_tab == "actions", "white", "rgba(255, 255, 255, 0.6)")),
                                    spacing="2",
                                    align="center",
                                ),
                                padding="0.75rem 1.5rem",
                                border_radius="0.75rem",
                                background=rx.cond(SearchModalState.active_tab == "actions", "linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(124, 58, 237, 0.2) 100%)", "rgba(255, 255, 255, 0.05)"),
                                border=rx.cond(SearchModalState.active_tab == "actions", "1px solid rgba(139, 92, 246, 0.5)", "1px solid rgba(255, 255, 255, 0.1)"),
                                cursor="pointer",
                                on_click=SearchModalState.set_active_tab("actions"),
                            ),
                            spacing="3",
                            width="100%",
                            justify="start",
                        ),
                        
                        spacing="0",
                        width="100%",
                    ),
                    
                    # Search input
                    rx.box(
                        rx.input(
                            placeholder=rx.cond(
                                SearchModalState.active_tab == "assets",
                                "Search assets, systems, locations, or serial numbers...",
                                rx.cond(
                                    SearchModalState.active_tab == "documents",
                                    "Search policies, playbooks, diagrams, or documentation...",
                                    "Search DAT updates, log collections, or image captures..."
                                )
                            ),
                            value=SearchModalState.search_query,
                            on_change=SearchModalState.update_search_query,
                            width="100%",
                            height="3.5rem",
                            font_size="1rem",
                            color="white",
                            bg="rgba(255, 255, 255, 0.05)",
                            border="1px solid rgba(255, 255, 255, 0.2)",
                            border_radius="1rem",
                            padding="1rem 1.5rem",
                            backdrop_filter="blur(10px)",
                        ),
                        margin="1.5rem 0",
                    ),
                    
                    # Conditional filter chips based on active tab
                    rx.cond(
                        SearchModalState.active_tab == "documents",
                        # Tag chips for Documents tab
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="filter", size=16, color="rgba(255, 255, 255, 0.8)"),
                                rx.text("Search by Tag", font_size="0.875rem", font_weight="600", color="rgba(255, 255, 255, 0.8)"),
                                rx.cond(
                                    SearchModalState.selected_tags.length() > 0,
                                    rx.box(
                                        rx.text(SearchModalState.selected_tags.length(), font_size="0.7rem", color="rgba(59, 130, 246, 0.9)"),
                                        background="rgba(59, 130, 246, 0.2)",
                                        border="1px solid rgba(59, 130, 246, 0.3)",
                                        border_radius="full",
                                        padding="0.2rem 0.5rem",
                                    ),
                                ),
                                spacing="2",
                                align="center",
                                margin_bottom="0.75rem",
                            ),
                            # All tag chips in a single flex container with wrap
                            rx.box(
                                rx.box(rx.text("#ifmc", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#ifmc"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#ifmc"), "#10b98140", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#ifmc"), "2px solid #10b981", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#ifmc"), margin="0.25rem"),
                                rx.box(rx.text("#tagm", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#tagm"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#tagm"), "#06b6d440", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#tagm"), "2px solid #06b6d4", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#tagm"), margin="0.25rem"),
                                rx.box(rx.text("#multi", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#multi"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#multi"), "#ec489940", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#multi"), "2px solid #ec4899", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#multi"), margin="0.25rem"),
                                rx.box(rx.text("#storm", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#storm"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#storm"), "#8b5cf640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#storm"), "2px solid #8b5cf6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#storm"), margin="0.25rem"),
                                rx.box(rx.text("#shield", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#shield"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#shield"), "#f59e0b40", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#shield"), "2px solid #f59e0b", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#shield"), margin="0.25rem"),
                                rx.box(rx.text("#stare", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#stare"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#stare"), "#ef444440", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#stare"), "2px solid #ef4444", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#stare"), margin="0.25rem"),
                                rx.box(rx.text("#process", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#process"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#process"), "#3b82f640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#process"), "2px solid #3b82f6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#process"), margin="0.25rem"),
                                rx.box(rx.text("#sop", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#sop"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#sop"), "#8b5cf640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#sop"), "2px solid #8b5cf6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#sop"), margin="0.25rem"),
                                rx.box(rx.text("#poam", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#poam"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#poam"), "#dc262640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#poam"), "2px solid #dc2626", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#poam"), margin="0.25rem"),
                                rx.box(rx.text("#guide", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#guide"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#guide"), "#059f4040", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#guide"), "2px solid #059f40", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#guide"), margin="0.25rem"),
                                rx.box(rx.text("#bitlocker", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#bitlocker"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#bitlocker"), "#7c2d1240", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#bitlocker"), "2px solid #7c2d12", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#bitlocker"), margin="0.25rem"),
                                rx.box(rx.text("#windows", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#windows"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#windows"), "#0ea5e940", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#windows"), "2px solid #0ea5e9", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#windows"), margin="0.25rem"),
                                rx.box(rx.text("#linux", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#linux"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#linux"), "#f97f0f40", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#linux"), "2px solid #f97f0f", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#linux"), margin="0.25rem"),
                                rx.box(rx.text("#article", font_size="0.8rem", color=rx.cond(SearchModalState.selected_tags.contains("#article"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_tags.contains("#article"), "#6366f140", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_tags.contains("#article"), "2px solid #6366f1", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_tag_filter("#article"), margin="0.25rem"),
                                display="flex",
                                flex_wrap="wrap",
                                width="100%",
                                justify_content="flex_start",
                                align_items="center",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # For other tabs, show project chips or personnel/action type chips
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="filter", size=16, color="rgba(255, 255, 255, 0.8)"),
                                rx.text(
                                    rx.cond(SearchModalState.active_tab == "actions", "Filter by Personnel & Type", "Filter by Project"),
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color="rgba(255, 255, 255, 0.8)",
                                ),
                                spacing="2",
                                align="center",
                                margin_bottom="0.75rem",
                            ),
                            # Project chips for Assets tab or Personnel chips for Actions tab
                            rx.cond(
                                SearchModalState.active_tab == "assets",
                                # All project chips in a single flex container
                                rx.box(
                                    rx.box(rx.text("IFMC", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("IFMC"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("IFMC"), "#10b98140", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("IFMC"), "2px solid #10b981", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("IFMC"), margin="0.25rem", flex="1", min_width="80px"),
                                    rx.box(rx.text("STARE", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("STARE"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("STARE"), "#ef444440", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("STARE"), "2px solid #ef4444", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("STARE"), margin="0.25rem", flex="1", min_width="80px"),
                                    rx.box(rx.text("STORM", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("STORM"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("STORM"), "#8b5cf640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("STORM"), "2px solid #8b5cf6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("STORM"), margin="0.25rem", flex="1", min_width="80px"),
                                    rx.box(rx.text("SHIELD", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("SHIELD"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("SHIELD"), "#f59e0b40", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("SHIELD"), "2px solid #f59e0b", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("SHIELD"), margin="0.25rem", flex="1", min_width="80px"),
                                    rx.box(rx.text("TAGM", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("TAGM"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("TAGM"), "#06b6d440", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("TAGM"), "2px solid #06b6d4", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("TAGM"), margin="0.25rem", flex="1", min_width="80px"),
                                    rx.box(rx.text("MULTI", font_size="0.8rem", color=rx.cond(SearchModalState.selected_projects.contains("MULTI"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_projects.contains("MULTI"), "#ec489940", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_projects.contains("MULTI"), "2px solid #ec4899", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_project_filter("MULTI"), margin="0.25rem", flex="1", min_width="80px"),
                                    display="flex",
                                    flex_wrap="wrap",
                                    width="100%",
                                    justify_content="space-between",
                                    align_items="center",
                                ),
                                # Personnel and Action Type chips for Actions tab
                                rx.vstack(
                                    rx.text("Personnel:", font_size="0.8rem", color="rgba(255, 255, 255, 0.7)", margin_bottom="0.5rem"),
                                    rx.box(
                                        rx.box(rx.text("Kyle Hurston", font_size="0.8rem", color=rx.cond(SearchModalState.selected_personnel.contains("Kyle Hurston"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_personnel.contains("Kyle Hurston"), "#10b98140", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_personnel.contains("Kyle Hurston"), "2px solid #10b981", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_personnel_filter("Kyle Hurston"), margin="0.25rem", flex="1", min_width="110px"),
                                        rx.box(rx.text("Craig Alleman", font_size="0.8rem", color=rx.cond(SearchModalState.selected_personnel.contains("Craig Alleman"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_personnel.contains("Craig Alleman"), "#3b82f640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_personnel.contains("Craig Alleman"), "2px solid #3b82f6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_personnel_filter("Craig Alleman"), margin="0.25rem", flex="1", min_width="110px"),
                                        rx.box(rx.text("Bob Shipp", font_size="0.8rem", color=rx.cond(SearchModalState.selected_personnel.contains("Bob Shipp"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_personnel.contains("Bob Shipp"), "#f59e0b40", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_personnel.contains("Bob Shipp"), "2px solid #f59e0b", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_personnel_filter("Bob Shipp"), margin="0.25rem", flex="1", min_width="110px"),
                                        rx.box(rx.text("David Felmlee", font_size="0.8rem", color=rx.cond(SearchModalState.selected_personnel.contains("David Felmlee"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 1rem", border_radius="full", background=rx.cond(SearchModalState.selected_personnel.contains("David Felmlee"), "#8b5cf640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_personnel.contains("David Felmlee"), "2px solid #8b5cf6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_personnel_filter("David Felmlee"), margin="0.25rem", flex="1", min_width="110px"),
                                        display="flex",
                                        flex_wrap="wrap",
                                        width="100%",
                                        justify_content="space-between",
                                        align_items="center",
                                    ),
                                    rx.text("Action Type:", font_size="0.8rem", color="rgba(255, 255, 255, 0.7)", margin="1rem 0 0.5rem 0"),
                                    # All action type chips in a single flex container
                                    rx.box(
                                        rx.box(rx.text("DAT Update", font_size="0.8rem", color=rx.cond(SearchModalState.selected_action_types.contains("DAT Update"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 0.8rem", border_radius="full", background=rx.cond(SearchModalState.selected_action_types.contains("DAT Update"), "#ef444440", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_action_types.contains("DAT Update"), "2px solid #ef4444", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_action_type_filter("DAT Update"), margin="0.15rem"),
                                        rx.box(rx.text("Log Collection", font_size="0.8rem", color=rx.cond(SearchModalState.selected_action_types.contains("Log Collection"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 0.8rem", border_radius="full", background=rx.cond(SearchModalState.selected_action_types.contains("Log Collection"), "#3b82f640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_action_types.contains("Log Collection"), "2px solid #3b82f6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_action_type_filter("Log Collection"), margin="0.15rem"),
                                        rx.box(rx.text("Image Collection", font_size="0.8rem", color=rx.cond(SearchModalState.selected_action_types.contains("Image Collection"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 0.8rem", border_radius="full", background=rx.cond(SearchModalState.selected_action_types.contains("Image Collection"), "#10b98140", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_action_types.contains("Image Collection"), "2px solid #10b981", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_action_type_filter("Image Collection"), margin="0.15rem"),
                                        rx.box(rx.text("Asset Patching", font_size="0.8rem", color=rx.cond(SearchModalState.selected_action_types.contains("Asset Patching"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 0.8rem", border_radius="full", background=rx.cond(SearchModalState.selected_action_types.contains("Asset Patching"), "#f59e0b40", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_action_types.contains("Asset Patching"), "2px solid #f59e0b", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_action_type_filter("Asset Patching"), margin="0.15rem"),
                                        rx.box(rx.text("Content Creation", font_size="0.8rem", color=rx.cond(SearchModalState.selected_action_types.contains("Content Creation"), "white", "rgba(255, 255, 255, 0.8)")), padding="0.5rem 0.8rem", border_radius="full", background=rx.cond(SearchModalState.selected_action_types.contains("Content Creation"), "#8b5cf640", "rgba(255, 255, 255, 0.08)"), border=rx.cond(SearchModalState.selected_action_types.contains("Content Creation"), "2px solid #8b5cf6", "1px solid rgba(255, 255, 255, 0.2)"), cursor="pointer", on_click=SearchModalState.toggle_action_type_filter("Content Creation"), margin="0.15rem"),
                                        display="flex",
                                        flex_wrap="wrap",
                                        width="100%",
                                        justify_content="flex-start",
                                        align_items="center",
                                    ),
                                    spacing="0",
                                    width="100%",
                                )
                            ),
                            spacing="0",
                            width="100%",
                        )
                    ),
                    
                    # Search results
                    rx.vstack(
                        rx.hstack(
                            rx.text("Search Results", font_size="1rem", font_weight="600", color="white"),
                            rx.box(
                                rx.text(SearchModalState.search_results.length(), font_size="0.75rem", color="rgba(59, 130, 246, 0.9)"),
                                background="rgba(59, 130, 246, 0.2)",
                                border="1px solid rgba(59, 130, 246, 0.3)",
                                border_radius="full",
                                padding="0.25rem 0.75rem",
                            ),
                            rx.spacer(),
                            width="100%",
                            align="center",
                            margin="1rem 0",
                        ),
                        
                        # Results list
                        rx.foreach(
                            SearchModalState.search_results.to(list[Dict[str, Any]]),
                            lambda result: rx.box(
                                rx.hstack(
                                    rx.box(
                                        rx.icon(tag="server", size=20, color="white"),
                                        width="3.5rem",
                                        height="3.5rem",
                                        border_radius="50%",
                                        background="linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(5, 150, 105, 0.2) 100%)",
                                        border="1px solid rgba(16, 185, 129, 0.4)",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center",
                                    ),
                                    rx.vstack(
                                        rx.text(result["name"], font_size="1rem", font_weight="600", color="white"),
                                        rx.text(result["type"], font_size="0.875rem", color="rgba(255, 255, 255, 0.7)"),
                                        spacing="0",
                                        align="start",
                                    ),
                                    rx.spacer(),
                                    rx.text(result["location"], font_size="0.8rem", color="rgba(255, 255, 255, 0.6)"),
                                    spacing="3",
                                    align="center",
                                    width="100%",
                                ),
                                padding="1rem",
                                background="rgba(255, 255, 255, 0.05)",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="0.75rem",
                                cursor="pointer",
                                _hover={"background": "rgba(255, 255, 255, 0.1)"},
                                margin_bottom="0.5rem",
                            )
                        ),
                        
                        width="100%",
                        max_height="300px",
                        overflow_y="auto",
                    ),
                    
                    # Modal styling
                    position="fixed",
                    top="50%",
                    left="50%",
                    transform="translate(-50%, -50%)",
                    width="90%",
                    max_width="700px",
                    background="rgba(15, 15, 20, 0.85)",
                    border="1px solid rgba(255, 255, 255, 0.2)",
                    border_radius="1.5rem",
                    backdrop_filter="blur(40px) saturate(180%)",
                    box_shadow="0 25px 50px rgba(0, 0, 0, 0.5)",
                    z_index="1600",
                    padding="2rem",
                ),
            )
        ),
    )