import reflex as rx
from ..states.dat_update_state import DatUpdateState


def dat_update_form() -> rx.Component:
    """Modern glass morphism DAT update form component."""
    return rx.vstack(
        
        # Success/Error Messages
        rx.cond(
            DatUpdateState.submission_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag=rx.cond(
                            DatUpdateState.submission_status == "success",
                            "check",
                            "alert_circle"
                        ),
                        size=20,
                        color=rx.cond(
                            DatUpdateState.submission_status == "success",
                            "rgba(34, 197, 94, 0.9)",
                            "rgba(239, 68, 68, 0.9)"
                        ),
                    ),
                    rx.text(
                        DatUpdateState.submission_message,
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
                        on_click=DatUpdateState.clear_message,
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
                    DatUpdateState.submission_status == "success",
                    "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)"
                ),
                border=rx.cond(
                    DatUpdateState.submission_status == "success",
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
            # Left Section - Employee & Project Selection
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
                        DatUpdateState.employees,
                        value=DatUpdateState.selected_employee_id,
                        on_change=DatUpdateState.set_selected_employee_id,
                        placeholder="Select employee...",
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
                        DatUpdateState.projects,
                        value=DatUpdateState.selected_project_id,
                        on_change=DatUpdateState.set_selected_project_id,
                        placeholder="Select project...",
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
            
            # Middle Section - Asset & DAT Version
            rx.vstack(
                rx.text(
                    "Asset & DAT Version",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Asset Selection
                rx.vstack(
                    rx.text("Asset", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        DatUpdateState.assets,
                        value=DatUpdateState.selected_asset_id,
                        on_change=DatUpdateState.set_selected_asset_id,
                        placeholder="Select asset...",
                        disabled=rx.cond(DatUpdateState.assets, False, True),
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
                
                # DAT Version Selection
                rx.vstack(
                    rx.text("DAT Version", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        DatUpdateState.dat_versions,
                        value=DatUpdateState.selected_datversion_id,
                        on_change=DatUpdateState.set_selected_datversion_id,
                        placeholder="Select DAT version...",
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
            
            # Right Section - DAT File & Results
            rx.vstack(
                rx.text(
                    "DAT File & Results",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # DAT File Name
                rx.vstack(
                    rx.hstack(
                        rx.text("DAT File Name", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.input(
                        value=DatUpdateState.datfile_name,
                        on_change=DatUpdateState.set_datfile_name,
                        placeholder="e.g., avgatp.dat",
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
                
                # Update Result
                rx.vstack(
                    rx.hstack(
                        rx.text("Update Result", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        DatUpdateState.result_options,
                        value=DatUpdateState.update_result,
                        on_change=DatUpdateState.set_update_result,
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
                        value=DatUpdateState.update_comments,
                        on_change=DatUpdateState.set_update_comments,
                        placeholder="Optional notes about the DAT update process...",
                        resize="vertical",
                        rows="3",
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
        
            key=DatUpdateState.form_key,  # Force re-render on form reset
            width="90%",
            max_width="1400px",
            margin="0 auto",
            padding="2rem",
            border_radius="16px",
            background="linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
            border="1px solid rgba(255, 255, 255, 0.2)",
            backdrop_filter="blur(20px)",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
            on_mount=DatUpdateState.load_form_data,
        ),
        
        spacing="0",
        width="100%",
    )