"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import os
import reflex as rx
import reflex_clerk_api as clerk
from dotenv import load_dotenv

from rxconfig import config
from .pages import Dashboard, Dats, Images, Logs, Tickets, Assets, Playbook, Software, Vulnerabilities
from .models import Employee, AppUser, Project, HardwareManufacturer, SWManufacturer

load_dotenv()

class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index) with Authentication
    return clerk.clerk_provider(
        rx.container(
            rx.color_mode.button(position="top-right"),
            clerk.clerk_loading(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Loading..."),
                    spacing="4",
                    align="center",
                    justify="center",
                    min_height="85vh",
                )
            ),
            clerk.clerk_loaded(
                clerk.signed_in(
                    rx.vstack(
                        rx.heading("Welcome to IAMS!", size="9"),
                        rx.text("Industrial Asset Management System", size="5"),
                        rx.text(f"Hello, {clerk.ClerkUser.first_name}!", size="4"),
                        rx.hstack(
                            rx.link(
                                rx.button("Dashboard", color_scheme="blue"),
                                href="/dashboard",
                            ),
                            rx.link(
                                rx.button("Assets", color_scheme="green"),
                                href="/assets",
                            ),
                            rx.link(
                                rx.button("Tickets", color_scheme="orange"),
                                href="/tickets",
                            ),
                            spacing="4",
                        ),
                        clerk.sign_out_button(
                            rx.button("Sign Out", color_scheme="red", variant="soft")
                        ),
                        spacing="5",
                        align="center",
                        justify="center",
                        min_height="85vh",
                    )
                ),
                clerk.signed_out(
                    rx.vstack(
                        rx.heading("Welcome to IAMS!", size="9"),
                        rx.text("Industrial Asset Management System", size="5"),
                        rx.text("Please sign in to access the system.", size="4"),
                        clerk.sign_in_button(
                            rx.button("Sign In", color_scheme="blue", size="3")
                        ),
                        rx.text("Don't have an account?", size="3"),
                        clerk.sign_up_button(
                            rx.button("Sign Up", color_scheme="green", variant="soft")
                        ),
                        spacing="5",
                        align="center",
                        justify="center",
                        min_height="85vh",
                    )
                ),
            ),
        ),
        publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
        secret_key=os.environ["CLERK_SECRET_KEY"],
        register_user_state=True,
    )


def protected_page(page_component):
    """Wrap a page component with authentication protection."""
    def wrapped_page() -> rx.Component:
        return clerk.clerk_provider(
            clerk.clerk_loaded(
                clerk.signed_in(
                    page_component()
                ),
                clerk.signed_out(
                    rx.vstack(
                        rx.heading("Access Denied", size="6"),
                        rx.text("Please sign in to access this page."),
                        rx.link(
                            rx.button("Go to Home", color_scheme="blue"),
                            href="/",
                        ),
                        spacing="4",
                        align="center",
                        justify="center",
                        min_height="85vh",
                    )
                ),
            ),
            publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
            secret_key=os.environ["CLERK_SECRET_KEY"],
            register_user_state=True,
        )
    return wrapped_page

app = rx.App()
app.add_page(index, route="/")

# Add protected pages
app.add_page(protected_page(Dashboard), route="/dashboard")
app.add_page(protected_page(Dats), route="/dats")
app.add_page(protected_page(Images), route="/images")
app.add_page(protected_page(Logs), route="/logs")
app.add_page(protected_page(Tickets), route="/tickets")
app.add_page(protected_page(Assets), route="/assets")
app.add_page(protected_page(Playbook), route="/playbook")
app.add_page(protected_page(Software), route="/software")
app.add_page(protected_page(Vulnerabilities), route="/vulnerabilities")
