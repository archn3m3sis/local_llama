import reflex as rx 

def Vulnerabilities() -> rx.Component:
    return rx.vstack(
        rx.heading("Vulnerability Management", size="8", color="white", margin_bottom="2em"),
        rx.text("Security Vulnerability Tracking", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )
