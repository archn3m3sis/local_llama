import reflex as rx

def advanced_smoke_system() -> rx.Component:
    """Advanced smoke particle system component using tsparticles."""
    return rx.fragment(
        rx.el.div(
            id="tsparticles-smoke",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0", 
                "width": "100%",
                "height": "100%",
                "pointer_events": "none",
                "z_index": "100",
            }
        ),
        rx.script("""
            // Robust particle system with DOM observer
            (async () => {
                // Skip if already initializing
                if (window.particlesInitializing) return;
                window.particlesInitializing = true;
                
                try {
                    // Load tsParticles modules if not already loaded
                    if (!window.tsParticlesEngine) {
                        const { tsParticles } = await import("https://cdn.jsdelivr.net/npm/@tsparticles/engine@3.0.3/+esm");
                        const { loadBasic } = await import("https://cdn.jsdelivr.net/npm/@tsparticles/basic@3.0.3/+esm");
                        const { loadExternalAttractInteraction } = await import("https://cdn.jsdelivr.net/npm/@tsparticles/interaction-external-attract@3.0.3/+esm");
                        const { loadExternalRepulseInteraction } = await import("https://cdn.jsdelivr.net/npm/@tsparticles/interaction-external-repulse@3.0.3/+esm");
                        
                        await loadBasic(tsParticles);
                        await loadExternalAttractInteraction(tsParticles);
                        await loadExternalRepulseInteraction(tsParticles);
                        
                        window.tsParticlesEngine = tsParticles;
                    }
                
                const options = {
                    background: {
                        color: {
                            value: 'transparent',
                        },
                    },
                    fpsLimit: 45, // Balanced performance vs smoothness
                    interactivity: {
                        events: {
                            onClick: {
                                enable: true,
                                mode: 'repulse',
                            },
                            onHover: {
                                enable: true,
                                mode: 'attract',
                                parallax: {
                                    enable: false, // Disable parallax for performance
                                    force: 2,
                                    smooth: 10
                                }
                            },
                            resize: true,
                        },
                        modes: {
                            attract: {
                                distance: 100, // Reduced from 150
                                duration: 0.3, // Reduced from 0.4
                                factor: 3, // Reduced from 5
                                maxSpeed: 25, // Reduced from 50
                                speed: 0.8, // Reduced from 1
                            },
                            repulse: {
                                distance: 120, // Reduced from 200
                                duration: 0.3, // Reduced from 0.4
                                factor: 50, // Reduced from 100
                                speed: 0.8, // Reduced from 1
                            },
                        },
                    },
                    particles: {
                        color: {
                            value: ['#ffffff', '#f8f9fa', '#e9ecef', '#cbd5e1', '#94a3b8'],
                        },
                        links: {
                            enable: false,
                        },
                        move: {
                            direction: 'none',
                            enable: true,
                            outModes: {
                                default: 'bounce',
                            },
                            random: true,
                            speed: 0.5,
                            straight: false,
                        },
                        number: {
                            density: {
                                enable: true,
                                area: 400, // Balanced density
                            },
                            value: 250, // Increased from 150 but less than original 600
                        },
                        opacity: {
                            value: {
                                min: 0.1,
                                max: 0.4, // Slightly increased for better visibility
                            },
                            animation: {
                                enable: true,
                                speed: 0.8, // Balanced animation speed
                                sync: false,
                            },
                        },
                        shape: {
                            type: 'circle',
                        },
                        size: {
                            value: {
                                min: 0.5,
                                max: 1.8, // Restored closer to original size
                            },
                            animation: {
                                enable: true,
                                speed: 1.5, // Balanced size animation
                                sync: false,
                            },
                        },
                    },
                    detectRetina: true,
                    smooth: true,
                };
                
                // Create a robust particle initialization function
                window.initializeParticles = async () => {
                    const tsParticles = window.tsParticlesEngine;
                    if (!tsParticles) return;
                    
                    try {
                        // Clear any existing particles
                        const existingContainer = tsParticles.domItem(0);
                        if (existingContainer) {
                            await existingContainer.destroy();
                        }
                        
                        // Wait for DOM to be ready
                        await new Promise(resolve => setTimeout(resolve, 50));
                        
                        // Check if the container exists
                        const container = document.getElementById('tsparticles-smoke');
                        if (container) {
                            await tsParticles.load({
                                id: "tsparticles-smoke",
                                options: options
                            });
                        }
                    } catch (error) {
                        console.log('Particle initialization error:', error);
                    }
                };
                
                // Optimized DOM observer with throttling
                let observerTimeout;
                const observer = new MutationObserver((mutations) => {
                    if (observerTimeout) return; // Throttle observer calls
                    observerTimeout = setTimeout(() => {
                        observerTimeout = null;
                        mutations.forEach((mutation) => {
                            mutation.addedNodes.forEach((node) => {
                                if (node.nodeType === 1 && (node.id === 'tsparticles-smoke' || node.querySelector('#tsparticles-smoke'))) {
                                    setTimeout(() => window.initializeParticles(), 100);
                                }
                            });
                        });
                    }, 50); // Throttle to 50ms
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: false // Reduced subtree monitoring for performance
                });
                
                // Initial load
                await window.initializeParticles();
                
                } catch (error) {
                    console.log('Particle system error:', error);
                } finally {
                    window.particlesInitializing = false;
                }
            })();
        """)
    )