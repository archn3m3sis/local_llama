"""Playbook Editor page with rich markdown editing capabilities."""
import reflex as rx
from ..components.metallic_text import metallic_title
from ..components.shared_styles import CARD_STYLE
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
        # Text formatting
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
                rx.icon(tag="underline", size=18),
                on_click=PlaybookEditorState.format_underline,
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
        
        # Headers
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
        
        # Lists
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
                rx.icon(tag="list-checks", size=18),
                on_click=PlaybookEditorState.format_checklist,
                style=button_style,
            ),
            spacing="2",
        ),
        
        rx.box(style=separator_style),
        
        # Insert elements
        rx.hstack(
            rx.button(
                rx.icon(tag="link", size=18),
                on_click=PlaybookEditorState.insert_link,
                style=button_style,
            ),
            rx.button(
                rx.icon(tag="image", size=18),
                on_click=PlaybookEditorState.insert_image,
                style=button_style,
            ),
            rx.button(
                rx.icon(tag="table", size=18),
                on_click=PlaybookEditorState.insert_table,
                style=button_style,
            ),
            rx.button(
                rx.icon(tag="quote", size=18),
                on_click=PlaybookEditorState.format_blockquote,
                style=button_style,
            ),
            spacing="2",
        ),
        
        rx.spacer(),
        
        style={
            **CARD_STYLE,
            "padding": "1rem",
            "margin_bottom": "1rem",
            "backdrop_filter": "blur(10px)",
        },
        width="100%",
        align="center",
    )


