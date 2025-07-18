import reflex as rx

def Playbook() -> rx.Component:
    return rx.vstack(
        rx.heading("Playbooks", size="8", color="white", margin_bottom="2em"),
        rx.text("Documentation and Playbooks", color="gray.300", font_size="lg"),
        spacing="4",
        align="center",
        padding="2em",
        min_height="100vh",
        justify="center"
    )