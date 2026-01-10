"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "../../../lib/utils";

interface CandidateData {
  id: string;
  candidateName: string;
  partyName: string;
  score: number;
  rank: number;
  riskLevel: "BAJO" | "MEDIO" | "ALTO";
  pillars: { id: string; score: number; icon: string }[];
}

interface CandidateSpotlightProps {
  candidates: CandidateData[];
  className?: string;
}

export const CandidateSpotlight = ({
  candidates,
  className,
}: CandidateSpotlightProps) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const getRiskColor = (level: string) => {
    switch (level) {
      case "BAJO":
        return "from-emerald-400 to-green-500";
      case "MEDIO":
        return "from-amber-400 to-orange-500";
      case "ALTO":
        return "from-red-400 to-rose-600";
      default:
        return "from-slate-400 to-slate-500";
    }
  };

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case "BAJO":
        return "bg-emerald-100 text-emerald-700 border-emerald-200";
      case "MEDIO":
        return "bg-amber-100 text-amber-700 border-amber-200";
      case "ALTO":
        return "bg-red-100 text-red-700 border-red-200";
      default:
        return "bg-slate-100 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className={cn("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", className)}>
      {candidates.map((candidate, idx) => (
        <motion.a
          key={candidate.id}
          href={`/candidatos/${candidate.id}`}
          className="relative group block p-1"
          onMouseEnter={() => setHoveredIndex(idx)}
          onMouseLeave={() => setHoveredIndex(null)}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.05 }}
        >
          <AnimatePresence>
            {hoveredIndex === idx && (
              <motion.span
                className={cn(
                  "absolute inset-0 h-full w-full block rounded-2xl bg-gradient-to-br",
                  getRiskColor(candidate.riskLevel)
                )}
                layoutId="candidateHover"
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
              />
            )}
          </AnimatePresence>
          
          <div className={cn(
            "relative z-10 h-full rounded-2xl border border-slate-200 bg-white p-5 overflow-hidden",
            "transition-all duration-300 shadow-lg",
            "group-hover:shadow-2xl group-hover:border-cyan-200 group-hover:scale-[1.02]"
          )}>
            {/* Rank badge */}
            <div className="absolute top-3 right-3">
              <span className={cn(
                "inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold",
                candidate.rank <= 3 
                  ? "bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-lg" 
                  : "bg-slate-100 text-slate-600"
              )}>
                {candidate.rank}
              </span>
            </div>

            {/* Header */}
            <div className="mb-4">
              <h3 className="font-bold text-lg text-slate-900 group-hover:text-cyan-600 transition-colors line-clamp-2 leading-tight mb-1">
                {candidate.candidateName}
              </h3>
              <span className="text-sm text-slate-500 line-clamp-1">
                {candidate.partyName}
              </span>
            </div>

            {/* Score */}
            <div className="flex items-center gap-4 mb-4">
              <div className="flex-1">
                <div className="h-2 rounded-full bg-slate-100 overflow-hidden">
                  <motion.div
                    className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-600"
                    initial={{ width: 0 }}
                    animate={{ width: `${candidate.score}%` }}
                    transition={{ duration: 1, delay: idx * 0.1 }}
                  />
                </div>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
                {candidate.score}%
              </span>
            </div>

            {/* Risk Badge */}
            <div className="flex items-center justify-between">
              <span className={cn(
                "px-3 py-1 text-xs font-semibold rounded-full border",
                getRiskBadgeColor(candidate.riskLevel)
              )}>
                Riesgo {candidate.riskLevel.toLowerCase()}
              </span>
              
              {/* Mini pillars */}
              <div className="flex gap-1">
                {candidate.pillars.slice(0, 5).map((pillar) => (
                  <div
                    key={pillar.id}
                    className={cn(
                      "w-6 h-6 rounded flex items-center justify-center text-xs",
                      pillar.score >= 3 
                        ? "bg-emerald-100 text-emerald-600" 
                        : pillar.score >= 2 
                          ? "bg-amber-100 text-amber-600"
                          : "bg-slate-100 text-slate-400"
                    )}
                    title={`${pillar.id}: ${pillar.score}/4`}
                  >
                    {pillar.icon}
                  </div>
                ))}
              </div>
            </div>

            {/* Hover gradient effect */}
            <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
              <div className="absolute inset-0 bg-gradient-to-t from-cyan-500/5 to-transparent" />
            </div>
          </div>
        </motion.a>
      ))}
    </div>
  );
};

export default CandidateSpotlight;
