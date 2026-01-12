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
// PENALIZACIONES (SISTEMA NEUTRAL v6)
// ============================================

// Tipos de penalización fiscal (objetivas - basadas en ley)
export type FiscalPenaltyType = 
  | 'attacks_fiscal_rule'      // Ataca la regla fiscal vigente
  | 'proposes_debt_increase';  // Propone más deuda sin plan

// Tipos de penalización por omisión (basadas en urgencias de CR)
export type OmissionPenaltyType = 
  | 'ignores_security'         // No menciona seguridad operativa
  | 'ignores_ccss'             // No menciona crisis de CCSS
  | 'ignores_employment'       // No menciona empleo/desempleo
  | 'ignores_organized_crime'  // No menciona crimen organizado
  | 'missing_priority_pillar'; // Falta propuesta en pilar prioritario

// Todos los tipos de penalización
export type PenaltyType = FiscalPenaltyType | OmissionPenaltyType;

export interface Penalty {
  type: PenaltyType;
  value: number;
  reason: string;
  evidence?: string;
}

// ============================================
// BANDERAS FISCALES (sin proposes_tax_increase - era sesgo ideológico)
// ============================================

export interface FiscalFlags {
  attacks_fiscal_rule: boolean;      // ¿Ataca la regla fiscal?
  proposes_debt_increase: boolean;   // ¿Propone más deuda sin plan?
  shows_fiscal_responsibility: boolean; // ¿Muestra responsabilidad fiscal?
}

export interface FiscalAnalysis {
  flags: FiscalFlags;
  total_penalty: number;
  evidence: string[];
}

// ============================================
// COBERTURA DE URGENCIAS NACIONALES
// ============================================

export interface UrgencyCoverageItem {
  covered: boolean;
  terms_found: string[];
  description: string;
}

export interface UrgencyCoverageMap {
  security_operations: UrgencyCoverageItem;
  ccss_crisis: UrgencyCoverageItem;
  formal_employment: UrgencyCoverageItem;
  organized_crime: UrgencyCoverageItem;
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
  penalties: Penalty[];
  // v7: Sistema de bonos
  bonus_multiple?: number;  // Bono por 3+ propuestas válidas
  bonus_quality?: number;    // Bono por propuesta completa (D1-D4=4/4)
  bonus_funding?: number;    // Bono por propuesta con financiamiento (score >=3)
  // v7: Verificación de viabilidad legal
  viability_penalty?: number;  // Penalización por violaciones constitucionales
  viability_flags?: {
    violates_separation_powers: boolean;
    violates_fundamental_rights: boolean;
    violates_constitutional_guarantees: boolean;
    violates_constitutional_procedures: boolean;
  };
  num_proposals?: number;  // Cantidad de propuestas válidas en este pilar
}

export interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  fiscal_analysis: FiscalAnalysis;
  omission_analysis: OmissionAnalysisV6;
  overall: {
    raw_sum: number;
    effective_sum: number;
    weighted_sum: number;
    priority_weighted_sum: number;
    critical_weighted_sum: number;
    total_penalties_applied: number;
    notes: string;
  };
  informative_flags?: InformativeFlags; // v7: Flags informativos (NO penalizan)
}

// ============================================
// ANÁLISIS DE OMISIONES (v6)
// ============================================

export interface OmissionAnalysisV6 {
  urgency_coverage: UrgencyCoverageMap;
  urgency_penalty: number;
  missing_pillars: PillarId[];
  pillar_penalty: number;
}

// Mantener compatibilidad con código existente
export interface OmissionAnalysis {
  ignores_security: boolean;
  ignores_ccss: boolean;
  ignores_employment: boolean;
  ignores_organized_crime: boolean;
  missing_priority_pillars: PillarId[];
  total_penalty: number;
}

// ============================================
// RANKING
// ============================================

export interface RankingEntry {
  rank: number;
  candidate_id: string;
  weighted_sum?: number;
  total_penalties?: number;
  priority_weighted_sum?: number;
  critical_weighted_sum?: number;
}

