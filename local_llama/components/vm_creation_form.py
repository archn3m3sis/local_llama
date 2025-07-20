import reflex as rx
from ..states.vm_state import VMState


def vm_creation_form() -> rx.Component:
    """Modern glass morphism VM creation form component."""
    return rx.vstack(
        
        # Success/Error Messages
        rx.cond(
            VMState.submission_message != "",
            rx.box(
                rx.hstack(
                    rx.icon(
                        tag=rx.cond(
                            VMState.submission_status == "success",
                            "check",
                            "alert_circle"
                        ),
                        size=20,
                        color=rx.cond(
                            VMState.submission_status == "success",
                            "rgba(34, 197, 94, 0.9)",
                            "rgba(239, 68, 68, 0.9)"
                        ),
                    ),
                    rx.text(
                        VMState.submission_message,
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
                    VMState.submission_status == "success",
                    "linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%)",
                    "linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%)"
                ),
                border=rx.cond(
                    VMState.submission_status == "success",
                    "1px solid rgba(34, 197, 94, 0.3)",
                    "1px solid rgba(239, 68, 68, 0.3)"
                ),
                custom_attrs={"data-toast-container": "true"},
                margin_bottom="1rem",
            ),
        ),
        
        # Auto-fade JavaScript for toast notifications
        rx.script(
            """
            (function() {
                let vmFadeTimer = null;
                
                const vmCheckAndFade = () => {
                    const toastContainer = document.querySelector('[data-toast-container]');
                    const message = document.querySelector('[data-toast-message]');
                    
                    if (toastContainer && message && message.textContent.includes('successfully')) {
                        // Clear any existing timer
                        if (vmFadeTimer) clearTimeout(vmFadeTimer);
                        
                        // Set new timer to fade out the toast
                        vmFadeTimer = setTimeout(() => {
                            toastContainer.style.transition = 'opacity 0.5s ease-out';
                            toastContainer.style.opacity = '0';
                            setTimeout(() => {
                                toastContainer.style.display = 'none';
                            }, 500);
                        }, 5000);
                    }
                };
                
                // Run check when page loads and when content changes
                vmCheckAndFade();
                const observer = new MutationObserver(vmCheckAndFade);
                observer.observe(document.body, { childList: true, subtree: true });
            })();
            """
        ),
        
        rx.box(
        rx.hstack(
            # Left Section - Asset & Project Selection
            rx.vstack(
                rx.text(
                    "Asset & Project",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Asset Selection
                rx.vstack(
                    rx.hstack(
                        rx.text("Asset", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.assets,
                        value=VMState.selected_asset_id,
                        on_change=VMState.set_asset,
                        placeholder="Select asset...",
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
                    rx.hstack(
                        rx.text("Project", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.projects,
                        value=VMState.selected_project_id,
                        on_change=VMState.set_project,
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
                
                # Image Collection Selection
                rx.vstack(
                    rx.hstack(
                        rx.text("Base Image", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.image_collections,
                        value=VMState.selected_imgcollection_id,
                        on_change=VMState.set_imgcollection,
                        placeholder="Select base image...",
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
                
                flex="1",
                spacing="1.5rem",
                padding="1.5rem",
                align="start",
                width="100%",
            ),
            
            # Middle Section - VM Configuration
            rx.vstack(
                rx.text(
                    "VM Configuration",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Virtualization Source
                rx.vstack(
                    rx.hstack(
                        rx.text("Virtualization Server", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.virtualization_sources,
                        value=VMState.selected_virtsource_id,
                        on_change=VMState.set_virtsource,
                        placeholder="Select virtualization server...",
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
                
                # VM Type
                rx.vstack(
                    rx.hstack(
                        rx.text("VM Type", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.vm_types,
                        value=VMState.selected_vmtype_id,
                        on_change=VMState.set_vmtype,
                        placeholder="Select VM type...",
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
                
                # VM Status
                rx.vstack(
                    rx.hstack(
                        rx.text("VM Status", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.vm_statuses,
                        value=VMState.selected_vmstatus_id,
                        on_change=VMState.set_vmstatus,
                        placeholder="Select VM status...",
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
                
                flex="1",
                spacing="1.5rem",
                padding="1.5rem",
                align="start",
                width="100%",
            ),
            
            # Right Section - VM Specifications & Scans
            rx.vstack(
                rx.text(
                    "Specifications & Scans",
                    font_size="1.1rem",
                    font_weight="600",
                    color="white",
                    margin_bottom="1rem",
                ),
                
                # Creator Employee
                rx.vstack(
                    rx.hstack(
                        rx.text("Created By", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                        rx.text("*", color="red", font_size="0.9rem"),
                        spacing="1",
                    ),
                    rx.select(
                        VMState.employees,
                        value=VMState.selected_creator_employee_id,
                        on_change=VMState.set_creator_employee,
                        placeholder="Select creator...",
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
                
                # RAM
                rx.vstack(
                    rx.text("RAM (GB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.input(
                        type="number",
                        placeholder="Enter RAM in GB...",
                        value=VMState.ram_gb,
                        on_change=VMState.set_ram_gb,
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
                
                # CPU Cores
                rx.vstack(
                    rx.text("CPU Cores", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.input(
                        type="number",
                        placeholder="Enter CPU cores...",
                        value=VMState.cpu_cores,
                        on_change=VMState.set_cpu_cores,
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
                
                # Disk Size
                rx.vstack(
                    rx.text("Disk Size (GB)", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.input(
                        type="number",
                        placeholder="Enter disk size in GB...",
                        value=VMState.disk_size_gb,
                        on_change=VMState.set_disk_size_gb,
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
                
                # Scan Checkboxes
                rx.vstack(
                    rx.text("Security Scans", color="rgba(255, 255, 255, 0.8)", font_size="0.9rem"),
                    rx.hstack(
                        rx.checkbox(
                            "ACAS Scan Completed",
                            checked=VMState.acas_scan_completed,
                            on_change=VMState.set_acas_scan,
                            color_scheme="green",
                        ),
                        rx.checkbox(
                            "SCAP Scan Completed",
                            checked=VMState.scap_scan_completed,
                            on_change=VMState.set_scap_scan,
                            color_scheme="green",
                        ),
                        direction="column",
                        spacing="2",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                flex="1",
                spacing="1.5rem",
                padding="1.5rem",
                align="start",
                width="100%",
            ),
            
            width="100%",
            align="start",
        ),
        
        # Glass morphism styling
        background="linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)",
        backdrop_filter="blur(20px)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="20px",
        box_shadow="0 8px 32px rgba(0, 0, 0, 0.12)",
        width="90%",
        max_width="1400px",
        margin="0 auto",
        key=VMState.form_key,
        ),
        
        width="100%",
        spacing="0",
        on_mount=VMState.load_form_data,
    )