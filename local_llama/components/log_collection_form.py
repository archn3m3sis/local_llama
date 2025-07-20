import reflex as rx
from ..states.log_collection_state import LogCollectionState


def simple_select(
    placeholder: str,
    options: list,
    on_change: callable,
    value: str = None,
    icon: str = None
) -> rx.Component:
    """Create a simple select component."""
    return rx.select(
        options,
        placeholder=placeholder,
        on_change=on_change,
        value=value,
        size="3",
        width="100%",
        style={
            "background": "rgba(255, 255, 255, 0.05)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "color": "white",
            "_hover": {
                "border": "1px solid rgba(59, 130, 246, 0.5)",
                "background": "rgba(255, 255, 255, 0.08)",
            },
            "_focus": {
                "border": "1px solid rgba(59, 130, 246, 0.8)",
                "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
            },
        }
    )


def form_section(title: str, icon: str, content: rx.Component) -> rx.Component:
    """Create a form section with title and icon."""
    return rx.vstack(
        rx.hstack(
            rx.icon(
                tag=icon,
                size=24,
                color="rgba(59, 130, 246, 0.8)",
            ),
            rx.text(
                title,
                font_size="1.1rem",
                font_weight="600",
                color="white",
            ),
            spacing="3",
            align="center",
            margin_bottom="1rem",
        ),
        content,
        spacing="4",
        width="100%",
        padding="2rem",
        background="rgba(255, 255, 255, 0.02)",
        border="1px solid rgba(255, 255, 255, 0.05)",
        border_radius="1rem",
        _hover={
            "border": "1px solid rgba(255, 255, 255, 0.08)",
            "background": "rgba(255, 255, 255, 0.03)",
        },
    )


