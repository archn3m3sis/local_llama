"""Shared styles for dashboard components."""

# Hover state for cards
CARD_HOVER_STYLE = {
    "background": "linear-gradient(135deg, rgba(31, 31, 31, 0.4) 0%, rgba(45, 45, 45, 0.3) 50%, rgba(31, 31, 31, 0.4) 100%)",
    "border_color": "rgba(255, 255, 255, 0.15)",
    "transform": "translateY(-2px)",
    "box_shadow": "0 12px 40px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08), inset 0 -1px 0 rgba(0, 0, 0, 0.2)",
}

# Dark grey gradient ultra-glassmorphic card style
CARD_STYLE = {
    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 50%, rgba(255, 255, 255, 0.05) 100%)",
    "backdrop_filter": "blur(16px) saturate(180%) brightness(0.9)",
    "-webkit-backdrop-filter": "blur(16px) saturate(180%) brightness(0.9)",
    "border": "1px solid rgba(255, 255, 255, 0.1)",
    "border_radius": "12px",
    "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.06), inset 0 -1px 0 rgba(0, 0, 0, 0.1)",
    "transition": "all 0.3s ease",
    "_hover": CARD_HOVER_STYLE,
}

def get_card_style_with_hover(hover_color: str = None):
    """Get card style with optional hover color accent."""
    base_style = CARD_STYLE.copy()
    hover_style = CARD_HOVER_STYLE.copy()
    
    if hover_color:
        hover_style["border_color"] = hover_color
        hover_style["box_shadow"] = f"{hover_style['box_shadow']}, 0 0 20px {hover_color}20"
    
    base_style["_hover"] = hover_style
    return base_style