def live_markdown_editor() -> rx.Component:
    """Create a live preview markdown editor."""
    return rx.box(
        rx.html(
            f"""
            <div id="live-markdown-editor" style="width: 100%; height: 100%;">
                <div 
                    contenteditable="true"
                    id="editor-content"
                    style="
                        width: 100%;
                        height: calc(100vh - 350px);
                        min-height: 500px;
                        padding: 2rem;
                        background: rgba(0, 0, 0, 0.3);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        border-radius: 12px;
                        color: rgba(255, 255, 255, 0.95);
                        font-size: 1rem;
                        line-height: 1.8;
                        outline: none;
                        overflow-y: auto;
                    "
                ></div>
            </div>
            <script>
                (function() {{
                    const editor = document.getElementById('editor-content');
                    let rawContent = '';
                    
                    // Markdown patterns with their HTML replacements
                    const markdownPatterns = [
                        // Headers (must be at start of line)
                        {{pattern: /^##### (.+)$/gm, replacement: '<h5 style="color: white; font-size: 0.875rem; font-weight: 600; margin: 0.5rem 0;">$1</h5>', syntax: '#####'}},
                        {{pattern: /^#### (.+)$/gm, replacement: '<h4 style="color: white; font-size: 1rem; font-weight: 600; margin: 0.75rem 0;">$1</h4>', syntax: '####'}},
                        {{pattern: /^### (.+)$/gm, replacement: '<h3 style="color: white; font-size: 1.25rem; font-weight: 500; margin: 1rem 0 0.5rem 0;">$1</h3>', syntax: '###'}},
                        {{pattern: /^## (.+)$/gm, replacement: '<h2 style="color: white; font-size: 1.5rem; font-weight: 600; margin: 1.5rem 0 0.75rem 0;">$1</h2>', syntax: '##'}},
                        {{pattern: /^# (.+)$/gm, replacement: '<h1 style="color: white; font-size: 2rem; font-weight: 700; margin: 1.5rem 0 1rem 0; border-bottom: 2px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem;">$1</h1>', syntax: '#'}},
                        
                        // Bold and italic
                        {{pattern: /\\*\\*(.+?)\\*\\*/g, replacement: '<strong style="font-weight: 700;">$1</strong>', syntax: '**'}},
                        {{pattern: /\\*(.+?)\\*/g, replacement: '<em style="font-style: italic;">$1</em>', syntax: '*'}},
                        
                        // Inline code
                        {{pattern: /`([^`]+)`/g, replacement: '<code style="background: rgba(99, 102, 241, 0.2); padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.9em;">$1</code>', syntax: '`'}},
                        
                        // Blockquotes
                        {{pattern: /^> (.+)$/gm, replacement: '<blockquote style="border-left: 4px solid rgba(99, 102, 241, 0.5); padding-left: 1rem; margin: 1rem 0; color: rgba(156, 163, 175, 0.9);">$1</blockquote>', syntax: '>'}},
                        
                        // Links
                        {{pattern: /\\[([^\\]]+)\\]\\(([^\\)]+)\\)/g, replacement: '<a href="$2" style="color: #6366f1; text-decoration: none; border-bottom: 1px solid rgba(99, 102, 241, 0.3);">$1</a>', syntax: '[]()'}},
                        {{pattern: /\\[([^\\]]+)\\]/g, replacement: '<a href="#" style="color: #6366f1; text-decoration: none; border-bottom: 1px solid rgba(99, 102, 241, 0.3);">$1</a>', syntax: '[]'}}
                    ];
                    
                    function parseMarkdown(text) {{
                        // Store raw content
                        rawContent = text;
                        
                        // Escape HTML
                        let html = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                        
                        // Handle code blocks first (to prevent processing inside them)
                        const codeBlocks = [];
                        html = html.replace(/```(\\w*)\\n([\\s\\S]*?)```/g, function(match, lang, code) {{
                            const index = codeBlocks.length;
                            codeBlocks.push('<pre style="background: rgba(0, 0, 0, 0.5); padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0;"><code style="color: #e5e7eb; font-family: monospace;">' + code + '</code></pre>');
                            return '___CODEBLOCK_' + index + '___';
                        }});
                        
                        // Apply markdown patterns
                        markdownPatterns.forEach(({pattern, replacement}) => {{
                            html = html.replace(pattern, replacement);
                        }});
                        
                        // Handle lists
                        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
                        html = html.replace(/(<li>.*<\\/li>\\s*)+/g, function(match) {{
                            return '<ul style="padding-left: 2rem; margin: 0.75rem 0; list-style-type: disc;">' + match + '</ul>';
                        }});
                        
                        // Restore code blocks
                        codeBlocks.forEach((block, index) => {{
                            html = html.replace('___CODEBLOCK_' + index + '___', block);
                        }});
                        
                        // Convert newlines to line breaks (but not inside tags)
                        html = html.replace(/\\n/g, '<br>');
                        
                        return html;
                    }}
                    
                    function getCursorPosition() {{
                        const selection = window.getSelection();
                        if (selection.rangeCount === 0) return null;
                        
                        const range = selection.getRangeAt(0);
                        const preCaretRange = range.cloneRange();
                        preCaretRange.selectNodeContents(editor);
                        preCaretRange.setEnd(range.endContainer, range.endOffset);
                        
                        return preCaretRange.toString().length;
                    }}
                    
                    function setCursorPosition(position) {{
                        const selection = window.getSelection();
                        const range = document.createRange();
                        
                        let charCount = 0;
                        let node = editor;
                        let found = false;
                        
                        function traverseNodes(node) {{
                            if (found) return;
                            
                            if (node.nodeType === 3) {{ // Text node
                                const nextCharCount = charCount + node.textContent.length;
                                if (position <= nextCharCount) {{
                                    range.setStart(node, position - charCount);
                                    range.setEnd(node, position - charCount);
                                    found = true;
                                    return;
                                }}
                                charCount = nextCharCount;
                            }} else {{
                                for (let i = 0; i < node.childNodes.length; i++) {{
                                    traverseNodes(node.childNodes[i]);
                                    if (found) return;
                                }}
                            }}
                        }}
                        
                        traverseNodes(editor);
                        
                        if (found) {{
                            selection.removeAllRanges();
                            selection.addRange(range);
                        }}
                    }}
                    
                    function updateDisplay() {{
                        const cursorPos = getCursorPosition();
                        const html = parseMarkdown(rawContent);
                        editor.innerHTML = html;
                        
                        if (cursorPos !== null) {{
                            // Attempt to restore cursor position
                            setCursorPosition(cursorPos);
                        }}
                    }}
                    
                    function handleInput() {{
                        // Get plain text content
                        const walker = document.createTreeWalker(
                            editor,
                            NodeFilter.SHOW_TEXT,
                            null,
                            false
                        );
                        
                        let text = '';
                        let node;
                        while (node = walker.nextNode()) {{
                            text += node.textContent;
                        }}
                        
                        rawContent = text;
                        
                        // Update state
                        window.reflex_updateState({{content: rawContent}});
                        
                        // Debounce the display update
                        clearTimeout(window.updateTimeout);
                        window.updateTimeout = setTimeout(updateDisplay, 100);
                    }}
                    
                    if (editor) {{
                        // Set initial content
                        const initialContent = {JSON.stringify(PlaybookEditorState.content)};
                        rawContent = initialContent || '';
                        updateDisplay();
                        
                        // Listen for input
                        editor.addEventListener('input', handleInput);
                        
                        // Handle paste as plain text
                        editor.addEventListener('paste', function(e) {{
                            e.preventDefault();
                            const text = e.clipboardData.getData('text/plain');
                            document.execCommand('insertText', false, text);
                        }});
                        
                        // Show markdown syntax on hover
                        editor.addEventListener('mousemove', function(e) {{
                            const selection = window.getSelection();
                            const range = document.caretRangeFromPoint(e.clientX, e.clientY);
                            
                            if (range) {{
                                const node = range.startContainer.parentElement;
                                
                                // Add subtle hints for formatted elements
                                if (node.tagName === 'STRONG') {{
                                    node.title = '**bold**';
                                }} else if (node.tagName === 'EM') {{
                                    node.title = '*italic*';
                                }} else if (node.tagName === 'CODE') {{
                                    node.title = '`code`';
                                }} else if (node.tagName === 'H1') {{
                                    node.title = '# Header 1';
                                }} else if (node.tagName === 'H2') {{
                                    node.title = '## Header 2';
                                }} else if (node.tagName === 'H3') {{
                                    node.title = '### Header 3';
                                }} else if (node.tagName === 'H4') {{
                                    node.title = '#### Header 4';
                                }} else if (node.tagName === 'H5') {{
                                    node.title = '##### Header 5';
                                }} else if (node.tagName === 'BLOCKQUOTE') {{
                                    node.title = '> Quote';
                                }} else if (node.tagName === 'A') {{
                                    node.title = '[Link](url)';
                                }}
                            }}
                        }});
                    }}
                }})();
            </script>
            """
        ),
        style={
            **CARD_STYLE,
            "width": "100%",
        }
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
                    "font_size": "1.5rem",
                    "font_weight": "700",
                    "padding": "0.5rem 0",
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
        
        # Live markdown editor
        live_markdown_editor(),
        
        width="100%",
        spacing="4",
    )


