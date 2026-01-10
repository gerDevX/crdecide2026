"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";
import { AnimatedCounter } from "./AnimatedCounter";

interface StatItem {
  value: number;
  label: string;
  suffix?: string;
  gradient?: string;
}

interface StatsCardsProps {
  stats: StatItem[];
  className?: string;
}

export const StatsCards = ({ stats, className }: StatsCardsProps) => {
  return (
    <div className={cn("grid grid-cols-2 md:grid-cols-4 gap-4", className)}>
      {stats.map((stat, idx) => (
        <motion.div
          key={stat.label}
          className="group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 shadow-lg hover:shadow-xl transition-all duration-300"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.1 }}
          whileHover={{ scale: 1.02 }}
        >
          {/* Background Gradient on Hover */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          {/* Content */}
          <div className="relative z-10 text-center">
            <AnimatedCounter
              value={stat.value}
              suffix={stat.suffix || ""}
              className={cn(
                "text-4xl md:text-5xl font-bold",
                "bg-gradient-to-r bg-clip-text text-transparent",
                stat.gradient || "from-cyan-600 to-blue-600"
              )}
            />
            <p className="text-sm text-slate-600 mt-2 font-medium">{stat.label}</p>
          </div>

          {/* Decorative Corner */}
          <div className="absolute -top-4 -right-4 w-16 h-16 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
        </motion.div>
      ))}
    </div>
  );
};

export default StatsCards;
