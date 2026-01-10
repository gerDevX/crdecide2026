"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

export const BentoGrid = ({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) => {
  return (
    <div
      className={cn(
        "mx-auto grid max-w-7xl grid-cols-1 gap-4 md:auto-rows-[18rem] md:grid-cols-3",
        className
      )}
    >
      {children}
    </div>
  );
};

export const BentoGridItem = ({
  className,
  title,
  description,
  header,
  icon,
  onClick,
  href,
}: {
  className?: string;
  title?: string | React.ReactNode;
  description?: string | React.ReactNode;
  header?: React.ReactNode;
  icon?: React.ReactNode;
  onClick?: () => void;
  href?: string;
}) => {
  const Wrapper = href ? "a" : "div";
  
  return (
    <Wrapper
      href={href}
      onClick={onClick}
      className={cn(
        "group/bento row-span-1 flex flex-col justify-between space-y-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-lg transition-all duration-300",
        "hover:shadow-2xl hover:border-cyan-200 hover:scale-[1.02]",
        "dark:border-slate-800 dark:bg-slate-900",
        onClick || href ? "cursor-pointer" : "",
        className
      )}
    >
      {header && (
        <div className="flex-1 w-full rounded-xl overflow-hidden">
          {header}
        </div>
      )}
      <div className="transition duration-200 group-hover/bento:translate-x-2">
        {icon && (
          <div className="mb-2 flex items-center gap-2">
            {icon}
          </div>
        )}
        {title && (
          <div className="mb-2 font-bold text-slate-900 dark:text-white">
            {title}
          </div>
        )}
        {description && (
          <div className="text-sm text-slate-600 dark:text-slate-400">
            {description}
          </div>
        )}
      </div>
    </Wrapper>
  );
};

export default BentoGrid;
