"""WYSIWYG Playbook Editor with inline markdown rendering using CodeMirror."""
import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.shared_styles import CARD_STYLE
from ..components.enhanced_editor import enhanced_editor
from ..states.playbook_editor_state import PlaybookEditorState


def editor_toolbar() -> rx.Component:
    """Create the editor toolbar with formatting options."""
    button_style = {
        "width": "40px",
        "height": "40px",
        "padding": "0",
        "background": "rgba(255, 255, 255, 0.05)",
        "border": "1px solid rgba(255, 255, 255, 0.1)",
        "border_radius": "8px",
        "color": "rgba(255, 255, 255, 0.8)",
        "cursor": "pointer",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
        "transition": "all 0.2s ease",
        "_hover": {
            "background": "rgba(255, 255, 255, 0.1)",
            "color": "white",
            "transform": "translateY(-1px)",
        }
    }
    
    separator_style = {
        "width": "1px",
        "height": "24px",
        "background": "rgba(255, 255, 255, 0.2)",
        "margin": "0 0.5rem",
    }
    
    return rx.hstack(
        # Text formatting - only show in edit mode
        rx.cond(
            ~PlaybookEditorState.preview_mode,
            rx.fragment(
                rx.hstack(
                    rx.button(
                        rx.icon(tag="bold", size=18),
                        on_click=PlaybookEditorState.format_bold,
                        style=button_style,
                    ),
                    rx.button(
                        rx.icon(tag="italic", size=18),
                        on_click=PlaybookEditorState.format_italic,
                        style=button_style,
                    ),
                    rx.button(
                        rx.icon(tag="code", size=18),
                        on_click=PlaybookEditorState.format_code,
                        style=button_style,
                    ),
                    spacing="2",
                ),
                rx.box(style=separator_style),
                rx.hstack(
                    rx.button(
                        rx.text("H1", style={"font_weight": "700", "font_size": "14px"}),
                        on_click=lambda: PlaybookEditorState.format_header(1),
                        style=button_style,
                    ),
                    rx.button(
                        rx.text("H2", style={"font_weight": "600", "font_size": "14px"}),
                        on_click=lambda: PlaybookEditorState.format_header(2),
                        style=button_style,
                    ),
                    rx.button(
                        rx.text("H3", style={"font_weight": "500", "font_size": "14px"}),
                        on_click=lambda: PlaybookEditorState.format_header(3),
                        style=button_style,
                    ),
                    spacing="2",
                ),
                rx.box(style=separator_style),
                rx.hstack(
                    rx.button(
                        rx.icon(tag="list", size=18),
                        on_click=PlaybookEditorState.format_bullet_list,
                        style=button_style,
                    ),
                    rx.button(
                        rx.icon(tag="list-ordered", size=18),
                        on_click=PlaybookEditorState.format_numbered_list,
                        style=button_style,
                    ),
                    rx.button(
                        rx.icon(tag="quote", size=18),
                        on_click=PlaybookEditorState.format_blockquote,
                        style=button_style,
                    ),
                    spacing="2",
                ),
                rx.box(style=separator_style),
            ),
        ),
        
        rx.spacer(),
        
        # View toggle button
        rx.button(
            rx.icon(
                tag=rx.cond(
                    PlaybookEditorState.preview_mode,
                    "pencil",
                    "eye"
                ),
                size=18
            ),
            rx.text(
                rx.cond(
                    PlaybookEditorState.preview_mode,
                    "Edit",
                    "Preview"
                ),
                size="2"
            ),
            on_click=PlaybookEditorState.toggle_preview,
            style={
                **button_style,
                "width": "auto",
                "padding": "0 1rem",
                "background": "rgba(99, 102, 241, 0.2)",
                "border_color": "rgba(99, 102, 241, 0.5)",
            }
        ),
        
        style={
            **CARD_STYLE,
            "padding": "1rem",
            "margin_bottom": "1rem",
            "backdrop_filter": "blur(10px)",
        },
        width="100%",
        align="center",
    )


