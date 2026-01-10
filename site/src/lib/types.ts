// ============================================
// TIPOS BASE
// ============================================

export type AgeGroup = '18-35' | '36-49' | '50+';

export type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9' | 'P10';

export type FiscalRiskLevel = 'ALTO' | 'MEDIO' | 'BAJO';

// ============================================
// ENTIDADES PRINCIPALES
// ============================================

export interface Candidate {
  candidate_id: string;
  candidate_name: string;
  party_name: string;
  pdf_id: string;
  pdf_title: string;
  pdf_url: string;
}

export interface Pillar {
  pillar_id: PillarId;
  pillar_name: string;
  weight: number;
}

export interface Dimensions {
  existence: 0 | 1;
  when: 0 | 1;
  how: 0 | 1;
  funding: 0 | 1;
}

export interface ExtractedFields {
  when_text: string;
  how_text: string;
  funding_text: string;
}

export interface Evidence {
  pdf_id: string;
  page: number;
  snippet: string;
}

export interface Proposal {
  proposal_id: string;
  candidate_id: string;
  pillar_id: PillarId;
  proposal_title: string;
  proposal_text: string;
  dimensions: Dimensions;
  extracted_fields: ExtractedFields;
  evidence: Evidence;
}

// ============================================
// PENALIZACIONES FISCALES
// ============================================

export interface FiscalPenalty {
  type: 'attacks_fiscal_rule' | 'proposes_debt_increase' | 'proposes_tax_increase' | 'urgency_omission';
  value: number;
  reason: string;
  evidence?: string;
}

export interface FiscalFlags {
  attacks_fiscal_rule: boolean;
  proposes_debt_increase: boolean;
  proposes_tax_increase: boolean;
  shows_fiscal_responsibility: boolean;
}

export interface FiscalAnalysis {
  flags: FiscalFlags;
  total_penalty: number;
  evidence: string[];
}

// ============================================
// SCORES
// ============================================

export interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;
  effective_score: number;
  normalized: number;
  weighted: number;
  penalties: FiscalPenalty[];
}

export interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  fiscal_analysis: FiscalAnalysis;
  overall: {
    raw_sum: number;
    effective_sum: number;
    weighted_sum: number;
    priority_weighted_sum: number;
    critical_weighted_sum: number;
    fiscal_penalty_applied: number;
    notes: string;
  };
}

export interface RankingEntry {
  rank: number;
  candidate_id: string;
  weighted_sum?: number;
  fiscal_penalty?: number;
  priority_weighted_sum?: number;
  critical_weighted_sum?: number;
}

export interface Ranking {
  method_version: string;
  weights: Record<string, number>;
  priority_pillars: string[];
  critical_pillars: string[];
  penalties_applied: {
    attacks_fiscal_rule: number;
    proposes_debt_increase: number;
    proposes_tax_increase: number;
  };
  ranking_overall_weighted: RankingEntry[];
  ranking_priority_weighted: RankingEntry[];
  ranking_critical_weighted: RankingEntry[];
}

// ============================================
// ANÁLISIS DETALLADO
// ============================================

export interface UrgencyCoverage {
  covered: boolean;
  mentions: string[];
}

export interface DetailedAnalysis {
  candidate_id: string;
  pdf_id: string;
  total_pages: number;
  fiscal_responsibility: FiscalFlags;
  fiscal_evidence: string[];
  urgency_coverage: {
    seguridad_operativa: UrgencyCoverage;
    salud_ccss: UrgencyCoverage;
    inversion_extranjera: UrgencyCoverage;
    empleo: UrgencyCoverage;
    educacion: UrgencyCoverage;
    infraestructura_APP: UrgencyCoverage;
    crimen_organizado: UrgencyCoverage;
  };
  strengths: string[];
  weaknesses: string[];
  risk_level: FiscalRiskLevel;
}

// ============================================
// ÍNDICES PARA NAVEGACIÓN RÁPIDA
// ============================================

export interface CandidateIndex {
  [candidate_id: string]: Candidate;
}

export interface PillarIndex {
  [pillar_id: string]: Pillar;
}

export interface ScoresByCandidate {
  [candidate_id: string]: CandidateScore;
}

export interface AnalysisByCandidate {
  [candidate_id: string]: DetailedAnalysis;
}

// ============================================
// TIPOS PARA UI
// ============================================

export interface PillarCardData {
  pillar: Pillar;
  avgScore: number;
  topCandidates: Array<{
    candidate: Candidate;
    score: PillarScore;
  }>;
}

// ============================================
// PILLAR METADATA
// ============================================

export const PILLAR_ICONS: Record<PillarId, string> = {
  P1: '💰',
  P2: '💼',
  P3: '🛡️',
  P4: '🏥',
  P5: '📚',
  P6: '🌿',
  P7: '⚖️',
  P8: '🤝',
  P9: '🌎',
  P10: '🏗️',
};

export const PILLAR_COLORS: Record<PillarId, string> = {
  P1: 'emerald',
  P2: 'blue',
  P3: 'red',
  P4: 'pink',
  P5: 'amber',
  P6: 'green',
  P7: 'purple',
  P8: 'orange',
  P9: 'cyan',
  P10: 'slate',
};

// Pilares prioritarios: 60% del peso (Seguridad, Salud, Finanzas, Reforma Estado)
export const PRIORITY_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7'];

// Pilares críticos: 81% del peso (incluye Empleo y Educación)
export const CRITICAL_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7', 'P2', 'P5'];

// ============================================
// CONSTANTES DE RIESGO FISCAL
// ============================================

export const FISCAL_RISK_COLORS: Record<FiscalRiskLevel, string> = {
  ALTO: 'red',
  MEDIO: 'amber',
  BAJO: 'green',
};

export const FISCAL_RISK_EMOJI: Record<FiscalRiskLevel, string> = {
  ALTO: '🔴',
  MEDIO: '🟠',
  BAJO: '🟢',
};

export const PENALTY_LABELS: Record<string, { emoji: string; label: string; description: string }> = {
  attacks_fiscal_rule: {
    emoji: '⚠️',
    label: 'Ataca regla fiscal',
    description: 'Propone flexibilizar o eliminar la regla fiscal que mantiene las finanzas de CR a flote',
  },
  proposes_debt_increase: {
    emoji: '💰',
    label: 'Más deuda',
    description: 'Propone aumentar la deuda pública sin plan de sostenibilidad',
  },
  proposes_tax_increase: {
    emoji: '📈',
    label: 'Más impuestos',
    description: 'Propone aumentar impuestos al pueblo costarricense',
  },
};
