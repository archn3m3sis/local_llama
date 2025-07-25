"""Playbook page with unique visual components and markdown integration."""
import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.shared_styles import CARD_STYLE
from ..states.playbook_state import PlaybookState


def floating_card(
    title: str,
    description: str,
    icon: str,
    count: int,
    color: str,
    on_click: callable = None
) -> rx.Component:
    """Create a floating card with hover effects and animations."""
    return rx.box(
        rx.vstack(
            # Icon container with glow effect
            rx.box(
                rx.icon(
                    tag=icon,
                    size=32,
                    style={
                        "color": color,
                        "filter": f"drop-shadow(0 0 20px {color})",
                    }
                ),
                style={
                    "width": "64px",
                    "height": "64px",
                    "background": f"radial-gradient(circle at center, {color}20 0%, transparent 70%)",
                    "display": "flex",
                    "align_items": "center",
                    "justify_content": "center",
                    "border_radius": "50%",
                    "animation": "pulse 3s ease-in-out infinite",
                }
            ),
            
            # Title and count
            rx.hstack(
                rx.text(
                    title,
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_size": "1.25rem",
                        "font_weight": "700",
                        "letter_spacing": "-0.025em",
                    }
                ),
                rx.spacer(),
                rx.text(
                    str(count),
                    style={
                        "color": color,
                        "font_size": "2rem",
                        "font_weight": "800",
                        "filter": f"drop-shadow(0 0 10px {color}40)",
                    }
                ),
                width="100%",
                align="center",
            ),
            
            # Description
            rx.text(
                description,
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "line_height": "1.5",
                }
            ),
            
            # View all link
            rx.hstack(
                rx.text(
                    "View all",
                    style={
                        "color": color,
                        "font_size": "0.875rem",
                        "font_weight": "500",
                    }
                ),
                rx.icon(
                    tag="arrow-right",
                    size=16,
                    style={"color": color}
                ),
                spacing="2",
                align="center",
                style={
                    "cursor": "pointer",
                    "opacity": "0",
                    "transform": "translateX(-10px)",
                    "transition": "all 0.3s ease",
                }
            ),
            
            spacing="4",
            width="100%",
        ),
        on_click=on_click,
        style={
            **CARD_STYLE,
            "padding": "2rem",
            "cursor": "pointer",
            "position": "relative",
            "overflow": "hidden",
            "transform": "translateY(0)",
            "transition": "all 0.3s ease",
            "_before": {
                "content": '""',
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": f"linear-gradient(135deg, {color}10 0%, transparent 50%)",
                "opacity": "0",
                "transition": "opacity 0.3s ease",
            },
            "_hover": {
                "transform": "translateY(-4px)",
                "box_shadow": f"0 20px 40px {color}20",
                "_before": {
                    "opacity": "1",
                },
                "& > div > div:last-child": {
                    "opacity": "1",
                    "transform": "translateX(0)",
                }
            }
        }
    )


def recent_playbook_item(playbook: dict) -> rx.Component:
    """Create a recent playbook list item with timeline indicator."""
    return rx.hstack(
        # Timeline dot and line
        rx.box(
            rx.box(
                style={
                    "width": "12px",
                    "height": "12px",
                    "background": rx.cond(
                        playbook["status"] == "published",
                        "#10b981",
                        "#f59e0b"
                    ),
                    "border_radius": "50%",
                    "box_shadow": rx.cond(
                        playbook["status"] == "published",
                        "0 0 0 4px #10b98130",
                        "0 0 0 4px #f59e0b30"
                    ),
                }
            ),
            style={
                "position": "relative",
                "_after": {
                    "content": '""',
                    "position": "absolute",
                    "top": "12px",
                    "left": "50%",
                    "transform": "translateX(-50%)",
                    "width": "2px",
                    "height": "100%",
                    "background": "rgba(255, 255, 255, 0.1)",
                }
            }
        ),
        
        # Content
        rx.vstack(
            rx.hstack(
                rx.text(
                    playbook["title"],
                    style={
                        "color": "rgba(255, 255, 255, 0.95)",
                        "font_weight": "600",
                        "font_size": "1rem",
                    }
                ),
                rx.box(
                    rx.text(
                        playbook["category"],
                        style={
                            "color": "rgba(255, 255, 255, 0.8)",
                            "font_size": "0.75rem",
                            "font_weight": "500",
                        }
                    ),
                    style={
                        "padding": "0.25rem 0.75rem",
                        "background": "rgba(99, 102, 241, 0.2)",
                        "border": "1px solid rgba(99, 102, 241, 0.3)",
                        "border_radius": "9999px",
                    }
                ),
                rx.spacer(),
                rx.text(
                    playbook["updated"],
                    style={
                        "color": "rgba(156, 163, 175, 0.6)",
                        "font_size": "0.875rem",
                    }
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                playbook["description"],
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "0.875rem",
                    "line_height": "1.5",
                }
            ),
            spacing="2",
            width="100%",
            style={"padding_bottom": "1.5rem"}
        ),
        
        spacing="4",
        width="100%",
        align="start",
    )


