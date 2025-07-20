import reflex as rx
from ..states.log_collection_state import LogCollectionState


def log_collection_form() -> rx.Component:
    """Modern glass morphism log collection form component."""
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
                    align="center",
                    spacing="3",
                ),
                width="90%",
                max_width="1400px",
                margin="0 auto",
                padding="1rem",
                border_radius="8px",
                background=rx.cond(
                    LogCollectionState.submission_status == "success",
                    "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)"
                ),
                border=rx.cond(
                    LogCollectionState.submission_status == "success",
                    "1px solid rgba(34, 197, 94, 0.3)",
                    "1px solid rgba(239, 68, 68, 0.3)"
                ),
                margin_bottom="1rem",
                custom_attrs={"data-toast-container": "true"},
            ),
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
        
        rx.box(
        rx.hstack(
            # Left Section - Personnel & Project
            rx.vstack(
                rx.text(
                    "Personnel & Project",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Employee Selection
                rx.vstack(
                    rx.text("Employee", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        LogCollectionState.employees,
                        placeholder="Select employee...",
                        on_change=LogCollectionState.set_employee,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Project Selection
                rx.vstack(
                    rx.text("Project", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        LogCollectionState.projects,
                        placeholder="Select project...",
                        on_change=LogCollectionState.set_project,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Date/Time Selection
                rx.vstack(
                    rx.hstack(
                        rx.text("Collection Date & Time", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.input(
                        type="datetime-local",
                        value=LogCollectionState.collection_date,
                        on_change=LogCollectionState.set_date,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                spacing="4",
                width="100%",
            ),
            
            # Middle Section - Asset & Log Type
            rx.vstack(
                rx.text(
                    "Asset & Log Type",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Asset Selection
                rx.vstack(
                    rx.text("Asset", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        LogCollectionState.filtered_assets,
                        placeholder="Select asset...",
                        on_change=LogCollectionState.set_asset,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Common Log Types Selection
                rx.vstack(
                    rx.hstack(
                        rx.text("Common Log Types", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.cond(
                            LogCollectionState.baseline_logs_completed,
                            rx.text("(Optional - Baseline Complete)", color="rgba(34, 197, 94, 0.8)", font_size="0.8rem"),
                            rx.text("*", color="red", font_size="0.9rem"),
                        ),
                        spacing="1",
                    ),
                    rx.select(
                        LogCollectionState.logtypes,
                        placeholder="Select common log type...",
                        on_change=LogCollectionState.set_common_logtype,
                        value=LogCollectionState.selected_common_logtype,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    # Baseline status indicator
                    rx.cond(
                        LogCollectionState.baseline_logs_completed,
                        rx.box(
                            rx.hstack(
                                rx.icon(tag="check", size=16, color="rgba(34, 197, 94, 0.8)"),
                                rx.text(
                                    "Baseline logs completed within 30 days. Extended logs can be submitted independently.",
                                    color="rgba(34, 197, 94, 0.8)",
                                    font_size="0.8rem",
                                ),
                                spacing="2",
                            ),
                            padding="0.5rem",
                            background="rgba(34, 197, 94, 0.1)",
                            border="1px solid rgba(34, 197, 94, 0.3)",
                            border_radius="6px",
                            margin_top="0.5rem",
                        ),
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Extended Log Types Selection
                rx.vstack(
                    rx.text("Extended Log Types", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        LogCollectionState.extended_logtypes,
                        placeholder="Select extended log type...",
                        on_change=LogCollectionState.set_logtype,
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                spacing="4",
                width="100%",
            ),
            
            # Right Section - Collection Results
            rx.vstack(
                rx.text(
                    "Collection Results",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Collection Result
                rx.vstack(
                    rx.hstack(
                        rx.text("Collection Result", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        ["Success", "Failed", "Partial Success", "In Progress", "Cancelled"],
                        value=LogCollectionState.collection_result,
                        on_change=LogCollectionState.set_result,
                        placeholder="Select result...",
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Comments
                rx.vstack(
                    rx.text("Comments", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.text_area(
                        value=LogCollectionState.collection_comments,
                        on_change=LogCollectionState.set_comments,
                        placeholder="Optional notes about the log collection...",
                        rows="5",
                        resize="vertical",
                        width="100%",
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "border": "1px solid rgba(255, 255, 255, 0.2)",
                            "color": "white",
                            "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                            "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                        },
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                spacing="4",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
            align="start",
        ),
        
            key=LogCollectionState.form_key,  # Force re-render on form reset
            width="90%",
            max_width="1400px",
            margin="0 auto",
            padding="2rem",
            border_radius="16px",
            background="linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
            border="1px solid rgba(255, 255, 255, 0.2)",
            backdrop_filter="blur(20px)",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
            on_mount=LogCollectionState.load_form_data,
        ),
        
        spacing="0",
        width="100%",
    )