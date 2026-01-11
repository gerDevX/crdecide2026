"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";
import { AnimatedCounter } from "./AnimatedCounter";

interface FiscalStats {
  lowRisk: number;
  mediumRisk: number;
  highRisk: number;
  attackFiscalRule: number;
  proposeDebt: number;
  ignoreSecurity: number;
  ignoreCCSS: number;
}

interface FiscalRiskDashboardProps {
  stats: FiscalStats;
  className?: string;
}

export const FiscalRiskDashboard = ({ stats, className }: FiscalRiskDashboardProps) => {
  return (
    <div className={cn("space-y-4", className)}>
      {/* Risk Level Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <RiskCard
          level="bajo"
          count={stats.lowRisk}
          color="emerald"
          icon="🟢"
          description="No comprometen las finanzas públicas"
          delay={0}
        />
        <RiskCard
          level="medio"
          count={stats.mediumRisk}
          color="amber"
          icon="🟠"
          description="1-2 banderas fiscales"
          delay={0.1}
        />
        <RiskCard
          level="alto"
          count={stats.highRisk}
          color="red"
          icon="🔴"
          description="Múltiples banderas fiscales"
          delay={0.2}
        />
      </div>

      {/* Penalty Details */}
      <motion.div
        className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-6 shadow-lg"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <div className="grid md:grid-cols-2 gap-4 sm:gap-6">
          <div>
            <h3 className="font-bold text-red-800 mb-3 sm:mb-4 flex items-center gap-2 text-base sm:text-lg">
              <span className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-red-100 flex items-center justify-center text-sm sm:text-base">🔴</span>
              Penalizaciones por irresponsabilidad
            </h3>
            <div className="space-y-2 sm:space-y-3">
              <PenaltyItem
                icon="⚠️"
                count={stats.attackFiscalRule}
                label="atacan la regla fiscal"
              />
              <PenaltyItem
                icon="💰"
                count={stats.proposeDebt}
                label="proponen más deuda"
              />
            </div>
          </div>
          <div>
            <h3 className="font-bold text-amber-800 mb-3 sm:mb-4 flex items-center gap-2 text-base sm:text-lg">
              <span className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-amber-100 flex items-center justify-center text-sm sm:text-base">🟠</span>
              Omisiones de urgencias
            </h3>
            <div className="space-y-2 sm:space-y-3">
              <PenaltyItem
                icon="🚨"
                count={stats.ignoreSecurity}
                label="ignoran seguridad operativa"
              />
              <PenaltyItem
                icon="🏥"
                count={stats.ignoreCCSS}
                label="ignoran crisis CCSS"
              />
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

const RiskCard = ({
  level,
  count,
  color,
  icon,
  description,
  delay,
}: {
  level: string;
  count: number;
  color: "emerald" | "amber" | "red";
  icon: string;
  description: string;
  delay: number;
}) => {
  const colorClasses = {
    emerald: "border-l-emerald-500 from-emerald-50/50",
    amber: "border-l-amber-500 from-amber-50/50",
    red: "border-l-red-500 from-red-50/50",
  };

  const textColors = {
    emerald: "text-emerald-600",
    amber: "text-amber-600",
    red: "text-red-600",
  };

  return (
    <motion.div
      className={cn(
        "relative overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br to-white p-4 sm:p-5 shadow-lg border-l-4",
        colorClasses[color]
      )}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ scale: 1.02 }}
    >
      <div className="flex items-center justify-between">
        <div>
          <AnimatedCounter
            value={count}
            className={cn("text-3xl sm:text-4xl font-bold", textColors[color])}
          />
          <p className="text-slate-600 text-base sm:text-sm mt-1 capitalize">Riesgo {level} {icon}</p>
        </div>
        <span className="text-4xl sm:text-5xl opacity-30">{icon}</span>
      </div>
      <p className="text-sm sm:text-xs text-slate-500 mt-3">{description}</p>
    </motion.div>
  );
};

const PenaltyItem = ({
  icon,
  count,
  label,
}: {
  icon: string;
  count: number;
  label: string;
}) => {
  return (
    <motion.div
      className="flex items-center gap-2 sm:gap-3 p-2 rounded-lg hover:bg-slate-50 transition-colors"
      whileHover={{ x: 4 }}
    >
      <span className="text-lg sm:text-xl">{icon}</span>
      <span className="text-base sm:text-sm">
        <strong className="text-slate-900">{count}</strong>{" "}
        <span className="text-slate-600">{label}</span>
      </span>
    </motion.div>
  );
};

export default FiscalRiskDashboard;