def editor_content() -> rx.Component:
    """Create the main editor content area with enhanced editor."""
    return rx.box(
        # Show editor or preview based on mode
        rx.cond(
            PlaybookEditorState.preview_mode,
            # Preview mode - render markdown
            rx.box(
                rx.markdown(
                    PlaybookEditorState.content,
                    style={
                        "width": "100%",
                        "color": "rgba(255, 255, 255, 0.95)",
                        "padding": "2rem",
                        "font_size": "16px",
                        "line_height": "1.8",
                        # Markdown specific styles
                        "& h1": {
                            "font_size": "2.25rem",
                            "font_weight": "700",
                            "margin": "1.5rem 0 1rem 0",
                            "color": "#818cf8",  # Purple/indigo
                            "text_shadow": "0 0 20px rgba(129, 140, 248, 0.5)",
                        },
                        "& h2": {
                            "font_size": "1.75rem",
                            "font_weight": "600",
                            "margin": "1.25rem 0 0.75rem 0",
                            "color": "#34d399",  # Emerald green
                            "text_shadow": "0 0 15px rgba(52, 211, 153, 0.4)",
                        },
                        "& h3": {
                            "font_size": "1.5rem",
                            "font_weight": "500",
                            "margin": "1rem 0 0.5rem 0",
                            "color": "#60a5fa",  # Sky blue
                            "text_shadow": "0 0 10px rgba(96, 165, 250, 0.3)",
                        },
                        "& h4": {
                            "font_size": "1.25rem",
                            "font_weight": "500",
                            "margin": "0.75rem 0 0.5rem 0",
                            "color": "#fbbf24",  # Amber
                            "text_shadow": "0 0 8px rgba(251, 191, 36, 0.3)",
                        },
                        "& h5": {
                            "font_size": "1.1rem",
                            "font_weight": "500",
                            "margin": "0.75rem 0 0.5rem 0",
                            "color": "#f472b6",  # Pink
                            "text_shadow": "0 0 6px rgba(244, 114, 182, 0.3)",
                        },
                        "& h6": {
                            "font_size": "1rem",
                            "font_weight": "600",
                            "margin": "0.75rem 0 0.5rem 0",
                            "color": "#c084fc",  # Purple
                            "text_shadow": "0 0 5px rgba(192, 132, 252, 0.3)",
                        },
                        "& p": {
                            "margin": "0.75rem 0",
                            "color": "rgba(209, 213, 219, 0.95)",  # Light gray
                        },
                        "& code": {
                            "background": "rgba(99, 102, 241, 0.15)",
                            "padding": "0.2rem 0.4rem",
                            "border_radius": "4px",
                            "font_family": "monospace",
                            "font_size": "0.9em",
                            "color": "#c7d2fe",
                            "border": "1px solid rgba(99, 102, 241, 0.3)",
                        },
                        "& pre": {
                            "background": "rgba(0, 0, 0, 0.5)",
                            "padding": "1rem",
                            "border_radius": "8px",
                            "overflow_x": "auto",
                            "margin": "1rem 0",
                        },
                        "& blockquote": {
                            "border_left": "4px solid rgba(99, 102, 241, 0.5)",
                            "padding_left": "1rem",
                            "margin": "1rem 0",
                            "color": "rgba(199, 210, 254, 0.9)",
                            "background": "rgba(99, 102, 241, 0.05)",
                            "padding": "1rem",
                            "border_radius": "0 8px 8px 0",
                            "font_style": "italic",
                        },
                        "& a": {
                            "color": "#818cf8",
                            "text_decoration": "underline",
                            "_hover": {
                                "color": "#6366f1",
                            },
                        },
                        "& ul, & ol": {
                            "margin": "0.75rem 0",
                            "padding_left": "2rem",
                        },
                        "& li": {
                            "margin": "0.25rem 0",
                            "color": "rgba(209, 213, 219, 0.95)",  # Same gray as paragraphs
                        },
                        "& table": {
                            "width": "100%",
                            "border_collapse": "collapse",
                            "margin": "1rem 0",
                        },
                        "& th": {
                            "background": "rgba(99, 102, 241, 0.1)",
                            "padding": "0.75rem",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "text_align": "left",
                            "font_weight": "600",
                        },
                        "& td": {
                            "padding": "0.75rem",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "color": "rgba(209, 213, 219, 0.95)",  # Same gray as paragraphs
                        },
                    }
                ),
                style={
                    "min_height": "500px",
                    "background": "rgba(0, 0, 0, 0.3)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "12px",
                    "padding_bottom": "2rem",  # Extra padding at bottom
                    # Custom scrollbar
                    "scrollbar_width": "thin",
                    "scrollbar_color": "rgba(255, 255, 255, 0.2) transparent",
                    "&::-webkit-scrollbar": {
                        "width": "8px",
                    },
                    "&::-webkit-scrollbar-track": {
                        "background": "transparent",
                    },
                    "&::-webkit-scrollbar-thumb": {
                        "background": "rgba(255, 255, 255, 0.2)",
                        "border_radius": "4px",
                    },
                    "&::-webkit-scrollbar-thumb:hover": {
                        "background": "rgba(255, 255, 255, 0.3)",
                    },
                }
            ),
            # Edit mode - show editor
            rx.box(
                enhanced_editor(
                    value=PlaybookEditorState.content,
                    on_change=PlaybookEditorState.set_content,
                    height="auto",
                    placeholder="Start typing your markdown here...",
                ),
                style={
                    "min_height": "500px",
                    "background": "rgba(0, 0, 0, 0.3)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                    "border_radius": "12px",
                    "padding_bottom": "2rem",  # Extra padding at bottom
                }
            ),
        ),
        
        # Add custom styling for markdown
        rx.html("""
        <style>
        /* Markdown syntax highlighting */
        .cm-editor .cm-line {
            line-height: 1.8;
        }
        
        /* Headers */
        .cm-editor .cm-header-1 {
            font-size: 2.25rem;
            font-weight: 700;
            color: white;
        }
        
        .cm-editor .cm-header-2 {
            font-size: 1.75rem;
            font-weight: 600;
            color: white;
        }
        
        .cm-editor .cm-header-3 {
            font-size: 1.5rem;
            font-weight: 500;
            color: white;
        }
        
        /* Text styling */
        .cm-editor .cm-strong {
            font-weight: 700;
            color: white;
        }
        
        .cm-editor .cm-em {
            font-style: italic;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .cm-editor .cm-link {
            color: #818cf8;
            text-decoration: underline;
        }
        
        .cm-editor .cm-url {
            color: #6366f1;
        }
        
        .cm-editor .cm-quote {
            color: rgba(156, 163, 175, 0.9);
            border-left: 3px solid rgba(99, 102, 241, 0.5);
            padding-left: 1rem;
        }
        
        /* Code blocks */
        .cm-editor .cm-codeblock {
            background: rgba(0, 0, 0, 0.5);
            padding: 0.5rem;
            border-radius: 4px;
            font-family: monospace;
        }
        
        .cm-editor .cm-code {
            background: rgba(99, 102, 241, 0.1);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
            font-family: monospace;
        }
        </style>
        """),
        width="100%",
    )


