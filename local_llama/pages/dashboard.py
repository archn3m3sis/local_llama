import reflex as rx

def Dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard", size="8", color="white", margin_bottom="2em"),
        rx.text("Welcome to the IAMS Dashboard", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )