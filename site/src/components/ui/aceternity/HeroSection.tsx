"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";
import { BackgroundBeams } from "./BackgroundBeams";
import { GlowingStarsBackground } from "./GlowingStars";
import { MovingBorder } from "./MovingBorder";

interface HeroSectionProps {
  title: string;
  highlight: string;
  subtitle: string;
  candidateCount: number;
  primaryAction: { label: string; href: string };
  secondaryAction: { label: string; href: string };
  className?: string;
}

export const HeroSection = ({
  title,
  highlight,
  subtitle,
  candidateCount,
  primaryAction,
  secondaryAction,
  className,
}: HeroSectionProps) => {
  return (
    <section className={cn("relative py-20 md:py-32 overflow-hidden", className)}>
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-50 via-white to-cyan-50/30" />
      <GlowingStarsBackground className="opacity-40" starCount={30} />
      <BackgroundBeams className="opacity-50" />
      
      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          {/* Badge */}
          <motion.div
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-cyan-100 to-blue-100 border border-cyan-200 mb-8"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-500 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-600" />
            </span>
            <span className="text-sm font-medium text-cyan-700">
              Elecciones Presidenciales 2026
            </span>
          </motion.div>

          {/* Title */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-slate-900 mb-6 tracking-tight">
            {title}{" "}
            <span className="relative inline-block">
              <span className="bg-gradient-to-r from-cyan-600 via-blue-600 to-cyan-600 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient">
                {highlight}
              </span>
              <motion.span
                className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 0.5, duration: 0.8 }}
              />
            </span>
          </h1>

          {/* Subtitle */}
          <motion.p
            className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto mb-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            {subtitle.replace("{count}", String(candidateCount))}
            <br />
            <strong className="text-slate-800">Ahora con análisis de responsabilidad fiscal.</strong>
          </motion.p>

          {/* CTAs */}
          <motion.div
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <MovingBorder
              as="a"
              href={primaryAction.href}
              className="text-base px-8 py-4"
              duration={4000}
            >
              {primaryAction.label}
            </MovingBorder>
            
            <a
              href={secondaryAction.href}
              className="group inline-flex items-center gap-2 px-8 py-4 rounded-xl text-slate-700 font-semibold hover:text-cyan-600 transition-colors"
            >
              {secondaryAction.label}
              <motion.span
                className="inline-block"
                whileHover={{ x: 4 }}
              >
                →
              </motion.span>
            </a>
          </motion.div>
        </motion.div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-cyan-300 to-transparent" />
    </section>
  );
};

export default HeroSection;
