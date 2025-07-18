import React, { useEffect, useRef, useState, useCallback } from 'react';

const AdvancedSmokeSystem = ({ className }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef();
  const particlesRef = useRef([]);
  const mouseRef = useRef({ x: 0, y: 0, vx: 0, vy: 0 });
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize particles
  const initParticles = useCallback(() => {
    const particles = [];
    for (let i = 0; i < 30; i++) {
      particles.push({
        id: i,
        x: Math.random() * -400 - 100,
        y: Math.random() * window.innerHeight,
        vx: Math.random() * 1.2 + 0.5,
        vy: (Math.random() - 0.5) * 0.4,
        size: Math.random() * 150 + 80,
        opacity: Math.random() * 0.4 + 0.1,
        life: Math.random() * 100,
        maxLife: Math.random() * 500 + 400,
        baseOpacity: Math.random() * 0.4 + 0.1,
        rotationSpeed: (Math.random() - 0.5) * 0.01,
        rotation: Math.random() * Math.PI * 2,
        mouseInfluence: Math.random() * 0.8 + 0.2,
      });
    }
    particlesRef.current = particles;
  }, []);

  // Mouse tracking
  useEffect(() => {
    const handleMouseMove = (e) => {
      const newX = e.clientX;
      const newY = e.clientY;
      mouseRef.current.vx = newX - mouseRef.current.x;
      mouseRef.current.vy = newY - mouseRef.current.y;
      mouseRef.current.x = newX;
      mouseRef.current.y = newY;
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Canvas setup and animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Initialize particles
    initParticles();
    setIsInitialized(true);

    // Animation loop
    const animate = () => {
      if (!ctx || !canvas) return;

      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update and render particles
      particlesRef.current = particlesRef.current.filter(particle => {
        particle.life += 1;

        // Mouse interaction
        const dx = mouseRef.current.x - particle.x;
        const dy = mouseRef.current.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const maxDistance = 300;

        if (distance < maxDistance) {
          const influence = (maxDistance - distance) / maxDistance;
          const force = influence * particle.mouseInfluence;
          const angle = Math.atan2(dy, dx);
          
          // Repulsion force
          particle.vx += Math.cos(angle + Math.PI) * force * 0.03;
          particle.vy += Math.sin(angle + Math.PI) * force * 0.03;
          
          // Enhanced opacity near mouse
          particle.opacity = Math.min(particle.baseOpacity * (1 + influence * 2), 0.8);
        } else {
          particle.opacity = particle.baseOpacity;
        }

        // Natural movement
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.rotation += particle.rotationSpeed;

        // Apply drag
        particle.vx *= 0.998;
        particle.vy *= 0.998;

        // Turbulence
        particle.vx += Math.sin(particle.life * 0.005 + particle.y * 0.001) * 0.02;
        particle.vy += Math.cos(particle.life * 0.007 + particle.x * 0.001) * 0.015;

        // Fade out over time
        const lifeFactor = Math.max(0, 1 - (particle.life / particle.maxLife));
        particle.opacity *= lifeFactor;

        // Render particle
        ctx.save();
        ctx.translate(particle.x + particle.size / 2, particle.y + particle.size / 2);
        ctx.rotate(particle.rotation);
        ctx.globalAlpha = particle.opacity;
        ctx.filter = `blur(${Math.max(12, particle.size / 8)}px)`;

        // Create radial gradient
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, particle.size / 2);
        gradient.addColorStop(0, `rgba(255, 255, 255, ${particle.opacity * 0.8})`);
        gradient.addColorStop(0.3, `rgba(255, 255, 255, ${particle.opacity * 0.4})`);
        gradient.addColorStop(0.7, `rgba(255, 255, 255, ${particle.opacity * 0.1})`);
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

        ctx.fillStyle = gradient;
        ctx.fillRect(-particle.size / 2, -particle.size / 2, particle.size, particle.size);
        ctx.restore();

        // Keep particle if still alive and on screen
        return particle.x < canvas.width + 200 && particle.life < particle.maxLife && particle.opacity > 0.01;
      });

      // Add new particles
      while (particlesRef.current.length < 30) {
        particlesRef.current.push({
          id: Date.now() + Math.random(),
          x: Math.random() * -400 - 100,
          y: Math.random() * window.innerHeight,
          vx: Math.random() * 1.2 + 0.5,
          vy: (Math.random() - 0.5) * 0.4,
          size: Math.random() * 150 + 80,
          opacity: Math.random() * 0.4 + 0.1,
          life: 0,
          maxLife: Math.random() * 500 + 400,
          baseOpacity: Math.random() * 0.4 + 0.1,
          rotationSpeed: (Math.random() - 0.5) * 0.01,
          rotation: Math.random() * Math.PI * 2,
          mouseInfluence: Math.random() * 0.8 + 0.2,
        });
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [initParticles]);

  return (
    <div 
      className={className} 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 5,
        overflow: 'hidden',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          width: '100%',
          height: '100%',
          mixBlendMode: 'screen',
        }}
      />
      
      {/* Visible indicator that the system is loaded */}
      {isInitialized && (
        <div style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          color: 'rgba(255, 255, 255, 0.5)',
          fontSize: '14px',
          fontFamily: 'monospace',
          zIndex: 10,
          background: 'rgba(0, 0, 0, 0.3)',
          padding: '4px 8px',
          borderRadius: '4px',
        }}>
          🌫️ Interactive Smoke System Active
        </div>
      )}
    </div>
  );
};

export default AdvancedSmokeSystem;