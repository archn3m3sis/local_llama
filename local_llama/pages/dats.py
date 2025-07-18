import reflex as rx

def Dats() -> rx.Component:
    return rx.vstack(
        rx.heading("DAT Management", size="8", color="white", margin_bottom="2em"),
        rx.text("DAT File Management System", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )
