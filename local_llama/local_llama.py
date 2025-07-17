"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages import Dashboard, Dats, Images, Logs, Tickets, Assets, Playbook

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(Dashboard, route="/dashboard")
app.add_page(Dats, route="/dats")
app.add_page(Images, route="/images")
app.add_page(Logs, route="/logs")
app.add_page(Tickets, route="/tickets")
app.add_page(Assets, route="/assets")
app.add_page(Playbook, route="/playbook")