def search_box() -> rx.Component:
    """Create an advanced search box with category filters."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Search input with icon
                rx.box(
                    rx.icon(
                        tag="search",
                        size=20,
                        style={
                            "position": "absolute",
                            "left": "1rem",
                            "top": "50%",
                            "transform": "translateY(-50%)",
                            "color": "rgba(156, 163, 175, 0.5)",
                        }
                    ),
                    rx.input(
                        placeholder="Search playbooks by title, content, or tags...",
                        value=PlaybookState.search_query,
                        on_change=PlaybookState.set_search_query,
                        style={
                            "width": "100%",
                            "padding": "1rem 1rem 1rem 3rem",
                            "height": "56px",
                            "background": "rgba(255, 255, 255, 0.03)",
                            "border": "2px solid transparent",
                            "border_radius": "12px",
                            "color": "rgba(255, 255, 255, 0.95)",
                            "font_size": "1.125rem",
                            "transition": "all 0.3s ease",
                            "_placeholder": {
                                "color": "rgba(156, 163, 175, 0.4)",
                            },
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.05)",
                            },
                            "_focus": {
                                "outline": "none",
                                "border_color": "rgba(99, 102, 241, 0.5)",
                                "background": "rgba(255, 255, 255, 0.05)",
                                "box_shadow": "0 0 0 4px rgba(99, 102, 241, 0.1)",
                            },
                        }
                    ),
                    style={
                        "position": "relative",
                        "flex": "1",
                    }
                ),
                
                # Button group
                rx.hstack(
                    # Open Editor View button
                    rx.button(
                        rx.icon(tag="file-text", size=20),
                        "Editor View",
                        on_click=lambda: rx.redirect("/playbook/editor"),
                        style={
                            "padding": "1rem 1.5rem",
                            "height": "56px",
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "border_radius": "12px",
                            "color": "rgba(255, 255, 255, 0.9)",
                            "font_size": "1rem",
                            "font_weight": "500",
                            "cursor": "pointer",
                            "display": "flex",
                            "align_items": "center",
                            "gap": "0.5rem",
                            "transition": "all 0.3s ease",
                            "backdrop_filter": "blur(10px)",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.1)",
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 4px 15px rgba(255, 255, 255, 0.1)",
                            }
                        }
                    ),
                    
                    # Browse Templates button
                    rx.button(
                        rx.icon(tag="layout-template", size=20),
                        "Templates",
                        on_click=PlaybookState.open_template_gallery,
                        style={
                            "padding": "1rem 1.5rem",
                            "height": "56px",
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "border_radius": "12px",
                            "color": "rgba(255, 255, 255, 0.9)",
                            "font_size": "1rem",
                            "font_weight": "500",
                            "cursor": "pointer",
                            "display": "flex",
                            "align_items": "center",
                            "gap": "0.5rem",
                            "transition": "all 0.3s ease",
                            "backdrop_filter": "blur(10px)",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.1)",
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 4px 15px rgba(255, 255, 255, 0.1)",
                            }
                        }
                    ),
                    
                    # Create new button (primary action)
                    rx.button(
                        rx.icon(tag="plus", size=20),
                        "Create Playbook",
                        on_click=PlaybookState.open_create_modal,
                        style={
                            "padding": "1rem 2rem",
                            "height": "56px",
                            "background": "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)",
                            "border": "none",
                            "border_radius": "12px",
                            "color": "white",
                            "font_size": "1rem",
                            "font_weight": "600",
                            "cursor": "pointer",
                            "display": "flex",
                            "align_items": "center",
                            "gap": "0.5rem",
                            "transition": "all 0.3s ease",
                            "box_shadow": "0 4px 15px rgba(99, 102, 241, 0.3)",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 8px 25px rgba(99, 102, 241, 0.4)",
                            }
                        }
                    ),
                    spacing="3",
                ),
                width="100%",
                spacing="4",
            ),
            
            # Category filter pills
            rx.hstack(
                rx.foreach(
                    PlaybookState.categories,
                    lambda cat: rx.box(
                        rx.text(
                            cat,
                            style={
                                "color": rx.cond(
                                    PlaybookState.selected_category == cat,
                                    "white",
                                    "rgba(156, 163, 175, 0.8)"
                                ),
                                "font_size": "0.875rem",
                                "font_weight": "500",
                            }
                        ),
                        on_click=lambda: PlaybookState.set_selected_category(cat),
                        style={
                            "padding": "0.5rem 1.25rem",
                            "background": rx.cond(
                                PlaybookState.selected_category == cat,
                                "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": rx.cond(
                                PlaybookState.selected_category == cat,
                                "1px solid transparent",
                                "1px solid rgba(255, 255, 255, 0.1)"
                            ),
                            "border_radius": "9999px",
                            "cursor": "pointer",
                            "transition": "all 0.2s ease",
                            "_hover": {
                                "background": rx.cond(
                                    PlaybookState.selected_category == cat,
                                    "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)",
                                    "rgba(255, 255, 255, 0.08)"
                                ),
                                "transform": "translateY(-1px)",
                            }
                        }
                    )
                ),
                spacing="3",
                wrap="wrap",
            ),
            spacing="4",
        ),
        style={
            **CARD_STYLE,
            "padding": "2rem",
            "background": "linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(79, 70, 229, 0.02) 100%)",
            "border": "1px solid rgba(99, 102, 241, 0.2)",
        }
    )


def Playbook() -> rx.Component:
    """Main playbook page with unique visual design."""
    return rx.vstack(
        # Title with animated background
        rx.box(
            metallic_title("IAMS Playbook Library"),
            rx.text(
                "Standardized procedures and runbooks for industrial asset management",
                style={
                    "color": "rgba(156, 163, 175, 0.8)",
                    "font_size": "1.125rem",
                    "text_align": "center",
                    "margin_top": "-1rem",
                }
            ),
            style={
                "position": "relative",
                "padding": "2rem 0 3rem 0",
                "_before": {
                    "content": '""',
                    "position": "absolute",
                    "top": "-50%",
                    "left": "-10%",
                    "width": "120%",
                    "height": "200%",
                    "background": "radial-gradient(ellipse at center, rgba(99, 102, 241, 0.1) 0%, transparent 70%)",
                    "animation": "float 20s ease-in-out infinite",
                    "z_index": "-1",
                }
            }
        ),
        
        # Search and filters - wrapped to align with carousel
        rx.box(
            search_box(),
            style={
                "padding": "0 60px",  # Match carousel padding
                "width": "100%",
            }
        ),
        
        # Stats cards carousel
        rx.box(
            rx.hstack(
                # Left scroll button
                rx.button(
                    rx.icon(tag="chevron-left", size=24),
                    on_click=PlaybookState.scroll_carousel_left,
                    style={
                        "position": "absolute",
                        "left": "0",
                        "top": "50%",
                        "transform": "translateY(-50%)",
                        "z_index": "10",
                        "background": "linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.6) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "50%",
                        "width": "48px",
                        "height": "48px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "cursor": "pointer",
                        "backdrop_filter": "blur(10px)",
                        "transition": "all 0.3s ease",
                        "_hover": {
                            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%)",
                            "transform": "translateY(-50%) scale(1.1)",
                        },
                        "_disabled": {
                            "opacity": "0.3",
                            "cursor": "not-allowed",
                        }
                    }
                ),
                
                # Scrollable container
                rx.box(
                    rx.hstack(
                        floating_card(
                            title="Incident Response",
                            description="Quick response procedures for security incidents",
                            icon="shield-alert",
                            count=24,
                            color="#ef4444",
                            on_click=lambda: PlaybookState.filter_by_category("Incident Response")
                        ),
                        floating_card(
                            title="Maintenance",
                            description="Routine maintenance and update procedures",
                            icon="wrench",
                            count=18,
                            color="#10b981",
                            on_click=lambda: PlaybookState.filter_by_category("Maintenance")
                        ),
                        floating_card(
                            title="Compliance",
                            description="Regulatory compliance and audit procedures",
                            icon="clipboard-check",
                            count=32,
                            color="#f59e0b",
                            on_click=lambda: PlaybookState.filter_by_category("Compliance")
                        ),
                        floating_card(
                            title="Emergency",
                            description="Emergency response and disaster recovery",
                            icon="siren",
                            count=12,
                            color="#8b5cf6",
                            on_click=lambda: PlaybookState.filter_by_category("Emergency")
                        ),
                        floating_card(
                            title="Security",
                            description="Security protocols and access control procedures",
                            icon="lock",
                            count=28,
                            color="#06b6d4",
                            on_click=lambda: PlaybookState.filter_by_category("Security")
                        ),
                        floating_card(
                            title="Operations",
                            description="Daily operational procedures and checklists",
                            icon="settings",
                            count=45,
                            color="#ec4899",
                            on_click=lambda: PlaybookState.filter_by_category("Operations")
                        ),
                        floating_card(
                            title="Training",
                            description="Training materials and onboarding procedures",
                            icon="graduation-cap",
                            count=15,
                            color="#14b8a6",
                            on_click=lambda: PlaybookState.filter_by_category("Training")
                        ),
                        spacing="4",
                        padding="0 60px",  # Padding for scroll buttons
                        style={
                            "min_width": "fit-content",
                        }
                    ),
                    id="playbook-carousel",
                    style={
                        "overflow_x": "auto",
                        "overflow_y": "hidden",
                        "scroll_behavior": "smooth",
                        "width": "100%",
                        "scrollbar_width": "thin",
                        "scrollbar_color": "rgba(255, 255, 255, 0.2) rgba(255, 255, 255, 0.05)",
                        "_webkit_scrollbar": {
                            "height": "8px",
                        },
                        "_webkit_scrollbar_track": {
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border_radius": "4px",
                        },
                        "_webkit_scrollbar_thumb": {
                            "background": "rgba(255, 255, 255, 0.2)",
                            "border_radius": "4px",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.3)",
                            }
                        },
                    }
                ),
                
                # Right scroll button
                rx.button(
                    rx.icon(tag="chevron-right", size=24),
                    on_click=PlaybookState.scroll_carousel_right,
                    style={
                        "position": "absolute",
                        "right": "0",
                        "top": "50%",
                        "transform": "translateY(-50%)",
                        "z_index": "10",
                        "background": "linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0.6) 100%)",
                        "border": "1px solid rgba(255, 255, 255, 0.1)",
                        "border_radius": "50%",
                        "width": "48px",
                        "height": "48px",
                        "display": "flex",
                        "align_items": "center",
                        "justify_content": "center",
                        "cursor": "pointer",
                        "backdrop_filter": "blur(10px)",
                        "transition": "all 0.3s ease",
                        "_hover": {
                            "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%)",
                            "transform": "translateY(-50%) scale(1.1)",
                        },
                        "_disabled": {
                            "opacity": "0.3",
                            "cursor": "not-allowed",
                        }
                    }
                ),
                width="100%",
                position="relative",
            ),
            style={
                "position": "relative",
                "width": "100%",
                "padding": "2rem 0",
            }
        ),
        
        # Content area with two columns - wrapped to align with carousel
        rx.box(
            rx.hstack(
                # Recent playbooks with timeline
                rx.box(
                rx.vstack(
                    rx.text(
                        "Recent Playbooks",
                        style={
                            "color": "rgba(255, 255, 255, 0.95)",
                            "font_size": "1.25rem",
                            "font_weight": "700",
                        }
                    ),
                    rx.box(
                        rx.foreach(
                            PlaybookState.recent_playbooks,
                            recent_playbook_item
                        ),
                        style={"width": "100%"}
                    ),
                    spacing="4",
                    width="100%",
                ),
                style={
                    **CARD_STYLE,
                    "padding": "2rem",
                    "flex": "2",
                }
            ),
            
            # Quick actions sidebar
            rx.box(
                rx.vstack(
                    rx.text(
                        "Quick Actions",
                        style={
                            "color": "rgba(255, 255, 255, 0.95)",
                            "font_size": "1.25rem",
                            "font_weight": "700",
                        }
                    ),
                    
                    # Template gallery
                    rx.box(
                        rx.vstack(
                            rx.icon(
                                tag="layout-template",
                                size=24,
                                style={"color": "#06b6d4"}
                            ),
                            rx.text(
                                "Browse Templates",
                                style={
                                    "color": "rgba(255, 255, 255, 0.9)",
                                    "font_weight": "600",
                                }
                            ),
                            rx.text(
                                "Start with pre-built playbook templates",
                                style={
                                    "color": "rgba(156, 163, 175, 0.8)",
                                    "font_size": "0.875rem",
                                    "text_align": "center",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        on_click=PlaybookState.open_template_gallery,
                        style={
                            "padding": "1.5rem",
                            "background": "linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
                            "border": "1px solid rgba(6, 182, 212, 0.3)",
                            "border_radius": "12px",
                            "cursor": "pointer",
                            "transition": "all 0.3s ease",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 8px 20px rgba(6, 182, 212, 0.2)",
                            }
                        }
                    ),
                    
                    # Import/Export
                    rx.box(
                        rx.vstack(
                            rx.icon(
                                tag="cloud-download",
                                size=24,
                                style={"color": "#10b981"}
                            ),
                            rx.text(
                                "Import/Export",
                                style={
                                    "color": "rgba(255, 255, 255, 0.9)",
                                    "font_weight": "600",
                                }
                            ),
                            rx.text(
                                "Backup or share playbook collections",
                                style={
                                    "color": "rgba(156, 163, 175, 0.8)",
                                    "font_size": "0.875rem",
                                    "text_align": "center",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        on_click=PlaybookState.open_import_export,
                        style={
                            "padding": "1.5rem",
                            "background": "linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%)",
                            "border": "1px solid rgba(16, 185, 129, 0.3)",
                            "border_radius": "12px",
                            "cursor": "pointer",
                            "transition": "all 0.3s ease",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 8px 20px rgba(16, 185, 129, 0.2)",
                            }
                        }
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                style={
                    **CARD_STYLE,
                    "padding": "2rem",
                    "flex": "1",
                }
            ),
            
                spacing="4",
                width="100%",
                align="start",
            ),
            style={
                "padding": "0 60px",  # Match carousel padding
                "width": "100%",
            }
        ),
        
        # CSS for animations
        rx.html("""
        <style>
        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(1deg); }
            66% { transform: translateY(10px) rotate(-1deg); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.1); opacity: 1; }
        }
        </style>
        """),
        
        spacing="6",
        width="100%",
        padding="3em",
        padding_top="4em",
        padding_bottom="8em",
        position="absolute",
        top="0",
        left="0",
        right="0",
        bottom="0",
        overflow_y="auto",
        z_index="10",
        on_mount=PlaybookState.load_playbooks,
    )