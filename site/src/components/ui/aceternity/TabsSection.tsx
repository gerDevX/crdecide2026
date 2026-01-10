"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../../lib/utils";

interface Tab {
  id: string;
  label: string;
  icon: string;
}

interface TabsSectionProps {
  tabs: Tab[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
  className?: string;
}

export const TabsSection = ({
  tabs,
  activeTab,
  onTabChange,
  className,
}: TabsSectionProps) => {
  return (
    <div className={cn("flex flex-wrap justify-center gap-2", className)}>
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={cn(
            "relative px-4 py-2.5 rounded-xl font-semibold text-sm transition-all duration-300",
            "flex items-center gap-2",
            activeTab === tab.id
              ? "text-white"
              : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
          )}
        >
          {activeTab === tab.id && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl shadow-lg shadow-cyan-500/25"
              transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            />
          )}
          <span className="relative z-10 text-lg">{tab.icon}</span>
          <span className="relative z-10">{tab.label}</span>
        </button>
      ))}
    </div>
  );
};

interface TabsContainerProps {
  children: React.ReactNode[];
  activeIndex: number;
  className?: string;
}

export const TabsContainer = ({
  children,
  activeIndex,
  className,
}: TabsContainerProps) => {
  return (
    <div className={cn("relative", className)}>
      <AnimatePresence mode="wait">
        <motion.div
          key={activeIndex}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          {children[activeIndex]}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

// Combined Tabs component with state management
interface TabsPanelProps {
  tabs: Tab[];
  children: React.ReactNode[];
  defaultTab?: string;
  className?: string;
}

export const TabsPanel = ({
  tabs,
  children,
  defaultTab,
  className,
}: TabsPanelProps) => {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id || "");
  const activeIndex = tabs.findIndex((t) => t.id === activeTab);

  return (
    <div className={cn("space-y-6", className)}>
      <TabsSection
        tabs={tabs}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      <TabsContainer activeIndex={activeIndex >= 0 ? activeIndex : 0}>
        {children}
      </TabsContainer>
    </div>
  );
};

export default TabsPanel;
