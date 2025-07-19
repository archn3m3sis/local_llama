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
                "z_index": "5",
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
                    fpsLimit: 60,
                    interactivity: {
                        events: {
                            onClick: {
                                enable: true,
                                mode: 'repulse',
                            },
                            onHover: {
                                enable: true,
                                mode: 'attract',
                            },
                            resize: true,
                        },
                        modes: {
                            attract: {
                                distance: 150,
                                duration: 0.4,
                                factor: 5,
                                maxSpeed: 50,
                                speed: 1,
                            },
                            repulse: {
                                distance: 200,
                                duration: 0.4,
                                factor: 100,
                                speed: 1,
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
                                area: 300,
                            },
                            value: 600,
                        },
                        opacity: {
                            value: {
                                min: 0.1,
                                max: 0.6,
                            },
                            animation: {
                                enable: true,
                                speed: 1,
                                sync: false,
                            },
                        },
                        shape: {
                            type: 'circle',
                        },
                        size: {
                            value: {
                                min: 0.5,
                                max: 2,
                            },
                            animation: {
                                enable: true,
                                speed: 3,
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
                
                // Set up DOM observer to watch for particle container
                const observer = new MutationObserver((mutations) => {
                    mutations.forEach((mutation) => {
                        mutation.addedNodes.forEach((node) => {
                            if (node.nodeType === 1 && (node.id === 'tsparticles-smoke' || node.querySelector('#tsparticles-smoke'))) {
                                setTimeout(() => window.initializeParticles(), 100);
                            }
                        });
                    });
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
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