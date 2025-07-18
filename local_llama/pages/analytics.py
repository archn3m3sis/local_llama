import reflex as rx

def Analytics() -> rx.Component:
    return rx.vstack(
        rx.heading("Analytics", size="8", color="white", margin_bottom="2em"),
        rx.text("Analytics and Reporting Dashboard", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )
