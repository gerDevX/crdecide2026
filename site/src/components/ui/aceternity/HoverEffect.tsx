"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../../lib/utils";

export const HoverEffect = ({
  items,
  className,
}: {
  items: {
    title: string;
    description: string;
    link: string;
    icon?: React.ReactNode;
    badge?: string;
    badgeColor?: string;
    bgColor?: string;
    iconBg?: string;
  }[];
  className?: string;
}) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  // Default background colors for each card
  const defaultBgColors = [
    "from-emerald-50 to-green-50 border-emerald-200",
    "from-blue-50 to-indigo-50 border-blue-200",
    "from-purple-50 to-violet-50 border-purple-200",
    "from-amber-50 to-orange-50 border-amber-200",
    "from-rose-50 to-red-50 border-rose-200",
  ];

  const defaultIconBgs = [
    "from-emerald-500 to-green-600",
    "from-blue-500 to-indigo-600",
    "from-purple-500 to-violet-600",
    "from-amber-500 to-orange-600",
    "from-rose-500 to-red-600",
  ];

  return (
    <div
      className={cn(
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4",
        className
      )}
    >
      {items.map((item, idx) => {
        const bgColor = item.bgColor || defaultBgColors[idx % defaultBgColors.length];
        const iconBg = item.iconBg || defaultIconBgs[idx % defaultIconBgs.length];
        
        return (
          <a
            href={item.link}
            key={item.link}
            className="relative group block h-full w-full"
            onMouseEnter={() => setHoveredIndex(idx)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <motion.div
              className={cn(
                "relative h-full w-full overflow-hidden rounded-2xl border-2 p-5",
                "bg-gradient-to-br",
                bgColor,
                "transition-all duration-300",
                hoveredIndex === idx && "shadow-xl scale-[1.02]"
              )}
              whileHover={{ y: -4 }}
              transition={{ duration: 0.2 }}
            >
              {/* Icon */}
              <div 
                className={cn(
                  "w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center text-white text-xl shadow-lg mb-4",
                  iconBg
                )}
              >
                {item.icon}
              </div>
              
              {/* Badge */}
              {item.badge && (
                <span 
                  className={cn(
                    "absolute top-4 right-4 px-2 py-0.5 text-xs font-semibold rounded-full",
                    item.badgeColor || "bg-white/80 text-slate-600"
                  )}
                >
                  {item.badge}
                </span>
              )}
              
              {/* Title */}
              <h4 className="font-bold text-slate-900 text-base mb-2">
                {item.title}
              </h4>
              
              {/* Description */}
              <p className="text-slate-600 text-sm leading-relaxed">
                {item.description}
              </p>
              
              {/* Hover shine effect */}
              <div 
                className={cn(
                  "absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent",
                  "translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"
                )}
              />
            </motion.div>
          </a>
        );
      })}
    </div>
  );
};

export default HoverEffect;
