import reflex as rx

def Images() -> rx.Component:
    return rx.vstack(
        rx.heading("Image Management", size="8", color="white", margin_bottom="2em"),
        rx.text("Image Storage and Management", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )