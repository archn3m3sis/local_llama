import reflex as rx
from ..states.file_storage_state import FileStorageState


def modern_progress_bar() -> rx.Component:
    """Create a modern animated progress bar for file uploads."""
    return rx.box(
        rx.box(
            rx.box(
                rx.box(
                    width=f"{FileStorageState.upload_progress}%",
                    height="100%",
                    background="linear-gradient(90deg, #3b82f6 0%, #60a5fa 50%, #3b82f6 100%)",
                    background_size="200% 100%",
                    border_radius="12px",
                    transition="width 0.3s ease-out",
                    animation="shimmer 2s linear infinite",
                    box_shadow="0 0 20px rgba(59, 130, 246, 0.5)",
                    style={
                        "@keyframes shimmer": {
                            "0%": {"backgroundPosition": "-200% 0"},
                            "100%": {"backgroundPosition": "200% 0"}
                        }
                    }
                ),
                # Progress particles
                rx.box(
                    rx.html("""
                    <div class="progress-particles">
                        <span class="particle"></span>
                        <span class="particle"></span>
                        <span class="particle"></span>
                        <span class="particle"></span>
                    </div>
                    <style>
                    .progress-particles {
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        top: 0;
                        left: 0;
                        pointer-events: none;
                    }
                    .particle {
                        position: absolute;
                        width: 4px;
                        height: 4px;
                        background: #60a5fa;
                        border-radius: 50%;
                        top: 50%;
                        opacity: 0;
                    }
                    .particle:nth-child(1) {
                        left: 10%;
                        animation: float-particle 3s ease-out infinite;
                    }
                    .particle:nth-child(2) {
                        left: 30%;
                        animation: float-particle 3s ease-out infinite 0.5s;
                    }
                    .particle:nth-child(3) {
                        left: 60%;
                        animation: float-particle 3s ease-out infinite 1s;
                    }
                    .particle:nth-child(4) {
                        left: 85%;
                        animation: float-particle 3s ease-out infinite 1.5s;
                    }
                    @keyframes float-particle {
                        0% {
                            transform: translateY(0) scale(0);
                            opacity: 0;
                        }
                        20% {
                            transform: translateY(-20px) scale(1);
                            opacity: 1;
                        }
                        100% {
                            transform: translateY(-60px) scale(0);
                            opacity: 0;
                        }
                    }
                    </style>
                    """),
                    position="absolute",
                    width="100%",
                    height="100%",
                    top="0",
                    left="0",
                ),
                position="relative",
                width="100%",
                height="12px",
                background="rgba(59, 130, 246, 0.1)",
                border_radius="12px",
                overflow="hidden",
                box_shadow="inset 0 2px 4px rgba(0, 0, 0, 0.1)",
            ),
            # Progress info
            rx.hstack(
                rx.text(
                    f"{FileStorageState.upload_progress}%",
                    font_size="1.25rem",
                    font_weight="700",
                    color="blue.400",
                    text_shadow="0 0 20px rgba(59, 130, 246, 0.5)",
                ),
                rx.spacer(),
                rx.text(
                    FileStorageState.upload_status,
                    font_size="0.875rem",
                    color="gray.400",
                    font_weight="500",
                ),
                width="100%",
                align="center",
                margin_top="0.75rem",
                padding="0 0.25rem",
            ),
            width="100%",
        ),
        width="100%",
        padding="1rem 0",
    )


def file_upload_progress_card() -> rx.Component:
    """Modern progress card showing individual file upload progress."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("file", size=20, color="blue.400"),
                rx.text(
                    FileStorageState.current_upload_filename,
                    size="2",
                    weight="medium",
                    color="white",
                    max_width="200px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
                rx.spacer(),
                rx.text(
                    FileStorageState.current_file_size_display,
                    size="1",
                    color="gray.400",
                ),
                width="100%",
                align="center",
                spacing="2",
            ),
            modern_progress_bar(),
            spacing="3",
            width="100%",
        ),
        background="rgba(20, 20, 20, 0.8)",
        border="1px solid rgba(59, 130, 246, 0.2)",
        border_radius="lg",
        padding="1.5rem",
        width="100%",
        max_width="500px",
        box_shadow="0 4px 20px rgba(0, 0, 0, 0.4)",
        backdrop_filter="blur(10px)",
    )