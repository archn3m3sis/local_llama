"""Universal background component with particles and mouse glow for all pages."""

import reflex as rx
import reflex_clerk_api as clerk
from .smoke_system import advanced_smoke_system
from .radial_speed_dial import radial_speed_dial, analytics_speed_dial, asset_data_speed_dial, playbook_speed_dial, vault_speed_dial, right_side_buttons


def universal_background() -> rx.Component:
    """Universal background with particles and mouse glow effect."""
    return rx.box(
        # Clean dark background
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="radial-gradient(circle at 50% 0%, rgba(20, 20, 20, 1) 0%, rgba(0, 0, 0, 1) 100%)",
            z_index="-3",
        ),
        
        # Subtle gradient overlay
        rx.box(
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="radial-gradient(ellipse 100% 40% at 50% 0%, rgba(255, 255, 255, 0.02) 0%, transparent 50%)",
            z_index="-2",
        ),
        
        # Mouse-following glow effect
        rx.box(
            id="mouse-glow",
            position="fixed",
            top="0",
            left="0",
            width="400px",
            height="400px",
            background="radial-gradient(ellipse 120% 80% at center, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 40%, rgba(255, 255, 255, 0.02) 70%, transparent 100%)",
            border_radius="50%",
            pointer_events="none",
            z_index="-1",
            transform="translate(-200px, -200px)",
            style={
                "filter": "blur(3px)",
                "box-shadow": "0 0 150px rgba(255, 255, 255, 0.02)",
                "will-change": "transform",
            }
        ),
        
        # JavaScript for mouse tracking and Clerk popup styling
        rx.script("""
            (function() {
                // Throttled mouse movement for better performance
                let mouseTimeout;
                let lastMouseMove = 0;
                const MOUSE_THROTTLE = 16; // ~60fps
                
                document.addEventListener('mousemove', function(e) {
                const now = Date.now();
                if (now - lastMouseMove < MOUSE_THROTTLE) return;
                lastMouseMove = now;
                
                const glow = document.getElementById('mouse-glow');
                if (glow) {
                    // Use transform instead of left/top for better performance
                    glow.style.transform = `translate(${e.clientX - 200}px, ${e.clientY - 200}px)`;
                }
            });
            
            // Function to style Clerk popup elements
            function styleClerkPopup() {
                // Wait for popup to be rendered
                setTimeout(() => {
                    // Try multiple selectors to find the popup
                    const selectors = [
                        '.cl-userButtonPopoverCard',
                        '[data-clerk-element="userButtonPopoverCard"]',
                        '.cl-popoverCard',
                        '[role="dialog"]',
                        '.cl-card'
                    ];
                    
                    let popup = null;
                    for (let selector of selectors) {
                        popup = document.querySelector(selector);
                        if (popup) break;
                    }
                    
                    if (popup) {
                        // Style the popup card
                        popup.style.background = '#1a1a1a !important';
                        popup.style.border = '1px solid rgba(255, 255, 255, 0.2) !important';
                        popup.style.borderRadius = '0.5rem !important';
                        popup.style.color = '#ffffff !important';
                        
                        // Find and style all text elements
                        const textElements = popup.querySelectorAll('*');
                        textElements.forEach(el => {
                            const computedStyle = window.getComputedStyle(el);
                            if (computedStyle.color && computedStyle.color.includes('rgb(0, 0, 0)')) {
                                el.style.color = '#ffffff !important';
                            }
                        });
                        
                        // Style buttons
                        const buttons = popup.querySelectorAll('button, [role="button"]');
                        buttons.forEach(button => {
                            button.style.color = '#ffffff !important';
                            button.style.backgroundColor = 'transparent !important';
                            button.addEventListener('mouseenter', () => {
                                button.style.backgroundColor = 'rgba(255, 255, 255, 0.1) !important';
                            });
                            button.addEventListener('mouseleave', () => {
                                button.style.backgroundColor = 'transparent !important';
                            });
                        });
                        
                        console.log('Clerk popup styled successfully');
                    } else {
                        console.log('Clerk popup not found');
                    }
                }, 100);
            }
            
            // Monitor for popup opening
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            if (node.classList && (
                                node.classList.contains('cl-userButtonPopoverCard') ||
                                node.classList.contains('cl-popoverCard') ||
                                node.classList.contains('cl-card') ||
                                node.getAttribute('data-clerk-element') === 'userButtonPopoverCard'
                            )) {
                                styleClerkPopup();
                            }
                            // Also check children
                            if (node.querySelector && node.querySelector('.cl-userButtonPopoverCard, .cl-popoverCard, .cl-card, [data-clerk-element="userButtonPopoverCard"]')) {
                                styleClerkPopup();
                            }
                        }
                    });
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            // Also try to style any existing popups
            styleClerkPopup();
            })();
        """),
        
        
        # Interactive smoke/particle system
        advanced_smoke_system(),
        
        # Radial speed dial navigation
        radial_speed_dial(),
        
        # Analytics speed dial
        analytics_speed_dial(),
        
        # Asset Data speed dial
        asset_data_speed_dial(),
        
        # Playbook speed dial
        playbook_speed_dial(),
        
        # Vault speed dial
        vault_speed_dial(),
        
        # Right side buttons (Home & Search)
        right_side_buttons(),
        
        # Subtle user menu with dropdown in top-right corner
        rx.box(
            # User avatar circle (clickable)
            rx.box(
                rx.text(
                    "KH",  # Placeholder - will be dynamic with user's initials
                    color="white",
                    font_weight="bold",
                    font_size="sm",
                ),
                id="user-avatar",
                width="2.5rem",
                height="2.5rem",
                border_radius="50%",
                bg="rgba(255, 255, 255, 0.1)",
                border="2px solid rgba(255, 255, 255, 0.2)",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                _hover={"transform": "scale(1.05)", "bg": "rgba(255, 255, 255, 0.15)"},
                transition="all 0.2s ease",
                on_click=rx.call_script("toggleUserDropdown()")
            ),
            # Dropdown menu (initially hidden)
            rx.box(
                clerk.sign_out_button(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="log-out", size=14),
                            rx.text("Sign Out", font_size="sm", font_weight="500"),
                            spacing="2",
                            align="center",
                            justify="center",
                        ),
                        variant="surface",
                        color_scheme="crimson",
                        border_radius="md",
                        padding="0.75rem 1rem",
                        width="100%",
                        min_height="2.5rem",
                        _hover={
                            "transform": "translateY(-1px)",
                        },
                        transition="all 0.2s ease",
                    )
                ),
                id="user-dropdown",
                position="absolute",
                top="3rem",
                right="0",
                bg="rgba(0, 0, 0, 0.8)",
                border="1px solid rgba(255, 255, 255, 0.2)",
                border_radius="md",
                padding="0.5rem",
                backdrop_filter="blur(10px)",
                box_shadow="0 4px 12px rgba(0, 0, 0, 0.3)",
                width="140px",
                display="none",  # Initially hidden
                z_index="1001",
            ),
            # JavaScript for dropdown functionality and user initials
            rx.script("""
                function toggleUserDropdown() {
                    const dropdown = document.getElementById('user-dropdown');
                    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
                        dropdown.style.display = 'block';
                    } else {
                        dropdown.style.display = 'none';
                    }
                }
                
                // Close dropdown when clicking outside
                document.addEventListener('click', function(event) {
                    const avatar = document.getElementById('user-avatar');
                    const dropdown = document.getElementById('user-dropdown');
                    
                    if (!avatar.contains(event.target) && !dropdown.contains(event.target)) {
                        dropdown.style.display = 'none';
                    }
                });
                
                // Update user initials when Clerk loads
                function updateUserInitials() {
                    if (window.Clerk && window.Clerk.user) {
                        const user = window.Clerk.user;
                        const firstName = user.firstName || '';
                        const lastName = user.lastName || '';
                        
                        let initials = '';
                        if (firstName) initials += firstName.charAt(0).toUpperCase();
                        if (lastName) initials += lastName.charAt(0).toUpperCase();
                        
                        // Fallback to email if no name
                        if (!initials && user.primaryEmailAddress) {
                            initials = user.primaryEmailAddress.emailAddress.charAt(0).toUpperCase();
                        }
                        
                        // Default fallback
                        if (!initials) initials = 'U';
                        
                        const avatarText = document.querySelector('#user-avatar .chakra-text');
                        if (avatarText) {
                            avatarText.textContent = initials;
                        }
                    }
                }
                
                // Try to update initials when Clerk loads
                if (window.Clerk) {
                    updateUserInitials();
                } else {
                    window.addEventListener('clerk:loaded', updateUserInitials);
                }
                
                // Also listen for user updates
                window.addEventListener('clerk:user', updateUserInitials);
            """),
            position="fixed",
            top="2rem",
            right="2rem",
            z_index="1000",
            transition="all 0.3s ease",
        ),
        
        # Container for page content
        position="relative",
        width="100%",
        min_height="100vh",
        overflow="hidden",
    )


def page_wrapper(*children) -> rx.Component:
    """Wrapper component for pages that includes universal background."""
    return rx.box(
        # Global CSS for Clerk components on all pages
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
        universal_background(),
        rx.box(
            *children,
            position="relative",
            z_index="10",
            width="100%",
            min_height="100vh",
            # Remove default padding that pushes content down
            padding="0",
            margin="0",
            style={
                "padding": "0",
                "margin": "0"
            }
        ),
        position="relative",
        width="100%",
        min_height="100vh",
        overflow="hidden",
    )