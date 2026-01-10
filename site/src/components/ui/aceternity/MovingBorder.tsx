"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

interface MovingBorderProps {
  children: React.ReactNode;
  duration?: number;
  className?: string;
  containerClassName?: string;
  borderClassName?: string;
  as?: React.ElementType;
  href?: string;
}

export const MovingBorder = ({
  children,
  duration = 3000,
  className,
  containerClassName,
  borderClassName,
  as: Component = "button",
  href,
}: MovingBorderProps) => {
  return (
    <Component
      href={href}
      className={cn(
        "relative inline-flex items-center justify-center overflow-hidden rounded-xl p-[2px] group",
        containerClassName
      )}
    >
      <motion.div
        className={cn(
          "absolute inset-[-100%] rounded-xl",
          borderClassName
        )}
        style={{
          background:
            "conic-gradient(from 0deg, transparent, #06b6d4, #0284c7, transparent 30%)",
        }}
        animate={{
          rotate: 360,
        }}
        transition={{
          duration: duration / 1000,
          repeat: Infinity,
          ease: "linear",
        }}
      />
      <div
        className={cn(
          "relative flex h-full w-full items-center justify-center rounded-[10px] bg-white px-6 py-3 font-semibold text-slate-900",
          "transition-colors duration-200 group-hover:bg-slate-50",
          "dark:bg-slate-950 dark:text-white dark:group-hover:bg-slate-900",
          className
        )}
      >
        {children}
      </div>
    </Component>
  );
};

export default MovingBorder;
