"use client";
import { motion } from "framer-motion";
import { cn } from "../../../lib/utils";

interface RankingEntry {
  id: string;
  name: string;
  party: string;
  score: number;
  rank: number;
  riskLevel: "BAJO" | "MEDIO" | "ALTO";
  penalty: number;
}

interface RankingTableProps {
  entries: RankingEntry[];
  limit?: number;
  className?: string;
  showViewAll?: boolean;
}

export const RankingTable = ({
  entries,
  limit,
  className,
  showViewAll = true,
}: RankingTableProps) => {
  const displayEntries = limit ? entries.slice(0, limit) : entries;

  const getRiskColor = (level: string) => {
    switch (level) {
      case "BAJO":
        return "text-emerald-600";
      case "MEDIO":
        return "text-amber-600";
      case "ALTO":
        return "text-red-600";
      default:
        return "text-slate-600";
    }
  };

  const getRankStyle = (rank: number) => {
    if (rank === 1) return "bg-gradient-to-br from-amber-400 to-amber-600 text-white shadow-lg shadow-amber-200";
    if (rank === 2) return "bg-gradient-to-br from-slate-300 to-slate-400 text-white";
    if (rank === 3) return "bg-gradient-to-br from-orange-400 to-orange-500 text-white";
    return "bg-slate-100 text-slate-600";
  };

  return (
    <div className={cn("rounded-2xl border border-slate-200 bg-white shadow-xl overflow-hidden", className)}>
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
        <h2 className="text-xl font-bold text-slate-900">Ranking General</h2>
        {showViewAll && (
          <a 
            href="/ranking" 
            className="text-cyan-600 hover:text-cyan-700 text-sm font-semibold flex items-center gap-1 group"
          >
            Ver completo
            <motion.span
              className="inline-block"
              initial={{ x: 0 }}
              whileHover={{ x: 4 }}
            >
              →
            </motion.span>
          </a>
        )}
      </div>
      
      {/* Risk Level Legend */}
      <div className="px-6 py-3 bg-slate-50 border-b border-slate-100">
        <div className="flex flex-wrap items-center gap-4 text-xs">
          <span className="text-slate-500 font-medium">Riesgo y Responsabilidad:</span>
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-semibold">
              🟢 BAJO
            </span>
            <span className="text-slate-400">No compromete finanzas</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 font-semibold">
              🟠 MEDIO
            </span>
            <span className="text-slate-400">1-2 alertas</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-semibold">
              🔴 ALTO
            </span>
            <span className="text-slate-400">Múltiples alertas</span>
          </div>
        </div>
      </div>
      
      <div className="divide-y divide-slate-100">
        {displayEntries.map((entry, idx) => (
          <motion.a
            key={entry.id}
            href={`/candidatos/${entry.id}`}
            className="flex items-center gap-4 px-6 py-4 hover:bg-gradient-to-r hover:from-cyan-50 hover:to-transparent transition-all group"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.05 }}
          >
            {/* Rank */}
            <motion.span 
              className={cn(
                "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shrink-0",
                getRankStyle(entry.rank)
              )}
              whileHover={{ scale: 1.1 }}
            >
              {entry.rank}
            </motion.span>
            
            {/* Info */}
            <div className="flex-1 min-w-0">
              <div className="font-semibold text-slate-900 group-hover:text-cyan-600 transition-colors truncate">
                {entry.name}
              </div>
              <div className="text-sm text-slate-500 truncate">{entry.party}</div>
            </div>
            
            {/* Risk Badge */}
            <span className={cn(
              "hidden md:inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold",
              entry.riskLevel === "BAJO" ? "bg-emerald-100 text-emerald-700" :
              entry.riskLevel === "MEDIO" ? "bg-amber-100 text-amber-700" :
              "bg-red-100 text-red-700"
            )}>
              {entry.riskLevel === "BAJO" ? "🟢" : entry.riskLevel === "MEDIO" ? "🟠" : "🔴"} {entry.riskLevel}
            </span>
            
            {/* Penalty */}
            {entry.penalty < 0 && (
              <span className="hidden lg:inline-flex items-center px-2 py-0.5 bg-red-50 text-red-600 rounded text-xs font-medium">
                {entry.penalty}
              </span>
            )}
            
            {/* Score Bar */}
            <div className="w-24 hidden sm:block">
              <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                <motion.div
                  className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-600"
                  initial={{ width: 0 }}
                  animate={{ width: `${(entry.score / 100) * 100}%` }}
                  transition={{ duration: 0.8, delay: idx * 0.1 }}
                />
              </div>
            </div>
            
            {/* Score */}
            <span className={cn(
              "font-bold text-lg min-w-[4rem] text-right",
              getRiskColor(entry.riskLevel)
            )}>
              {entry.score}%
            </span>
          </motion.a>
        ))}
      </div>
    </div>
  );
};

export default RankingTable;
