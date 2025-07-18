"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import os
import reflex as rx
import reflex_clerk_api as clerk
from dotenv import load_dotenv
import reflex_type_animation as ta

from rxconfig import config
from .pages import Dashboard, Dats, Images, Logs, Tickets, Assets, Playbook, Software, Vulnerabilities, Analytics
from .models import Employee, AppUser, Project, HardwareManufacturer, SWManufacturer, LogType, ImagingMethod, SysArchitecture, CPUType, GPUType
from .components import advanced_smoke_system, page_wrapper

load_dotenv()

# Configure JWT claims validation with proper leeway
clerk.ClerkState.set_claims_options({
    "iat": {"essential": False, "leeway": 31536000},
    "exp": {"essential": False, "leeway": 31536000},
    "nbf": {"essential": False, "leeway": 31536000}
})


class State(rx.State):
    """The app state."""
    mouse_x: int = 0
    mouse_y: int = 0

    def update_mouse_position(self, x: int, y: int):
        """Update mouse position for glow effect."""
        self.mouse_x = x
        self.mouse_y = y


def xai_navbar() -> rx.Component:
    """xAI-style navigation bar."""
    return rx.hstack(
        # Logo section
        rx.hstack(
            rx.html("""
            <div class="navbar-logo">
                <div class="nx-main">Nx.</div>
                <div class="iams-sub">IAMS</div>
            </div>
            <style>
            .navbar-logo {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                line-height: 1;
            }
            
            .nx-main {
                font-size: 1.5em;
                font-weight: 700;
                color: white;
                letter-spacing: -0.02em;
                margin-bottom: -0.1em;
            }
            
            .iams-sub {
                font-size: 0.85em;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.7);
                letter-spacing: 0.08em;
                text-transform: uppercase;
                margin-left: 0.1em;
                background: linear-gradient(90deg, 
                    rgba(255, 255, 255, 0.8) 0%, 
                    rgba(255, 255, 255, 0.5) 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                transition: all 0.3s ease;
            }
            
            .navbar-logo:hover .iams-sub {
                background: linear-gradient(90deg, 
                    rgba(255, 255, 255, 1) 0%, 
                    rgba(255, 255, 255, 0.8) 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                transform: translateX(2px);
            }
            </style>
            """),
            spacing="2",
        ),
        rx.spacer(),
        
        # Navigation links
        rx.hstack(
            rx.link("IAMS", href="/dashboard", color="gray.300", _hover={"color": "white"}, font_size="sm", font_weight="500"),
            rx.link("COMPLIANCE", href="#", color="gray.300", _hover={"color": "white"}, font_size="sm", font_weight="500"),
            rx.link("CYBER NEWS", href="#", color="gray.300", _hover={"color": "white"}, font_size="sm", font_weight="500"),
            spacing="6",
            display=["none", "none", "flex"],
        ),
        
        rx.spacer(),
        
        # Sign In/Dashboard Button
        clerk.signed_in(
            rx.link(
                rx.button(
                    "Dashboard",
                    bg="white",
                    color="black",
                    _hover={"bg": "gray.200", "transform": "translateY(-1px)"},
                    border_radius="full",
                    padding="0.75em 1.5em",
                    font_size="sm",
                    font_weight="600",
                    transition="all 0.2s ease",
                    box_shadow="0 4px 12px rgba(255, 255, 255, 0.1)",
                ),
                href="/dashboard",
            ),
        ),
        clerk.signed_out(
            clerk.sign_in_button(
                rx.button(
                    "Sign In",
                    bg="white",
                    color="black",
                    _hover={"bg": "gray.200", "transform": "translateY(-1px)"},
                    border_radius="full",
                    padding="0.75em 1.5em",
                    font_size="sm",
                    font_weight="600",
                    transition="all 0.2s ease",
                    box_shadow="0 4px 12px rgba(255, 255, 255, 0.1)",
                )
            ),
        ),
        
        # Mobile menu button
        rx.button(
            rx.icon(tag="hamburger", size=20),
            bg="transparent",
            color="white",
            display=["flex", "flex", "none"],
            _hover={"bg": "rgba(255, 255, 255, 0.1)"},
        ),
        
        width="100%",
        padding="1.5em 2em",
        position="fixed",
        top="0",
        left="0",
        z_index="1000",
        backdrop_filter="blur(20px)",
        border_bottom="1px solid rgba(255, 255, 255, 0.05)",
        background="rgba(0, 0, 0, 0.3)",
    )

