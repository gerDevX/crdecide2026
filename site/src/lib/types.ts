// ============================================
// TIPOS BASE
// ============================================

export type AgeGroup = '18-35' | '36-49' | '50+';

export type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9';

export type ConflictType = 'constitutional' | 'fiscal' | 'none';

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

export interface Compatibility {
  normative_fiscal: 0 | 1;
  conflict_type: ConflictType;
  reference: string;
  note: string;
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
  compatibility: Compatibility;
  evidence: Evidence;
  multi_pillar_source_proposal_id: string | null;
}

export interface Penalty {
  type: 'compatibility';
  value: number;
  reason: string;
}

export interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;
  effective_score: number;
  normalized: number;
  weighted: number;
  dimension_counts: Dimensions;
  penalties: Penalty[];
  evidence_refs: Array<{
    proposal_id: string;
    page: number;
  }>;
}

export interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  overall: {
    raw_sum: number;
    effective_sum: number;
    weighted_sum: number;
    coverage_critical_weighted_sum: number;
    notes: string;
  };
}

export interface RankingEntry {
  rank: number;
  candidate_id: string;
  weighted_sum?: number;
  coverage_critical_weighted_sum?: number;
}

export interface Ranking {
  method_version: string;
  weights: Record<string, number>;
  ranking_overall_weighted: RankingEntry[];
  ranking_critical_weighted: RankingEntry[];
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
};

export const CRITICAL_PILLARS: PillarId[] = ['P1', 'P2', 'P3', 'P4', 'P5', 'P7'];
