"""Virtual Machine Creation Form Component."""
import reflex as rx
from ..states.vm_creation_state import VMCreationState
from .ram_slider_dialog import ram_slider_dialog
from .disk_slider_dialog import disk_slider_dialog

def vm_creation_form() -> rx.Component:
    """Virtual Machine Creation form component."""
    return rx.vstack(
        # Success/Error Messages
        rx.cond(
            VMCreationState.submission_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag=rx.cond(
                            VMCreationState.submission_status == "success",
                            "check",
                            "alert_circle"
                        ),
                        size=20,
                        color=rx.cond(
                            VMCreationState.submission_status == "success",
                            "rgba(34, 197, 94, 0.9)",
                            "rgba(239, 68, 68, 0.9)"
                        ),
                    ),
                    rx.text(
                        VMCreationState.submission_message,
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
                        on_click=VMCreationState.clear_message,
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
                    VMCreationState.submission_status == "success",
                    "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)"
                ),
                border=rx.cond(
                    VMCreationState.submission_status == "success",
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
                            VMCreationState.employees,
                            placeholder="Select employee...",
                            value=VMCreationState.selected_employee,
                            on_change=VMCreationState.set_employee,
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
                            VMCreationState.projects,
                            placeholder="Select project...",
                            value=VMCreationState.selected_project,
                            on_change=VMCreationState.set_project,
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
                    
                    # Virtualization Source
                    rx.vstack(
                        rx.text("Virtualization Source", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.select(
                            VMCreationState.virt_sources,
                            placeholder="Select source...",
                            value=VMCreationState.selected_virt_source,
                            on_change=VMCreationState.set_virt_source,
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
                
                # Middle Section - Asset & VM Config
                rx.vstack(
                    rx.text(
                        "Asset & VM Configuration",
                        font_size="1.1rem",
                        font_weight="600",
                        color="white",
                        margin_bottom="1rem",
                    ),
                    
                    # Asset Selection
                    rx.vstack(
                        rx.text("Asset", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.select(
                            VMCreationState.filtered_assets,
                            placeholder="Select asset...",
                            value=VMCreationState.selected_asset,
                            on_change=VMCreationState.set_asset,
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "white",
                                "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                            },
                            disabled=VMCreationState.selected_project == "",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    
                    # Image Collection Selection
                    rx.vstack(
                        rx.text("Image Collection", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.select(
                            VMCreationState.filtered_image_collections,
                            placeholder="Select image collection...",
                            value=VMCreationState.selected_image_collection,
                            on_change=VMCreationState.set_image_collection,
                            width="100%",
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.2)",
                                "color": "white",
                                "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                            },
                            disabled=VMCreationState.selected_asset == "",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    
                    # VM Type and Status
                    rx.hstack(
                        rx.vstack(
                            rx.text("VM Type", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                            rx.select(
                                VMCreationState.vm_types,
                                placeholder="Select type...",
                                value=VMCreationState.selected_vm_type,
                                on_change=VMCreationState.set_vm_type,
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
                        rx.vstack(
                            rx.text("VM Status", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                            rx.select(
                                VMCreationState.vm_statuses,
                                placeholder="Select status...",
                                value=VMCreationState.selected_vm_status,
                                on_change=VMCreationState.set_vm_status,
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
                        spacing="3",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                
                # Right Section - VM Specifications
                rx.vstack(
                    rx.text(
                        "VM Specifications",
                        font_size="1.1rem",
                        font_weight="600",
                        color="white",
                        margin_bottom="1rem",
                    ),
                    
                    # Hardware Specs
                    rx.hstack(
                        rx.vstack(
                            rx.text("RAM (MB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                            rx.input(
                                placeholder="16384",
                                value=VMCreationState.ram_mb,
                                on_change=VMCreationState.set_ram_mb,
                                on_focus=VMCreationState.open_ram_dialog,
                                width="100%",
                                type="number",
                                min="1",
                                style={
                                    "background": "rgba(255, 255, 255, 0.05)",
                                    "border": "1px solid rgba(255, 255, 255, 0.2)",
                                    "color": "white",
                                    "cursor": "pointer",
                                    "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                                    "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                                },
                            ),
                            width="100%",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.text("CPU Cores", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                            rx.input(
                                placeholder="4",
                                value=VMCreationState.cpu_cores,
                                on_change=VMCreationState.set_cpu_cores,
                                width="100%",
                                type="number",
                                min="1",
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
                        rx.vstack(
                            rx.text("Disk (MB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                            rx.input(
                                placeholder="262144",
                                value=VMCreationState.disk_size_mb,
                                on_change=VMCreationState.set_disk_size_mb,
                                on_focus=VMCreationState.open_disk_dialog,
                                width="100%",
                                type="number",
                                min="1",
                                style={
                                    "background": "rgba(255, 255, 255, 0.05)",
                                    "border": "1px solid rgba(255, 255, 255, 0.2)",
                                    "color": "white",
                                    "cursor": "pointer",
                                    "_focus": {"border": "1px solid rgba(59, 130, 246, 0.5)"},
                                    "_placeholder": {"color": "rgba(255, 255, 255, 0.4)"},
                                },
                            ),
                            width="100%",
                            spacing="2",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    
                    # Security Scans
                    rx.vstack(
                        rx.text("Security Scans", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.vstack(
                            rx.hstack(
                                rx.checkbox(
                                    checked=VMCreationState.acas_scan_completed,
                                    on_change=VMCreationState.toggle_acas_scan,
                                    color_scheme="green",
                                ),
                                rx.text("ACAS Scan Completed", color="rgba(255, 255, 255, 0.8)", font_size="0.85rem"),
                                spacing="2",
                                align="center",
                            ),
                            rx.hstack(
                                rx.checkbox(
                                    checked=VMCreationState.scap_scan_completed,
                                    on_change=VMCreationState.toggle_scap_scan,
                                    color_scheme="green",
                                ),
                                rx.text("SCAP Scan Completed", color="rgba(255, 255, 255, 0.8)", font_size="0.85rem"),
                                spacing="2",
                                align="center",
                            ),
                            spacing="2",
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
            
            key=VMCreationState.form_key,  # Force re-render on form reset
            width="90%",
            max_width="1400px",
            margin="0 auto",
            padding="2rem",
            border_radius="16px",
            background="linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
            border="1px solid rgba(255, 255, 255, 0.2)",
            backdrop_filter="blur(20px)",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.3)",
            on_mount=VMCreationState.load_dropdowns,
        ),
        
        # RAM Slider Dialog
        ram_slider_dialog(),
        
        # Disk Slider Dialog
        disk_slider_dialog(),
        
        spacing="0",
        width="100%",
    )