def editor_panel() -> rx.Component:
    """Create the main editor panel."""
    return rx.vstack(
        # Editor header with title and category
        rx.hstack(
            rx.input(
                value=PlaybookEditorState.title,
                on_change=PlaybookEditorState.set_title,
                placeholder="Playbook Title",
                style={
                    "background": "transparent",
                    "border": "none",
                    "border_bottom": "2px solid rgba(255, 255, 255, 0.1)",
                    "color": "white",
                    "font_size": "1.75rem",  # Increased from 1.5rem
                    "font_weight": "700",
                    "padding": "1rem 0",  # Increased from 0.5rem 0
                    "height": "60px",  # Added explicit height
                    "width": "100%",
                    "_focus": {
                        "outline": "none",
                        "border_bottom": "2px solid rgba(99, 102, 241, 0.5)",
                    },
                    "_placeholder": {
                        "color": "rgba(156, 163, 175, 0.5)",
                    }
                }
            ),
            rx.select(
                PlaybookEditorState.categories,
                value=PlaybookEditorState.category,
                on_change=PlaybookEditorState.set_category,
                placeholder="Select Category",
                style={
                    "background": "rgba(255, 255, 255, 0.05)",
                    "border": "1px solid rgba(255, 255, 255, 0.2)",
                    "border_radius": "8px",
                    "color": "white",
                    "padding": "0.5rem 1rem",
                    "min_width": "200px",
                }
            ),
            width="100%",
            spacing="4",
            margin_bottom="2rem",
        ),
        
        # Editor toolbar
        editor_toolbar(),
        
        # Editor content
        editor_content(),
        
        width="100%",
        spacing="4",
    )