def interactive_smoke_system() -> rx.Component:
    """TSParticles-based smoke system with thousands of particles and mouse interaction."""
    return advanced_smoke_system()

def hero_section() -> rx.Component:
    """Main hero section."""
    return rx.vstack(
        # Main title
        rx.box(
            rx.html("""
            <div class="hero-container">
                <div class="nx-backdrop">Nx</div>
                <div class="hero-text">IAMS</div>
            </div>
            <style>
            .hero-container {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1rem;
            }
            
            .nx-backdrop {
                position: absolute;
                font-size: clamp(8rem, 20vw, 20rem);
                font-weight: 900;
                color: rgba(255, 255, 255, 0.08);
                text-align: center;
                line-height: 0.9;
                letter-spacing: -0.02em;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                z-index: 1;
                transform: translateX(-15%) translateY(-20%);
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.1) 0%, 
                    rgba(255, 255, 255, 0.05) 50%, 
                    rgba(255, 255, 255, 0.02) 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
            }
            
            .hero-text {
                font-size: clamp(6rem, 15vw, 16rem);
                font-weight: 800;
                color: white;
                text-align: center;
                line-height: 0.9;
                letter-spacing: -0.02em;
                background: linear-gradient(180deg, 
                    #ffffff 0%, 
                    #f8fafc 25%, 
                    #e2e8f0 50%, 
                    #cbd5e1 75%, 
                    #94a3b8 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                position: relative;
                z-index: 2;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
            }
            
            @media (max-width: 768px) {
                .nx-backdrop {
                    font-size: clamp(5rem, 18vw, 12rem);
                }
                .hero-text {
                    font-size: clamp(4rem, 15vw, 8rem);
                }
            }
            </style>
            """),
            z_index="10",
        ),
        
        # Subtitle with type animation
        rx.box(
            ta.type_animation(
                sequence=[
                    "Next Generation Visibility",
                    2000,
                    "Next Generation Insight",
                    2000,
                    "Next Generation Industrial Asset Management System",
                    2000,
                ],
                wrapper="span",
                speed=50,
                repeat=True,
                style={
                    "fontSize": "clamp(1.5rem, 4vw, 3rem)",
                    "fontWeight": "600",
                    "color": "rgba(255, 255, 255, 0.9)",
                    "textAlign": "center",
                    "lineHeight": "1.2",
                    "background": "linear-gradient(135deg, #ffffff 0%, #f8fafc 25%, #e2e8f0 50%, #cbd5e1 75%, #94a3b8 100%)",
                    "backgroundClip": "text",
                    "WebkitBackgroundClip": "text",
                    "WebkitTextFillColor": "transparent",
                    "textShadow": "0 0 20px rgba(255, 255, 255, 0.3)",
                }
            ),
            text_align="center",
            margin_bottom="3em",
        ),
        
        # Conditional content based on auth status
        clerk.signed_in(
            rx.vstack(
                rx.text(
                    f"Welcome back, {clerk.ClerkUser.first_name}!",
                    font_size="xl",
                    color="white",
                    text_align="center",
                    margin_bottom="2em",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Dashboard",
                            bg="white",
                            color="black",
                            _hover={"bg": "gray.100", "transform": "translateY(-2px)"},
                            border_radius="full",
                            padding="1em 2em",
                            font_size="lg",
                            font_weight="600",
                            transition="all 0.3s ease",
                        ),
                        href="/dashboard",
                    ),
                    rx.link(
                        rx.button(
                            "Assets",
                            bg="transparent",
                            color="white",
                            border="1px solid rgba(255, 255, 255, 0.3)",
                            _hover={"bg": "rgba(255, 255, 255, 0.1)", "transform": "translateY(-2px)"},
                            border_radius="full",
                            padding="1em 2em",
                            font_size="lg",
                            font_weight="600",
                            transition="all 0.3s ease",
                        ),
                        href="/assets",
                    ),
                    spacing="3",
                ),
                clerk.sign_out_button(
                    rx.button(
                        "Sign Out",
                        bg="transparent",
                        color="gray.400",
                        _hover={"color": "white"},
                        margin_top="2em",
                        font_size="sm",
                    )
                ),
                spacing="4",
                align="center",
            )
        ),
        clerk.signed_out(
            rx.vstack(
                clerk.sign_in_button(
                    rx.button(
                        "Get Started",
                        bg="white",
                        color="black",
                        _hover={
                            "bg": "gray.100",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 8px 25px rgba(255, 255, 255, 0.15)",
                        },
                        border_radius="full",
                        padding="1em 2.5em",
                        font_size="lg",
                        font_weight="600",
                        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                        box_shadow="0 4px 20px rgba(255, 255, 255, 0.1)",
                    )
                ),
                rx.text(
                    "Don't have an account?",
                    color="gray.400",
                    font_size="sm",
                    margin_top="1em",
                ),
                clerk.sign_up_button(
                    rx.button(
                        "Sign Up",
                        bg="transparent",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        _hover={"bg": "rgba(255, 255, 255, 0.1)"},
                        border_radius="full",
                        padding="0.75em 1.5em",
                        font_size="md",
                        font_weight="500",
                    )
                ),
                spacing="3",
                align="center",
            )
        ),
        
        spacing="4",
        align="center",
        justify="center",
        width="100%",
        z_index="10",
        position="relative",
    )

