import reflex as rx

def metallic_text(text: str, size: str = "8") -> rx.Component:
    """
    Clean luminant white text like the landing page hero.
    Simple, elegant, and professional.
    """
    return rx.text(
        text,
        font_weight="800",
        line_height="1.1",
        letter_spacing="-0.02em",
        color="white",
        background="linear-gradient(180deg, #ffffff 0%, #f8fafc 25%, #e2e8f0 50%, #cbd5e1 75%, #94a3b8 100%)",
        background_clip="text",
        style={
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "font_size": "clamp(1.25rem, 3.5vw, 2.5rem)",
            "background": "linear-gradient(180deg, #ffffff 0%, #f8fafc 25%, #e2e8f0 50%, #cbd5e1 75%, #94a3b8 100%)",
            "-webkit-background-clip": "text",
            "background-clip": "text",
            "-webkit-text-fill-color": "transparent",
            "text-shadow": "0 0 20px rgba(255, 255, 255, 0.2)",
            "position": "relative",
            "z-index": "10",
        },
        text_align="left",
        margin_bottom="0.5em",
    )

def metallic_title(text: str) -> rx.Component:
    """
    Creates a massive metallic title with enhanced effects, positioned to the left
    """
    return rx.vstack(
        metallic_text(text, "9xl"),  # Much bigger - massive header
        rx.box(
            height="4px",
            width="750px",  # Extended the line length
            background="linear-gradient(90deg, #F0F0F0 0%, #E8E8E8 10%, #D5D5D5 20%, #C8C8C8 30%, #B8B8B8 50%, rgba(180,180,180,0.8) 70%, rgba(160,160,160,0.5) 85%, transparent 100%)",
            border_radius="2px",
            box_shadow="0 0 20px rgba(255,255,255,0.4), 0 3px 6px rgba(0,0,0,0.2)",
            margin_top="0.1em",
            margin_left="-100px",  # Start from off-screen left
            position="relative",
        ),
        align="start",
        spacing="0",
        margin_bottom="2em",
        width="100%",
    )