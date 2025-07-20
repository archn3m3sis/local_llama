import reflex as rx
from ..states.image_collection_state import ImageCollectionState


def image_collection_form() -> rx.Component:
    """Modern glass morphism image collection form component."""
    return rx.vstack(
        
        # Success/Error Messages
        rx.cond(
            ImageCollectionState.submission_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag=rx.cond(
                            ImageCollectionState.submission_status == "success",
                            "check",
                            "alert_circle"
                        ),
                        size=20,
                        color=rx.cond(
                            ImageCollectionState.submission_status == "success",
                            "rgba(34, 197, 94, 0.9)",
                            "rgba(239, 68, 68, 0.9)"
                        ),
                    ),
                    rx.text(
                        ImageCollectionState.submission_message,
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
                        on_click=ImageCollectionState.clear_message,
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
                    ImageCollectionState.submission_status == "success",
                    "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)"
                ),
                border=rx.cond(
                    ImageCollectionState.submission_status == "success",
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
                        ImageCollectionState.employees,
                        value=ImageCollectionState.selected_employee_id,
                        on_change=ImageCollectionState.set_selected_employee_id,
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
                        ImageCollectionState.projects,
                        value=ImageCollectionState.selected_project_id,
                        on_change=ImageCollectionState.set_selected_project_id,
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
                
                # Collection Date/Time
                rx.vstack(
                    rx.hstack(
                        rx.text("Collection Date & Time", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.input(
                        type="datetime-local",
                        value=ImageCollectionState.collection_date,
                        on_change=ImageCollectionState.set_collection_date,
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
            
            # Middle Section - Asset & Imaging Method
            rx.vstack(
                rx.text(
                    "Asset & Method",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Asset Selection
                rx.vstack(
                    rx.text("Asset", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        ImageCollectionState.assets,
                        value=ImageCollectionState.selected_asset_id,
                        on_change=ImageCollectionState.set_selected_asset_id,
                        placeholder="Select asset...",
                        disabled=rx.cond(ImageCollectionState.assets, False, True),
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
                
                # Imaging Method Selection
                rx.vstack(
                    rx.text("Imaging Method", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.select(
                        ImageCollectionState.imaging_methods,
                        value=ImageCollectionState.selected_imaging_method_id,
                        on_change=ImageCollectionState.set_selected_imaging_method_id,
                        placeholder="Select imaging method...",
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
            
            # Right Section - Image Details & Results
            rx.vstack(
                rx.text(
                    "Image Details & Results",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Image Size
                rx.vstack(
                    rx.text("Image Size (MB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.input(
                        value=ImageCollectionState.image_size_mb,
                        on_change=ImageCollectionState.set_image_size_mb,
                        placeholder="e.g., 1024.5",
                        type="number",
                        step="0.1",
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
                
                # Imaging Result
                rx.vstack(
                    rx.hstack(
                        rx.text("Imaging Result", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        ["Success", "Failed", "Partial Success", "In Progress", "Cancelled"],
                        value=ImageCollectionState.imaging_result,
                        on_change=ImageCollectionState.set_imaging_result,
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
                        value=ImageCollectionState.imaging_comments,
                        on_change=ImageCollectionState.set_imaging_comments,
                        placeholder="Optional notes about the imaging process...",
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
        
            key=ImageCollectionState.form_key,  # Force re-render on form reset
            width="90%",
            max_width="1400px",
            margin="0 auto",
            padding="2rem",
            border_radius="16px",
            background="linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
            border="1px solid rgba(255, 255, 255, 0.2)",
            backdrop_filter="blur(20px)",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
            on_mount=ImageCollectionState.load_form_data,
        ),
        
        spacing="0",
        width="100%",
    )