def left_sidebar_panel() -> rx.Component:
    """Create the left sidebar with playbook templates and resources."""
    # Common box style for all sidebar cards
    sidebar_card_style = {
        **CARD_STYLE,
        "padding": "1.5rem",
        "width": "100%",  # Full width of parent
    }
    
    return rx.vstack(
        # Templates
        rx.box(
            rx.vstack(
                rx.text(
                    "Templates",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.vstack(
                    rx.button(
                        "Incident Response",
                        on_click=lambda: PlaybookEditorState.load_template("incident"),
                        style={
                            "width": "100%",
                            "padding": "0.75rem",
                            "background": "transparent",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "6px",
                            "color": "rgba(255, 255, 255, 0.8)",
                            "font_size": "0.875rem",
                            "text_align": "left",
                            "cursor": "pointer",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border_color": "rgba(99, 102, 241, 0.3)",
                            }
                        }
                    ),
                    rx.button(
                        "Security Audit",
                        on_click=lambda: PlaybookEditorState.load_template("audit"),
                        style={
                            "width": "100%",
                            "padding": "0.75rem",
                            "background": "transparent",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "6px",
                            "color": "rgba(255, 255, 255, 0.8)",
                            "font_size": "0.875rem",
                            "text_align": "left",
                            "cursor": "pointer",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border_color": "rgba(99, 102, 241, 0.3)",
                            }
                        }
                    ),
                    rx.button(
                        "Maintenance",
                        on_click=lambda: PlaybookEditorState.load_template("maintenance"),
                        style={
                            "width": "100%",
                            "padding": "0.75rem",
                            "background": "transparent",
                            "border": "1px solid rgba(255, 255, 255, 0.1)",
                            "border_radius": "6px",
                            "color": "rgba(255, 255, 255, 0.8)",
                            "font_size": "0.875rem",
                            "text_align": "left",
                            "cursor": "pointer",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border_color": "rgba(99, 102, 241, 0.3)",
                            }
                        }
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        # Resources
        rx.box(
            rx.vstack(
                rx.text(
                    "Resources",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.vstack(
                    rx.link(
                        rx.hstack(
                            rx.icon(tag="book-open", size=16),
                            rx.text("Markdown Guide", font_size="0.875rem"),
                            spacing="2",
                            align="center",
                        ),
                        href="https://www.markdownguide.org/basic-syntax/",
                        is_external=True,
                        style={
                            "color": "rgba(255, 255, 255, 0.8)",
                            "_hover": {"color": "#6366f1"},
                        }
                    ),
                    rx.link(
                        rx.hstack(
                            rx.icon(tag="shield", size=16),
                            rx.text("NIST Guidelines", font_size="0.875rem"),
                            spacing="2",
                            align="center",
                        ),
                        href="https://www.nist.gov/cyberframework",
                        is_external=True,
                        style={
                            "color": "rgba(255, 255, 255, 0.8)",
                            "_hover": {"color": "#6366f1"},
                        }
                    ),
                    rx.link(
                        rx.hstack(
                            rx.icon(tag="file-text", size=16),
                            rx.text("Best Practices", font_size="0.875rem"),
                            spacing="2",
                            align="center",
                        ),
                        href="#",
                        style={
                            "color": "rgba(255, 255, 255, 0.8)",
                            "_hover": {"color": "#6366f1"},
                        }
                    ),
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        # Recent Files
        rx.box(
            rx.vstack(
                rx.text(
                    "Recent Playbooks",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.vstack(
                    rx.foreach(
                        ["Network Scan Response", "Database Backup", "User Access Review"],
                        lambda name: rx.hstack(
                            rx.icon(tag="file", size=14),
                            rx.text(
                                name,
                                style={
                                    "font_size": "0.875rem",
                                    "color": "rgba(255, 255, 255, 0.7)",
                                    "cursor": "pointer",
                                    "_hover": {"color": "white"},
                                }
                            ),
                            spacing="2",
                            align="center",
                        )
                    ),
                    spacing="2",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        spacing="4",
        width="280px",  # Slightly narrower than right sidebar
        flex_shrink="0",  # Prevent shrinking
    )


def right_sidebar_panel() -> rx.Component:
    """Create the right sidebar with metadata and actions."""
    # Common box style for all sidebar cards
    sidebar_card_style = {
        **CARD_STYLE,
        "padding": "1.5rem",
        "width": "100%",  # Full width of parent
    }
    
    return rx.vstack(
        # Save actions
        rx.box(
            rx.vstack(
                rx.button(
                    rx.icon(tag="save", size=20),
                    "Save Draft",
                    on_click=PlaybookEditorState.save_draft,
                    style={
                        "width": "100%",
                        "padding": "1rem",
                        "background": "rgba(255, 255, 255, 0.05)",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "color": "white",
                        "font_weight": "500",
                        "cursor": "pointer",
                        "transition": "all 0.3s ease",
                        "_hover": {
                            "background": "rgba(255, 255, 255, 0.1)",
                            "transform": "translateY(-2px)",
                        }
                    }
                ),
                rx.button(
                    rx.icon(tag="rocket", size=20),
                    "Publish",
                    on_click=PlaybookEditorState.publish_playbook,
                    style={
                        "width": "100%",
                        "padding": "1rem",
                        "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                        "border": "none",
                        "border_radius": "8px",
                        "color": "white",
                        "font_weight": "600",
                        "cursor": "pointer",
                        "transition": "all 0.3s ease",
                        "_hover": {
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 8px 20px rgba(16, 185, 129, 0.3)",
                        }
                    }
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        # Tags
        rx.box(
            rx.vstack(
                rx.text(
                    "Tags",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.input(
                    value=PlaybookEditorState.tag_input,
                    on_change=PlaybookEditorState.set_tag_input,
                    on_key_down=PlaybookEditorState.handle_tag_input,
                    placeholder="Add tags (press Enter)",
                    style={
                        "background": "rgba(255, 255, 255, 0.05)",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "color": "white",
                        "padding": "0.5rem",
                        "width": "100%",
                        "_focus": {
                            "outline": "none",
                            "border": "1px solid rgba(99, 102, 241, 0.5)",
                        }
                    }
                ),
                rx.hstack(
                    rx.foreach(
                        PlaybookEditorState.tags,
                        lambda tag: rx.box(
                            rx.hstack(
                                rx.text(tag, style={"font_size": "0.875rem"}),
                                rx.icon(
                                    tag="x",
                                    size=14,
                                    on_click=lambda: PlaybookEditorState.remove_tag(tag),
                                    style={"cursor": "pointer"}
                                ),
                                spacing="2",
                                align="center",
                            ),
                            style={
                                "background": "rgba(99, 102, 241, 0.2)",
                                "border": "1px solid rgba(99, 102, 241, 0.3)",
                                "border_radius": "9999px",
                                "padding": "0.25rem 0.75rem",
                                "color": "white",
                            }
                        )
                    ),
                    wrap="wrap",
                    spacing="2",
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        # Metadata
        rx.box(
            rx.vstack(
                rx.text(
                    "Metadata",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Status:", style={"color": "rgba(156, 163, 175, 0.8)", "font_size": "0.875rem"}),
                        rx.text(
                            PlaybookEditorState.status,
                            style={
                                "color": rx.cond(
                                    PlaybookEditorState.status == "Published",
                                    "#10b981",
                                    "#f59e0b"
                                ),
                                "font_weight": "500",
                                "font_size": "0.875rem",
                            }
                        ),
                        width="100%",
                        justify="between",
                    ),
                    rx.hstack(
                        rx.text("Created:", style={"color": "rgba(156, 163, 175, 0.8)", "font_size": "0.875rem"}),
                        rx.text(
                            PlaybookEditorState.created_date,
                            style={"color": "white", "font_size": "0.875rem"}
                        ),
                        width="100%",
                        justify="between",
                    ),
                    rx.hstack(
                        rx.text("Modified:", style={"color": "rgba(156, 163, 175, 0.8)", "font_size": "0.875rem"}),
                        rx.text(
                            PlaybookEditorState.modified_date,
                            style={"color": "white", "font_size": "0.875rem"}
                        ),
                        width="100%",
                        justify="between",
                    ),
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            style=sidebar_card_style,
        ),
        
        spacing="4",
        width="280px",  # Fixed width for sidebar
        flex_shrink="0",  # Prevent shrinking
    )


def PlaybookEditorEnhanced() -> rx.Component:
    """Enhanced playbook editor with WYSIWYG capabilities and live preview toggle."""
    return rx.vstack(
        # Header with title only
        rx.hstack(
            metallic_title("Playbook Editor"),
            rx.text(
                "Auto-saved",
                style={
                    "color": "rgba(156, 163, 175, 0.6)",
                    "font_size": "0.875rem",
                    "display": rx.cond(
                        PlaybookEditorState.auto_saved,
                        "block",
                        "none"
                    )
                }
            ),
            width="100%",
            justify="between",
            align="center",
            margin_bottom="2rem",
        ),
        
        # Main content area with three columns
        rx.hstack(
            # Left sidebar with back button
            rx.vstack(
                # Back to Library button - same width as sidebar
                rx.button(
                    rx.icon(tag="arrow-left", size=20),
                    "Back to Library",
                    on_click=lambda: rx.redirect("/playbook"),
                    style={
                        "width": "100%",  # Full width of sidebar
                        "background": "rgba(255, 255, 255, 0.05)",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "color": "rgba(255, 255, 255, 0.8)",
                        "padding": "0.75rem 1rem",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "display": "flex",
                        "align_items": "center",
                        "gap": "0.5rem",
                        "font_weight": "500",
                        "_hover": {
                            "background": "rgba(255, 255, 255, 0.1)",
                            "color": "white",
                            "border_color": "rgba(255, 255, 255, 0.3)",
                        }
                    }
                ),
                # Left sidebar panels
                left_sidebar_panel(),
                spacing="4",
                width="280px",
                align_self="start",  # Align to top
            ),
            
            # Center editor panel with margins
            rx.box(
                editor_panel(),
                flex="1 1 0",  # Allow it to grow and shrink
                min_width="600px",  # Minimum width for usability
                margin="0 2rem",  # Add margins to create space from sidebars
                align_self="start",  # Align to top
            ),
            
            # Right sidebar with visibility toggle
            rx.vstack(
                # Personal/Public toggle button
                rx.hstack(
                    rx.button(
                        rx.icon(
                            tag=rx.cond(
                                PlaybookEditorState.is_public,
                                "globe",
                                "lock"
                            ),
                            size=18
                        ),
                        "Personal",
                        on_click=lambda: PlaybookEditorState.set_is_public(False),
                        style={
                            "flex": "1",
                            "padding": "0.75rem",
                            "background": rx.cond(
                                ~PlaybookEditorState.is_public,
                                "rgba(99, 102, 241, 0.2)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": rx.cond(
                                ~PlaybookEditorState.is_public,
                                "1px solid rgba(99, 102, 241, 0.5)",
                                "1px solid rgba(255, 255, 255, 0.2)"
                            ),
                            "border_radius": "8px 0 0 8px",
                            "color": rx.cond(
                                ~PlaybookEditorState.is_public,
                                "white",
                                "rgba(255, 255, 255, 0.7)"
                            ),
                            "cursor": "pointer",
                            "font_weight": rx.cond(
                                ~PlaybookEditorState.is_public,
                                "600",
                                "400"
                            ),
                            "transition": "all 0.2s ease",
                            "_hover": {
                                "background": rx.cond(
                                    ~PlaybookEditorState.is_public,
                                    "rgba(99, 102, 241, 0.3)",
                                    "rgba(255, 255, 255, 0.1)"
                                ),
                            }
                        }
                    ),
                    rx.button(
                        rx.icon(
                            tag=rx.cond(
                                PlaybookEditorState.is_public,
                                "globe",
                                "lock"
                            ),
                            size=18
                        ),
                        "Public",
                        on_click=lambda: PlaybookEditorState.set_is_public(True),
                        style={
                            "flex": "1",
                            "padding": "0.75rem",
                            "background": rx.cond(
                                PlaybookEditorState.is_public,
                                "rgba(16, 185, 129, 0.2)",
                                "rgba(255, 255, 255, 0.05)"
                            ),
                            "border": rx.cond(
                                PlaybookEditorState.is_public,
                                "1px solid rgba(16, 185, 129, 0.5)",
                                "1px solid rgba(255, 255, 255, 0.2)"
                            ),
                            "border_radius": "0 8px 8px 0",
                            "color": rx.cond(
                                PlaybookEditorState.is_public,
                                "white",
                                "rgba(255, 255, 255, 0.7)"
                            ),
                            "cursor": "pointer",
                            "font_weight": rx.cond(
                                PlaybookEditorState.is_public,
                                "600",
                                "400"
                            ),
                            "transition": "all 0.2s ease",
                            "_hover": {
                                "background": rx.cond(
                                    PlaybookEditorState.is_public,
                                    "rgba(16, 185, 129, 0.3)",
                                    "rgba(255, 255, 255, 0.1)"
                                ),
                            }
                        }
                    ),
                    spacing="0",
                    width="100%",
                ),
                # Right sidebar panels
                right_sidebar_panel(),
                spacing="4",
                width="280px",
                align_self="start",  # Align to top
            ),
            
            spacing="0",  # No spacing between columns
            width="100%",
            align="start",
            justify="between",  # Push sidebars to edges
        ),
        
        spacing="6",
        width="100%",
        padding="1rem 2rem",
        padding_bottom="120px",  # Increased space for navigation
        position="absolute",
        top="0",
        left="50%",
        transform="translateX(-50%)",
        max_width="95vw",
        min_height="100vh",
        z_index="10",
    )