def sidebar_panel() -> rx.Component:
    """Create the sidebar with metadata and actions."""
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
                    on_click=PlaybookEditorState.publish,
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
            style={
                **CARD_STYLE,
                "padding": "1.5rem",
            }
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
            style={
                **CARD_STYLE,
                "padding": "1.5rem",
            }
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
                        rx.text("Status:", style={"color": "rgba(156, 163, 175, 0.8)"}),
                        rx.text(
                            PlaybookEditorState.status,
                            style={
                                "color": rx.cond(
                                    PlaybookEditorState.status == "Published",
                                    "#10b981",
                                    "#f59e0b"
                                ),
                                "font_weight": "500",
                            }
                        ),
                        width="100%",
                        justify="between",
                    ),
                    rx.hstack(
                        rx.text("Created:", style={"color": "rgba(156, 163, 175, 0.8)"}),
                        rx.text(
                            PlaybookEditorState.created_date,
                            style={"color": "white", "font_size": "0.875rem"}
                        ),
                        width="100%",
                        justify="between",
                    ),
                    rx.hstack(
                        rx.text("Modified:", style={"color": "rgba(156, 163, 175, 0.8)"}),
                        rx.text(
                            PlaybookEditorState.modified_date,
                            style={"color": "white", "font_size": "0.875rem"}
                        ),
                        width="100%",
                        justify="between",
                    ),
                    rx.hstack(
                        rx.text("Version:", style={"color": "rgba(156, 163, 175, 0.8)"}),
                        rx.text(
                            f"v{PlaybookEditorState.version}",
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
            style={
                **CARD_STYLE,
                "padding": "1.5rem",
            }
        ),
        
        # Quick actions
        rx.box(
            rx.vstack(
                rx.text(
                    "Quick Actions",
                    style={
                        "color": "white",
                        "font_weight": "600",
                        "margin_bottom": "0.5rem",
                    }
                ),
                rx.button(
                    rx.icon(tag="download", size=16),
                    "Export as Markdown",
                    on_click=PlaybookEditorState.export_markdown,
                    style={
                        "width": "100%",
                        "padding": "0.75rem",
                        "background": "transparent",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "color": "rgba(255, 255, 255, 0.8)",
                        "font_size": "0.875rem",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "background": "rgba(255, 255, 255, 0.05)",
                            "color": "white",
                        }
                    }
                ),
                rx.button(
                    rx.icon(tag="copy", size=16),
                    "Duplicate Playbook",
                    on_click=PlaybookEditorState.duplicate_playbook,
                    style={
                        "width": "100%",
                        "padding": "0.75rem",
                        "background": "transparent",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "border_radius": "8px",
                        "color": "rgba(255, 255, 255, 0.8)",
                        "font_size": "0.875rem",
                        "cursor": "pointer",
                        "transition": "all 0.2s ease",
                        "_hover": {
                            "background": "rgba(255, 255, 255, 0.05)",
                            "color": "white",
                        }
                    }
                ),
                spacing="2",
                width="100%",
            ),
            style={
                **CARD_STYLE,
                "padding": "1.5rem",
            }
        ),
        
        spacing="4",
        width="300px",
    )