export interface Ranking {
  method_version: string;
  description?: string;
  weights: Record<string, number>;
  priority_pillars: string[];
  critical_pillars: string[];
  penalties_applied: {
    fiscal: {
    attacks_fiscal_rule: number;
    proposes_debt_increase: number;
    };
    omissions: {
      ignores_security_operations: number;
      ignores_ccss_crisis: number;
      ignores_formal_employment: number;
      ignores_organized_crime: number;
      missing_priority_pillar: number;
    };
  };
  ranking_overall_weighted: RankingEntry[];
  ranking_priority_weighted: RankingEntry[];
  ranking_critical_weighted: RankingEntry[];
}

// ============================================
// ANÁLISIS DETALLADO
// ============================================

export interface DetailedAnalysis {
  candidate_id: string;
  pdf_id: string;
  total_pages: number;
  version: string;
  fiscal_flags: FiscalFlags;
  fiscal_evidence: string[];
  urgency_coverage: UrgencyCoverageMap;
  missing_priority_pillars: PillarId[];
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
// CONSTANTES DE PENALIZACIÓN (v6 - Neutral + Estricto)
// ============================================

// Penalizaciones por irresponsabilidad (objetivas - basadas en ley vigente)
export const FISCAL_PENALTIES: Record<FiscalPenaltyType, number> = {
  attacks_fiscal_rule: -2,      // Ataca ley vigente = penalización fuerte
  proposes_debt_increase: -1,   // Más deuda en contexto de déficit
};

// Penalizaciones por omisión (basadas en urgencias nacionales de CR)
export const OMISSION_PENALTIES: Record<OmissionPenaltyType, number> = {
  ignores_security: -1,         // No menciona seguridad en contexto de crisis
  ignores_ccss: -1,             // No menciona CCSS en contexto de crisis
  ignores_employment: -0.5,     // No menciona empleo en contexto de desempleo alto
  ignores_organized_crime: -0.5,// No menciona crimen organizado
  missing_priority_pillar: -0.5,// Falta propuesta en pilar prioritario (P1,P3,P4,P7)
};

// ============================================
// CONSTANTES DE RIESGO Y RESPONSABILIDAD
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

export const PENALTY_LABELS: Record<PenaltyType, { emoji: string; label: string; description: string }> = {
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
  ignores_security: {
    emoji: '🚨',
    label: 'Ignora seguridad',
    description: 'No menciona seguridad operativa en medio de crisis de violencia',
  },
  ignores_ccss: {
    emoji: '🏥',
    label: 'Ignora CCSS',
    description: 'No aborda la crisis de la Caja Costarricense de Seguro Social',
  },
  ignores_employment: {
    emoji: '💼',
    label: 'Ignora empleo',
    description: 'No menciona empleo/desempleo con tasa superior al 10%',
  },
  ignores_organized_crime: {
    emoji: '🔫',
    label: 'Ignora crimen organizado',
    description: 'No menciona narcotráfico ni crimen organizado',
  },
  missing_priority_pillar: {
    emoji: '📋',
    label: 'Falta pilar prioritario',
    description: 'No tiene propuesta concreta en un pilar prioritario (P1, P3, P4, P7)',
  },
};

// ============================================
// FLAGS INFORMATIVOS (v7 - NO penalizan, solo informan)
// ============================================

export interface FlagInfo {
  active: boolean;
  severity: 'high' | 'medium' | 'low';
  evidence: Array<{
    pillar_id?: string;
    evidence: string;
    detected_by: string;
  }>;
  description?: string;
  historical_sources?: string[];
}

export interface ContradictionFlag extends FlagInfo {
  evidence: {
    historical: string | null;
    current: string | null;
    pattern: string | null;
  };
  description: string;
}

export interface InformativeFlags {
  current_proposals: {
    violates_separation_powers: FlagInfo;
    violates_fundamental_rights: FlagInfo;
    violates_constitutional_guarantees: FlagInfo;
    violates_constitutional_procedures: FlagInfo;
  };
  dictatorial_patterns?: {
    cuba_similarity?: FlagInfo;
    venezuela_similarity?: FlagInfo;
  };
  power_negotiation_requirements?: {
    requires_assembly_approval?: FlagInfo;
    requires_qualified_majority?: FlagInfo;
    requires_inter_branch_coordination?: FlagInfo;
  };
  historical?: {
    anti_democratic_behavior?: FlagInfo;
    human_rights_violations?: FlagInfo;
    corruption_convictions?: FlagInfo;
  };
  contradictions?: {
    historical_current_contradiction?: ContradictionFlag;
    corruption_transparency_concern?: ContradictionFlag;
  };
}
