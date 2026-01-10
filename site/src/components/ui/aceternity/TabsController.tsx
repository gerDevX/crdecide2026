"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

interface Tab {
  id: string;
  label: string;
  icon: string;
}

interface TabsControllerProps {
  tabs: Tab[];
  defaultTab?: string;
  className?: string;
  containerId?: string;
}

export const TabsController = ({
  tabs,
  defaultTab,
  className,
  containerId = "tabs-content",
}: TabsControllerProps) => {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id || "");

  useEffect(() => {
    // Update the data attribute on the container element
    const container = document.getElementById(containerId);
    if (container) {
      container.setAttribute("data-active-tab", activeTab);
    }
  }, [activeTab, containerId]);

  return (
    <div className={cn("flex flex-wrap justify-center gap-2 p-2 bg-slate-100 rounded-2xl", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={cn(
            "relative px-5 py-3 rounded-xl font-semibold text-sm transition-all duration-300",
            "flex items-center gap-2",
            activeTab === tab.id
              ? "text-white"
              : "text-slate-600 hover:text-slate-900 hover:bg-white/50"
          )}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="activeTabIndicator"
              className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl shadow-lg shadow-cyan-500/25"
              transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            />
          )}
          <span className="relative z-10 text-lg">{tab.icon}</span>
          <span className="relative z-10 hidden sm:inline">{tab.label}</span>
        </button>
      ))}
    </div>
  );
};

export default TabsController;
