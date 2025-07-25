"""Enhanced native editor component for Reflex."""
import reflex as rx

def enhanced_editor(
    value: str,
    on_change,
    placeholder: str = "Start typing your markdown here...",
    height: str = "auto",
    **props
) -> rx.Component:
    """Create an enhanced native editor with markdown support.
    
    This uses Reflex's native textarea with enhanced styling to avoid
    third-party component integration issues.
    """
    return rx.box(
        rx.text_area(
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            style={
                "width": "100%",
                "height": "100%",
                "min_height": "600px",
                "background": "rgba(0, 0, 0, 0.7)",
                "color": "rgba(255, 255, 255, 0.95)",
                "border": "none",
                "padding": "2rem",
                "font_size": "16px",
                "line_height": "1.8",
                "font_family": "ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace",
                "resize": "none",
                "outline": "none",
                "_placeholder": {
                    "color": "rgba(156, 163, 175, 0.5)",
                },
                "_focus": {
                    "outline": "none",
                    "box_shadow": "inset 0 0 0 2px rgba(99, 102, 241, 0.3)",
                },
                # Scrollbar styling
                "scrollbar_width": "thin",
                "scrollbar_color": "rgba(255, 255, 255, 0.2) transparent",
                "_webkit_scrollbar": {
                    "width": "8px",
                },
                "_webkit_scrollbar_track": {
                    "background": "transparent",
                },
                "_webkit_scrollbar_thumb": {
                    "background": "rgba(255, 255, 255, 0.2)",
                    "border_radius": "4px",
                },
                "_webkit_scrollbar_thumb_hover": {
                    "background": "rgba(255, 255, 255, 0.3)",
                },
            },
            **props
        ),
        style={
            "width": "100%",
            "height": height,
            "background": "rgba(0, 0, 0, 0.3)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": "12px",
            "overflow": "hidden",
        }
    )