def PlaybookEditor() -> rx.Component:
    """Main playbook editor page."""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.hstack(
                    rx.button(
                        rx.icon(tag="arrow-left", size=20),
                        "Back to Library",
                        on_click=lambda: rx.redirect("/playbook"),
                        style={
                            "background": "transparent",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "border_radius": "8px",
                            "color": "rgba(255, 255, 255, 0.8)",
                            "padding": "0.5rem 1rem",
                            "cursor": "pointer",
                            "transition": "all 0.2s ease",
                            "_hover": {
                                "background": "rgba(255, 255, 255, 0.05)",
                                "color": "white",
                            }
                        }
                    ),
                    metallic_title("Playbook Editor"),
                    align="center",
                    spacing="4",
                ),
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
            
            # Main content area
            rx.hstack(
                # Editor panel
                rx.box(
                    editor_panel(),
                    flex="1",
                ),
                
                # Sidebar
                sidebar_panel(),
                
                spacing="4",
                width="100%",
                align="start",
            ),
            
            # CSS for custom styling
            rx.html("""
            <style>
            #live-markdown-editor {
                scrollbar-width: thin;
                scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
            }
            #live-markdown-editor::-webkit-scrollbar {
                width: 8px;
            }
            #live-markdown-editor::-webkit-scrollbar-track {
                background: transparent;
            }
            #live-markdown-editor::-webkit-scrollbar-thumb {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            #editor-content::-webkit-scrollbar {
                width: 8px;
            }
            #editor-content::-webkit-scrollbar-track {
                background: transparent;
            }
            #editor-content::-webkit-scrollbar-thumb {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            </style>
            """),
            
            spacing="6",
            width="100%",
            padding="2rem",
        ),
        style={
            "width": "100%",
            "height": "100vh",
            "overflow_y": "auto",
            "padding_top": "2rem",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "z_index": "10",
        }
    )