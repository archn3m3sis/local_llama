import React, { useCallback, useMemo } from 'react';
import Particles from '@tsparticles/react';
import { loadBasic } from '@tsparticles/basic';
import { loadExternalAttractInteraction } from '@tsparticles/interaction-external-attract';
import { loadExternalRepulseInteraction } from '@tsparticles/interaction-external-repulse';
import type { Engine, ISourceOptions } from '@tsparticles/engine';

interface AdvancedSmokeSystemProps {
  className?: string;
}

const AdvancedSmokeSystem: React.FC<AdvancedSmokeSystemProps> = ({ className = '' }) => {
  const particlesInit = useCallback(async (engine: Engine) => {
    // Load the basic tsparticles package
    await loadBasic(engine);
    // Load external interactions for mouse control
    await loadExternalAttractInteraction(engine);
    await loadExternalRepulseInteraction(engine);
  }, []);

  const options: ISourceOptions = useMemo(() => ({
    background: {
      color: {
        value: 'transparent',
      },
    },
    fpsLimit: 60,
    interactivity: {
      events: {
        onClick: {
          enable: false,
        },
        onHover: {
          enable: true,
          mode: ['attract', 'repulse'],
        },
        resize: true,
      },
      modes: {
        attract: {
          distance: 150,
          duration: 0.4,
          factor: 3,
          maxSpeed: 50,
          speed: 1,
        },
        repulse: {
          distance: 100,
          duration: 0.4,
          factor: 100,
          speed: 1,
        },
      },
    },
    particles: {
      color: {
        value: ['#ffffff', '#f8f9fa', '#e9ecef'],
      },
      links: {
        enable: false,
      },
      move: {
        direction: 'right',
        enable: true,
        outModes: {
          default: 'out',
        },
        random: true,
        speed: {
          min: 0.3,
          max: 1.2,
        },
        straight: false,
        trail: {
          enable: true,
          length: 10,
          fill: {
            color: {
              value: '#000000',
            },
          },
        },
        vibrate: true,
        warp: true,
      },
      number: {
        density: {
          enable: true,
          area: 1000,
        },
        value: 800, // High particle count for dense smoke effect
      },
      opacity: {
        value: {
          min: 0.05,
          max: 0.4,
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
          min: 1,
          max: 8,
        },
        animation: {
          enable: true,
          speed: 2,
          sync: false,
        },
      },
      twinkle: {
        particles: {
          enable: true,
          frequency: 0.05,
          opacity: 0.8,
        },
      },
      wobble: {
        distance: 10,
        enable: true,
        speed: {
          min: -3,
          max: 3,
        },
      },
      life: {
        count: 1,
        delay: {
          value: 0,
        },
        duration: {
          value: {
            min: 3,
            max: 8,
          },
        },
      },
      rotate: {
        animation: {
          enable: true,
          speed: 5,
          sync: false,
        },
        direction: 'random',
        value: {
          min: 0,
          max: 360,
        },
      },
    },
    detectRetina: true,
    smooth: true,
    style: {
      position: 'absolute',
      top: '0',
      left: '0',
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      zIndex: '5',
    },
    themes: [
      {
        name: 'light',
        default: {
          value: false,
        },
        options: {
          particles: {
            color: {
              value: ['#ffffff', '#f8f9fa', '#e9ecef'],
            },
          },
        },
      },
      {
        name: 'dark',
        default: {
          value: true,
        },
        options: {
          particles: {
            color: {
              value: ['#ffffff', '#f8f9fa', '#e9ecef'],
            },
          },
        },
      },
    ],
    // Advanced smoke-like movement with turbulence
    motion: {
      disable: false,
      reduce: {
        factor: 4,
        value: true,
      },
    },
    // Emitter configuration for continuous smoke generation
    emitters: [
      {
        autoPlay: true,
        fill: true,
        life: {
          wait: false,
        },
        rate: {
          delay: 0.1,
          quantity: 5,
        },
        shape: {
          type: 'square',
        },
        startCount: 0,
        size: {
          mode: 'percent',
          height: 100,
          width: 10,
        },
        direction: 'right',
        particles: {
          move: {
            direction: 'right',
            outModes: {
              default: 'destroy',
              left: 'none',
            },
            speed: {
              min: 0.5,
              max: 1.5,
            },
            angle: {
              offset: 0,
              value: 15,
            },
          },
          opacity: {
            value: {
              min: 0.1,
              max: 0.6,
            },
          },
          size: {
            value: {
              min: 2,
              max: 12,
            },
          },
        },
        position: {
          x: -10,
          y: 50,
        },
      },
      {
        autoPlay: true,
        fill: true,
        life: {
          wait: false,
        },
        rate: {
          delay: 0.15,
          quantity: 3,
        },
        shape: {
          type: 'square',
        },
        startCount: 0,
        size: {
          mode: 'percent',
          height: 80,
          width: 8,
        },
        direction: 'right',
        particles: {
          move: {
            direction: 'right',
            outModes: {
              default: 'destroy',
              left: 'none',
            },
            speed: {
              min: 0.3,
              max: 1.0,
            },
            angle: {
              offset: 0,
              value: 20,
            },
          },
          opacity: {
            value: {
              min: 0.05,
              max: 0.3,
            },
          },
          size: {
            value: {
              min: 3,
              max: 15,
            },
          },
        },
        position: {
          x: -15,
          y: 30,
        },
      },
    ],
  }), []);

  return (
    <div className={`fixed inset-0 w-full h-full overflow-hidden ${className}`}>
      <Particles
        id="tsparticles-smoke"
        init={particlesInit}
        options={options}
        className="absolute inset-0 w-full h-full"
      />
      
      {/* Visibility indicator */}
      <div 
        className="absolute top-5 left-5 z-10 bg-black bg-opacity-60 text-white text-sm font-mono px-3 py-2 rounded border border-white border-opacity-30"
        style={{
          backdropFilter: 'blur(10px)',
        }}
      >
        🌫️ TSParticles Smoke System Active - Move mouse to interact
      </div>
    </div>
  );
};

export default AdvancedSmokeSystem;