"use client";

import { useEffect, useRef } from "react";

export default function Football3D() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationId: number;
    let time = 0;

    const resize = () => {
      canvas.width = canvas.offsetWidth * 2;
      canvas.height = canvas.offsetHeight * 2;
      ctx.scale(2, 2);
    };
    resize();

    const W = () => canvas.offsetWidth;
    const H = () => canvas.offsetHeight;

    // Particles for stadium atmosphere
    interface Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      color: string;
      alpha: number;
      life: number;
      maxLife: number;
    }

    const particles: Particle[] = [];
    const colors = ["#F97316", "#3B82F6", "#22C55E", "#F7D618", "#CE1021", "#00B4D8"];

    function spawnParticle() {
      const cx = W() / 2;
      const cy = H() / 2;
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.3 + Math.random() * 1.2;
      particles.push({
        x: cx + (Math.random() - 0.5) * 60,
        y: cy + (Math.random() - 0.5) * 60,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: 1.5 + Math.random() * 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 0.6 + Math.random() * 0.4,
        life: 0,
        maxLife: 80 + Math.random() * 120,
      });
    }

    function drawFootball(cx: number, cy: number, r: number, rotation: number) {
      if (!ctx) return;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotation);

      // Ball body - gradient for 3D look
      const grad = ctx.createRadialGradient(-r * 0.25, -r * 0.25, r * 0.1, 0, 0, r);
      grad.addColorStop(0, "#ffffff");
      grad.addColorStop(0.5, "#e0e0e0");
      grad.addColorStop(1, "#888888");

      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Pentagon patches
      const pentagonCount = 5;
      for (let i = 0; i < pentagonCount; i++) {
        const angle = (i * Math.PI * 2) / pentagonCount;
        const px = Math.cos(angle) * r * 0.55;
        const py = Math.sin(angle) * r * 0.55;
        const pSize = r * 0.22;

        ctx.beginPath();
        for (let j = 0; j < 5; j++) {
          const a = (j * Math.PI * 2) / 5 - Math.PI / 2 + angle * 0.3;
          const x = px + Math.cos(a) * pSize;
          const y = py + Math.sin(a) * pSize;
          if (j === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fillStyle = "rgba(20, 20, 20, 0.75)";
        ctx.fill();
      }

      // Center pentagon
      ctx.beginPath();
      for (let j = 0; j < 5; j++) {
        const a = (j * Math.PI * 2) / 5 - Math.PI / 2;
        const x = Math.cos(a) * r * 0.25;
        const y = Math.sin(a) * r * 0.25;
        if (j === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.fillStyle = "rgba(20, 20, 20, 0.8)";
      ctx.fill();

      // Shine highlight
      const shine = ctx.createRadialGradient(-r * 0.3, -r * 0.3, 0, -r * 0.3, -r * 0.3, r * 0.5);
      shine.addColorStop(0, "rgba(255,255,255,0.5)");
      shine.addColorStop(1, "rgba(255,255,255,0)");
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.fillStyle = shine;
      ctx.fill();

      ctx.restore();
    }

    function drawOrbitRing(cx: number, cy: number, rx: number, ry: number, rotation: number, color: string) {
      if (!ctx) return;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotation);
      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 8]);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();
    }

    function draw() {
      if (!ctx) return;
      ctx.clearRect(0, 0, W(), H());
      time += 0.012;

      const cx = W() / 2;
      const cy = H() / 2;

      // Spawn particles
      if (Math.random() < 0.3) spawnParticle();

      // Draw orbit rings
      drawOrbitRing(cx, cy, 100, 35, time * 0.5, "rgba(249, 115, 22, 0.15)");
      drawOrbitRing(cx, cy, 120, 40, -time * 0.3 + 1, "rgba(59, 130, 246, 0.12)");
      drawOrbitRing(cx, cy, 80, 28, time * 0.7 + 2, "rgba(0, 180, 216, 0.1)");

      // Update and draw particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life++;

        const lifeRatio = p.life / p.maxLife;
        const alpha = p.alpha * (1 - lifeRatio);

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * (1 - lifeRatio * 0.5), 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = alpha;
        ctx.fill();
        ctx.globalAlpha = 1;

        if (p.life >= p.maxLife) particles.splice(i, 1);
      }

      // Floating ball with gentle bob
      const bobY = Math.sin(time * 1.5) * 8;
      const ballR = 35 + Math.sin(time * 2) * 2;
      drawFootball(cx, cy + bobY, ballR, time * 0.8);

      // Glow behind ball
      const glow = ctx.createRadialGradient(cx, cy + bobY, ballR, cx, cy + bobY, ballR * 3);
      glow.addColorStop(0, "rgba(249, 115, 22, 0.08)");
      glow.addColorStop(0.5, "rgba(59, 130, 246, 0.04)");
      glow.addColorStop(1, "rgba(0, 0, 0, 0)");
      ctx.beginPath();
      ctx.arc(cx, cy + bobY, ballR * 3, 0, Math.PI * 2);
      ctx.fillStyle = glow;
      ctx.fill();

      // Orbiting small dots (like planet moons)
      for (let i = 0; i < 3; i++) {
        const orbitAngle = time * (1.2 + i * 0.4) + (i * Math.PI * 2) / 3;
        const orbitRx = 90 + i * 20;
        const orbitRy = 30 + i * 8;
        const dotX = cx + Math.cos(orbitAngle) * orbitRx;
        const dotY = cy + Math.sin(orbitAngle) * orbitRy + bobY;
        const dotColor = colors[i];

        ctx.beginPath();
        ctx.arc(dotX, dotY, 3 + Math.sin(time + i) * 1, 0, Math.PI * 2);
        ctx.fillStyle = dotColor;
        ctx.globalAlpha = 0.7;
        ctx.fill();

        // Trail
        for (let t = 1; t <= 5; t++) {
          const trailAngle = orbitAngle - t * 0.08;
          const tx = cx + Math.cos(trailAngle) * orbitRx;
          const ty = cy + Math.sin(trailAngle) * orbitRy + bobY;
          ctx.beginPath();
          ctx.arc(tx, ty, 2 - t * 0.3, 0, Math.PI * 2);
          ctx.globalAlpha = 0.3 - t * 0.05;
          ctx.fill();
        }
        ctx.globalAlpha = 1;
      }

      animationId = requestAnimationFrame(draw);
    }

    draw();

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(canvas);

    return () => {
      cancelAnimationFrame(animationId);
      resizeObserver.disconnect();
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
      style={{ display: "block" }}
    />
  );
}
