import reflex as rx

def Tickets() -> rx.Component:
    return rx.vstack(
        rx.heading("Ticket Management", size="8", color="white", margin_bottom="2em"),
        rx.text("Support Ticket System", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )