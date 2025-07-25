"""Simple test for markdown editor debugging."""
import reflex as rx

def test_markdown_editor() -> rx.Component:
    """Create a simple markdown editor for testing."""
    return rx.vstack(
        rx.heading("Markdown Editor Test", size="4"),
        rx.text("Type markdown syntax like **bold**, *italic*, # Header, `code`"),
        
        # Add debug console
        rx.box(
            rx.html("""
                <div id="debug-console" style="
                    background: #000;
                    color: #0f0;
                    font-family: monospace;
                    padding: 10px;
                    height: 150px;
                    overflow-y: auto;
                    border: 1px solid #0f0;
                    margin-bottom: 20px;
                ">
                    <div>Debug Console:</div>
                </div>
            """),
            width="100%",
        ),
        
        # Simpler markdown editor
        rx.box(
            rx.html("""
                <div 
                    contenteditable="true"
                    id="test-editor"
                    style="
                        width: 100%;
                        min-height: 300px;
                        padding: 20px;
                        background: rgba(0, 0, 0, 0.3);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 8px;
                        color: white;
                        font-size: 16px;
                        line-height: 1.6;
                        outline: none;
                    "
                >Start typing here...</div>
                
                <script>
                    console.log('Markdown editor script loading...');
                    
                    // Add debug logging function
                    function debugLog(message) {
                        console.log(message);
                        const debugConsole = document.getElementById('debug-console');
                        if (debugConsole) {
                            const timestamp = new Date().toLocaleTimeString();
                            debugConsole.innerHTML += '<div>[' + timestamp + '] ' + message + '</div>';
                            debugConsole.scrollTop = debugConsole.scrollHeight;
                        }
                    }
                    
                    // Wait for DOM to be ready
                    function initMarkdownEditor() {
                        debugLog('Initializing markdown editor...');
                        
                        const editor = document.getElementById('test-editor');
                        if (!editor) {
                            debugLog('ERROR: Editor element not found!');
                            return;
                        }
                        
                        debugLog('Editor element found');
                        
                        // Simple markdown detection
                        function detectAndProcessMarkdown() {
                            const selection = window.getSelection();
                            if (!selection.rangeCount) {
                                debugLog('No selection');
                                return;
                            }
                            
                            const range = selection.getRangeAt(0);
                            const node = range.startContainer;
                            
                            if (node.nodeType !== Node.TEXT_NODE) {
                                debugLog('Not a text node');
                                return;
                            }
                            
                            const text = node.textContent;
                            const offset = range.startOffset;
                            
                            debugLog('Text: "' + text + '", Offset: ' + offset);
                            
                            // Simple bold detection
                            if (text.includes('**')) {
                                const start = text.indexOf('**');
                                const end = text.indexOf('**', start + 2);
                                
                                if (start !== -1 && end !== -1 && end > start + 2) {
                                    debugLog('Found bold pattern from ' + start + ' to ' + (end + 2));
                                    
                                    // Check if cursor just left the pattern
                                    if (offset === end + 2 || offset === start) {
                                        debugLog('Cursor at edge of bold pattern!');
                                        
                                        // Process the markdown
                                        const content = text.substring(start + 2, end);
                                        const before = text.substring(0, start);
                                        const after = text.substring(end + 2);
                                        
                                        // Create bold element
                                        const bold = document.createElement('strong');
                                        bold.textContent = content;
                                        bold.style.fontWeight = '700';
                                        
                                        // Replace content
                                        node.textContent = before;
                                        node.parentNode.insertBefore(bold, node.nextSibling);
                                        
                                        if (after) {
                                            const afterNode = document.createTextNode(after);
                                            bold.parentNode.insertBefore(afterNode, bold.nextSibling);
                                        }
                                        
                                        debugLog('Bold element created!');
                                    }
                                }
                            }
                        }
                        
                        // Add event listeners
                        document.addEventListener('selectionchange', function() {
                            debugLog('Selection changed');
                            detectAndProcessMarkdown();
                        });
                        
                        editor.addEventListener('input', function() {
                            debugLog('Input event fired');
                        });
                        
                        debugLog('Event listeners attached');
                    }
                    
                    // Initialize when DOM is ready
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', initMarkdownEditor);
                        debugLog('Waiting for DOMContentLoaded...');
                    } else {
                        // DOM is already ready
                        initMarkdownEditor();
                    }
                </script>
            """),
            width="100%",
        ),
        
        spacing="4",
        padding="20px",
        width="100%",
        max_width="800px",
    )

# Create a simple test app
app = rx.App()
app.add_page(test_markdown_editor, route="/test-markdown")

if __name__ == "__main__":
    app.run()