def log_collection_form() -> rx.Component:
    """Create the modern log collection input form."""
    return rx.vstack(
        
        # Success/Error Messages
        rx.cond(
            LogCollectionState.submission_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag=rx.cond(
                            LogCollectionState.submission_status == "success",
                            "check",
                            "alert_circle"
                        ),
                        size=20,
                        color=rx.cond(
                            LogCollectionState.submission_status == "success",
                            "rgba(34, 197, 94, 0.9)",
                            "rgba(239, 68, 68, 0.9)"
                        ),
                    ),
                    rx.text(
                        LogCollectionState.submission_message,
                        color="white",
                        font_size="0.9rem",
                        custom_attrs={"data-toast-message": "true"},
                    ),
                    rx.spacer(),
                    rx.icon(
                        tag="x",
                        size=20,
                        color="rgba(255, 255, 255, 0.5)",
                        cursor="pointer",
                        on_click=LogCollectionState.clear_message,
                        _hover={"color": "white"},
                        custom_attrs={"data-clear-toast": "true"},
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                padding="1rem 1.5rem",
                background=rx.cond(
                    LogCollectionState.submission_status == "success",
                    "rgba(34, 197, 94, 0.1)",
                    "rgba(239, 68, 68, 0.1)"
                ),
                border=rx.cond(
                    LogCollectionState.submission_status == "success",
                    "1px solid rgba(34, 197, 94, 0.3)",
                    "1px solid rgba(239, 68, 68, 0.3)"
                ),
                border_radius="0.75rem",
                width="100%",
                margin_bottom="1.5rem",
                custom_attrs={"data-toast-container": "true"},
            ),
            rx.fragment(),
        ),
        
        # Auto-fade script for toast notifications
        rx.script(
            """
            // Auto-fade toast notification after 5 seconds
            (function() {
                let fadeTimer = null;
                
                const checkAndFade = () => {
                    const toastContainer = document.querySelector('[data-toast-container]');
                    const message = document.querySelector('[data-toast-message]');
                    
                    if (toastContainer && message && message.textContent.includes('successfully')) {
                        // Clear any existing timer
                        if (fadeTimer) clearTimeout(fadeTimer);
                        
                        // Set new timer to fade out the toast
                        fadeTimer = setTimeout(() => {
                            toastContainer.style.transition = 'opacity 0.5s ease-out';
                            toastContainer.style.opacity = '0';
                            setTimeout(() => {
                                toastContainer.style.display = 'none';
                            }, 500);
                        }, 5000);
                    }
                };
                
                // Run check when page loads and when content changes
                checkAndFade();
                const observer = new MutationObserver(checkAndFade);
                observer.observe(document.body, { childList: true, subtree: true });
            })();
            """
        ),
        
        # Form - Single horizontal row layout
        rx.hstack(
            # Personnel & Project Section
            form_section(
                "Personnel & Project",
                "users",
                rx.vstack(
                    # Employee Selection
                    rx.vstack(
                        rx.text(
                            "Employee *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            LogCollectionState.employees,
                            placeholder="Select employee...",
                            on_change=LogCollectionState.set_employee,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    
                    # Project Selection
                    rx.vstack(
                        rx.text(
                            "Project *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            LogCollectionState.projects,
                            placeholder="Select project...",
                            on_change=LogCollectionState.set_project,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    
                    # Date/Time Selection
                    rx.vstack(
                        rx.text(
                            "Collection Date & Time *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.input(
                            type="datetime-local",
                            value=LogCollectionState.collection_date,
                            on_change=LogCollectionState.set_date,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "padding": "0.75rem 1rem",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="6",
                    width="100%",
                ),
            ),
            
            # Asset & Log Type Section
            form_section(
                "Asset & Log Type",
                "server",
                rx.vstack(
                    # Asset Selection
                    rx.vstack(
                        rx.text(
                            "Asset *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            LogCollectionState.filtered_assets,
                            placeholder="Select asset...",
                            on_change=LogCollectionState.set_asset,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    
                    # Common Log Types Selection
                    rx.vstack(
                        rx.text(
                            "Common Log Types *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            [
                                "Windows Event System Logs",
                                "Windows Event Application Logs",
                                "Windows Event Security Logs",
                                "All Common Logtypes"
                            ],
                            placeholder="Select common log type...",
                            on_change=LogCollectionState.set_common_logtype,
                            value=LogCollectionState.selected_common_logtype,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    
                    # Extended Log Types Selection
                    rx.vstack(
                        rx.text(
                            "Extended Log Types",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            LogCollectionState.extended_logtypes,
                            placeholder="Select extended log type...",
                            on_change=LogCollectionState.set_logtype,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="6",
                    width="100%",
                ),
            ),
            
            # Collection Results Section
            form_section(
                "Collection Results",
                "clipboard",
                rx.vstack(
                    # Result Field
                    rx.vstack(
                        rx.text(
                            "Collection Result *",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.select(
                            [
                                "Success",
                                "Partial Success", 
                                "Failed",
                                "No Logs Found",
                                "Access Denied",
                                "System Offline",
                            ],
                            placeholder="Select result...",
                            on_change=LogCollectionState.set_result,
                            value=LogCollectionState.collection_result,
                            size="3",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    
                    # Comments Field
                    rx.vstack(
                        rx.text(
                            "Additional Comments",
                            font_size="0.9rem",
                            color="rgba(255, 255, 255, 0.7)",
                            margin_bottom="0.5rem",
                        ),
                        rx.text_area(
                            placeholder="Enter any additional notes or observations...",
                            value=LogCollectionState.collection_comments,
                            on_change=LogCollectionState.set_comments,
                            size="3",
                            rows="4",
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "color": "white",
                                "resize": "vertical",
                                "_placeholder": {"color": "rgba(255, 255, 255, 0.3)"},
                                "_hover": {
                                    "border": "1px solid rgba(59, 130, 246, 0.5)",
                                    "background": "rgba(255, 255, 255, 0.08)",
                                },
                                "_focus": {
                                    "border": "1px solid rgba(59, 130, 246, 0.8)",
                                    "box_shadow": "0 0 0 3px rgba(59, 130, 246, 0.2)",
                                },
                            }
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="6",
                    width="100%",
                ),
            ),
            
            spacing="6",
            width="100%",
            align="stretch",
        ),
        
        
        spacing="6",
        width="90%",
        max_width="1400px",
        padding="2rem",
        background="rgba(255, 255, 255, 0.01)",
        border="1px solid rgba(255, 255, 255, 0.05)",
        border_radius="1.5rem",
        backdrop_filter="blur(10px)",
        margin="0 auto",
        on_mount=LogCollectionState.load_form_data,
        key=LogCollectionState.form_key,
    )