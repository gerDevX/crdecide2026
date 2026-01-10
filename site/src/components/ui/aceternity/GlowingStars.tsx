"use client";
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../../lib/utils";

interface Star {
  id: number;
  x: number;
  y: number;
  scale: number;
  duration: number;
}

export const GlowingStarsBackground = ({
  className,
  starCount = 50,
}: {
  className?: string;
  starCount?: number;
}) => {
  const [stars, setStars] = useState<Star[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const generateStars = () => {
      const newStars: Star[] = [];
      for (let i = 0; i < starCount; i++) {
        newStars.push({
          id: i,
          x: Math.random() * 100,
          y: Math.random() * 100,
          scale: Math.random() * 0.5 + 0.5,
          duration: Math.random() * 3 + 2,
        });
      }
      setStars(newStars);
    };
    generateStars();
  }, [starCount]);

  return (
    <div
      ref={containerRef}
      className={cn(
        "absolute inset-0 overflow-hidden pointer-events-none",
        className
      )}
    >
      <AnimatePresence>
        {stars.map((star) => (
          <motion.div
            key={star.id}
            className="absolute h-1 w-1 rounded-full bg-cyan-400"
            style={{
              left: `${star.x}%`,
              top: `${star.y}%`,
              boxShadow: "0 0 6px 1px rgba(6, 182, 212, 0.5)",
            }}
            initial={{ opacity: 0, scale: 0 }}
            animate={{
              opacity: [0, 1, 0],
              scale: [0, star.scale, 0],
            }}
            transition={{
              duration: star.duration,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </AnimatePresence>
    </div>
  );
};

export default GlowingStarsBackground;