def index() -> rx.Component:
    # xAI-style Landing Page with Authentication
    return clerk.clerk_provider(
        clerk.clerk_loaded(
            # If signed in, show content with redirect
            clerk.signed_in(
                rx.box(
                    rx.vstack(
                        rx.text("Welcome back!", color="white", font_size="2xl"),
                        rx.text("Redirecting to dashboard...", color="gray.300"),
                        rx.spinner(size="3", color="white"),
                        rx.link(
                            rx.button("Go to Dashboard", color_scheme="blue"),
                            href="/dashboard",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    width="100%",
                    height="100vh",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    background="radial-gradient(circle at 50% 0%, rgba(20, 20, 20, 1) 0%, rgba(0, 0, 0, 1) 100%)",
                ),
                rx.script("""
                    console.log('User is signed in, attempting redirect...');
                    setTimeout(() => {
                        console.log('Executing redirect to dashboard...');
                        console.log('Current URL:', window.location.href);
                        try {
                            window.location.replace('/dashboard');
                        } catch (e) {
                            console.error('Redirect failed:', e);
                            // Fallback method
                            window.location.href = '/dashboard';
                        }
                    }, 1000);
                """)
            ),
            # If signed out, show landing page
            clerk.signed_out(
                landing_page_content()
            )
        ),
        clerk.clerk_loading(
            rx.center(
                rx.vstack(
                    rx.spinner(size="3", color="white"),
                    rx.text("Loading...", color="white"),
                    spacing="4",
                    align="center",
                ),
                width="100%",
                height="100vh",
                background="radial-gradient(circle at 50% 0%, rgba(20, 20, 20, 1) 0%, rgba(0, 0, 0, 1) 100%)",
            )
        ),
        publishable_key=os.environ["CLERK_PUBLISHABLE_KEY"],
        secret_key=os.environ["CLERK_SECRET_KEY"],
        register_user_state=True,
    )

def landing_page_content() -> rx.Component:
    """The main landing page content for signed-out users."""
    return rx.box(
        # Global CSS for Clerk components
        rx.html("""
        <style>
            .cl-userButtonPopoverCard {
                background: #1a1a1a !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 0.5rem !important;
                color: #ffffff !important;
            }
            
            .cl-userButtonPopoverActionButton {
                color: #ffffff !important;
                background-color: transparent !important;
            }
            
            .cl-userButtonPopoverActionButton:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            
            .cl-userButtonPopoverActionButtonText {
                color: #ffffff !important;
            }
            
            .cl-userButtonPopoverActionButtonIcon {
                color: #ffffff !important;
            }
            
            .cl-userPreviewTextContainer {
                color: #ffffff !important;
            }
            
            .cl-userPreviewSecondaryIdentifier {
                color: #cccccc !important;
            }
            
            .cl-userButtonPopoverFooter {
                background: #0a0a0a !important;
                border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Additional selectors for different Clerk versions */
            [data-clerk-element="userButtonPopoverCard"] {
                background: #1a1a1a !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 0.5rem !important;
                color: #ffffff !important;
            }
            
            [data-clerk-element="userButtonPopoverActionButton"] {
                color: #ffffff !important;
                background-color: transparent !important;
            }
            
            [data-clerk-element="userButtonPopoverActionButton"]:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            
            [data-clerk-element="userButtonPopoverActionButtonText"] {
                color: #ffffff !important;
            }
            
            [data-clerk-element="userButtonPopoverActionButtonIcon"] {
                color: #ffffff !important;
            }
            
            [data-clerk-element="userPreviewTextContainer"] {
                color: #ffffff !important;
            }
            
            [data-clerk-element="userPreviewSecondaryIdentifier"] {
                color: #cccccc !important;
            }
            
            [data-clerk-element="userButtonPopoverFooter"] {
                background: #0a0a0a !important;
                border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
        </style>
        """),
            # Clean dark background
            rx.box(
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background="radial-gradient(circle at 50% 0%, rgba(20, 20, 20, 1) 0%, rgba(0, 0, 0, 1) 100%)",
                z_index="-3",
            ),
            
            # Subtle gradient overlay
            rx.box(
                position="absolute",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background="radial-gradient(ellipse 100% 40% at 50% 0%, rgba(255, 255, 255, 0.02) 0%, transparent 50%)",
                z_index="-2",
            ),
            
            # Mouse-following glow effect
            rx.box(
                id="mouse-glow",
                position="fixed",
                top="50%",
                left="50%",
                width="600px",
                height="600px",
                background="radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 30%, rgba(255, 255, 255, 0.05) 60%, transparent 100%)",
                border_radius="50%",
                pointer_events="none",
                z_index="-1",
                transform="translate(-50%, -50%)",
                transition="all 0.1s ease-out",
                style={
                    "filter": "blur(1px)",
                    "box-shadow": "0 0 100px rgba(255, 255, 255, 0.05)",
                }
            ),
            
            # JavaScript for mouse tracking
            rx.script("""
                document.addEventListener('mousemove', function(e) {
                    const glow = document.getElementById('mouse-glow');
                    if (glow) {
                        glow.style.left = e.clientX + 'px';
                        glow.style.top = e.clientY + 'px';
                    }
                });
            """),
            
            # Interactive smoke system
            interactive_smoke_system(),
            
            # Navigation
            xai_navbar(),
            
            # Loading state
            clerk.clerk_loading(
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color="white"),
                        rx.text("Loading...", color="white"),
                        spacing="4",
                        align="center",
                    ),
                    width="100%",
                    height="100vh",
                )
            ),
            
            # Main content
            clerk.clerk_loaded(
                rx.center(
                    hero_section(),
                    width="100%",
                    height="100vh",
                    padding="0 2em",
                )
            ),
            
            width="100%",
            height="100vh",
            overflow="hidden",
            position="relative",
        )


def protected_page(page_component):
    """Wrap a page component with authentication protection."""
    def wrapped_page() -> rx.Component:
        return clerk.clerk_provider(
            clerk.clerk_loaded(
                clerk.signed_in(
                    page_wrapper(
                        page_component()
                    )
                ),
                clerk.signed_out(
                    page_wrapper(
                        rx.vstack(
                            rx.heading("Access Denied", size="6", color="white"),
                            rx.text("Please sign in to access this page.", color="gray.300"),
                            rx.link(
                                rx.button("Go to Home", color_scheme="blue"),
                                href="/",
                            ),
                            spacing="4",
                            align="center",
                            justify="center",
                            min_height="85vh",
                        )
                    )
                ),
            ),
            clerk.clerk_loading(
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3", color="white"),
                        rx.text("Loading...", color="white"),
                        spacing="4",
                        align="center",
                    ),
                    width="100%",
                    height="100vh",
                    background="radial-gradient(circle at 50% 0%, rgba(20, 20, 20, 1) 0%, rgba(0, 0, 0, 1) 100%)",
                )
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
app.add_page(protected_page(Analytics), route="/analytics")
