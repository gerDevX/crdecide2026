import type {
  Candidate,
  Pillar,
  Proposal,
  CandidateScore,
  Ranking,
  DetailedAnalysis,
  PillarId,
  CandidateIndex,
  PillarIndex,
  ScoresByCandidate,
  AnalysisByCandidate,
  PillarCardData,
  FiscalRiskLevel,
  OmissionAnalysis,
  PenaltyType,
  PRIORITY_PILLARS,
} from './types';

// Importar datos JSON
import candidatesData from '../../../analysis/data/candidates.json';
import pillarsData from '../../../analysis/data/pillars.json';
import proposalsData from '../../../analysis/data/proposals.json';
import candidateScoresData from '../../../analysis/data/candidate_scores.json';
import rankingData from '../../../analysis/data/ranking.json';
import detailedAnalysisData from '../../../analysis/data/detailed_analysis.json';

// ============================================
// DATOS BASE
// ============================================

export const candidates: Candidate[] = candidatesData as Candidate[];
export const pillars: Pillar[] = pillarsData as Pillar[];
export const proposals: Proposal[] = proposalsData as Proposal[];
export const candidateScores: CandidateScore[] = candidateScoresData as CandidateScore[];
export const ranking: Ranking = rankingData as Ranking;
export const detailedAnalysis: DetailedAnalysis[] = detailedAnalysisData as DetailedAnalysis[];

// ============================================
// ÍNDICES
// ============================================

export const candidateIndex: CandidateIndex = candidates.reduce((acc, c) => {
  acc[c.candidate_id] = c;
  return acc;
}, {} as CandidateIndex);

export const pillarIndex: PillarIndex = pillars.reduce((acc, p) => {
  acc[p.pillar_id] = p;
  return acc;
}, {} as PillarIndex);

export const scoresByCandidate: ScoresByCandidate = candidateScores.reduce((acc, cs) => {
  acc[cs.candidate_id] = cs;
  return acc;
}, {} as ScoresByCandidate);

export const analysisByCandidate: AnalysisByCandidate = detailedAnalysis.reduce((acc, a) => {
  acc[a.candidate_id] = a;
  return acc;
}, {} as AnalysisByCandidate);

// ============================================
// FUNCIONES DE CONSULTA
// ============================================

export function getCandidate(id: string): Candidate | undefined {
  return candidateIndex[id];
}

export function getPillar(id: string): Pillar | undefined {
  return pillarIndex[id];
}

export function getCandidateScore(candidateId: string): CandidateScore | undefined {
  return scoresByCandidate[candidateId];
}

export function getCandidateAnalysis(candidateId: string): DetailedAnalysis | undefined {
  return analysisByCandidate[candidateId];
}

export function getProposalsByCandidate(candidateId: string): Proposal[] {
  return proposals.filter(p => p.candidate_id === candidateId);
}

export function getProposalsByPillar(pillarId: PillarId): Proposal[] {
  return proposals.filter(p => p.pillar_id === pillarId);
}

export function getProposalsByCandidateAndPillar(candidateId: string, pillarId: PillarId): Proposal[] {
  return proposals.filter(p => p.candidate_id === candidateId && p.pillar_id === pillarId);
}

export function getPillarScoreForCandidate(candidateId: string, pillarId: PillarId) {
  const score = scoresByCandidate[candidateId];
  if (!score) return undefined;
  return score.pillar_scores.find(ps => ps.pillar_id === pillarId);
}

// ============================================
// FUNCIONES DE RIESGO Y RESPONSABILIDAD
// ============================================

export function getFiscalRiskLevel(candidateId: string): FiscalRiskLevel {
  const analysis = analysisByCandidate[candidateId];
  return analysis?.risk_level || 'BAJO';
}

export function getFiscalPenalty(candidateId: string): number {
  const score = scoresByCandidate[candidateId];
  return score?.fiscal_analysis.total_penalty || 0;
}

export function getOmissionPenalty(candidateId: string): number {
  const score = scoresByCandidate[candidateId];
  if (!score?.omission_analysis) return 0;
  return score.omission_analysis.urgency_penalty + score.omission_analysis.pillar_penalty;
}

export function getTotalPenalty(candidateId: string): number {
  const score = scoresByCandidate[candidateId];
  return score?.overall.total_penalties_applied || 0;
}

export function getFiscalFlags(candidateId: string) {
  const score = scoresByCandidate[candidateId];
  return score?.fiscal_analysis.flags || {
    attacks_fiscal_rule: false,
    proposes_debt_increase: false,
    shows_fiscal_responsibility: false,
  };
}

export function getOmissionAnalysis(candidateId: string): OmissionAnalysis | undefined {
  const score = scoresByCandidate[candidateId];
  if (!score?.omission_analysis) return undefined;
  
  // Convertir estructura v6 a formato compatible
  const oa = score.omission_analysis;
  return {
    ignores_security: !oa.urgency_coverage.security_operations?.covered,
    ignores_ccss: !oa.urgency_coverage.ccss_crisis?.covered,
    ignores_employment: !oa.urgency_coverage.formal_employment?.covered,
    ignores_organized_crime: !oa.urgency_coverage.organized_crime?.covered,
    missing_priority_pillars: oa.missing_pillars || [],
    total_penalty: oa.urgency_penalty + oa.pillar_penalty,
  };
}

export function getCandidateStrengths(candidateId: string): string[] {
  const analysis = analysisByCandidate[candidateId];
  return analysis?.strengths || [];
}

export function getCandidateWeaknesses(candidateId: string): string[] {
  const analysis = analysisByCandidate[candidateId];
  return analysis?.weaknesses || [];
}

// ============================================
// FUNCIONES DE COBERTURA DE URGENCIAS
// ============================================

export function getUrgencyCoverage(candidateId: string) {
  const analysis = analysisByCandidate[candidateId];
  return analysis?.urgency_coverage;
}

export function hasSecurityCoverage(candidateId: string): boolean {
  const coverage = getUrgencyCoverage(candidateId);
  return coverage?.security_operations?.covered || false;
}

export function hasCCSSCoverage(candidateId: string): boolean {
  const coverage = getUrgencyCoverage(candidateId);
  return coverage?.ccss_crisis?.covered || false;
}

export function hasEmploymentCoverage(candidateId: string): boolean {
  const coverage = getUrgencyCoverage(candidateId);
  return coverage?.formal_employment?.covered || false;
}

export function hasOrganizedCrimeCoverage(candidateId: string): boolean {
  const coverage = getUrgencyCoverage(candidateId);
  return coverage?.organized_crime?.covered || false;
}

// ============================================
// DATOS AGREGADOS POR PILAR
// ============================================

export function getPillarCardData(pillarId: PillarId): PillarCardData {
  const pillar = pillarIndex[pillarId];
  
  // Obtener scores de todos los candidatos para este pilar
  const candidateScoresForPillar = candidateScores.map(cs => {
    const pillarScore = cs.pillar_scores.find(ps => ps.pillar_id === pillarId);
    return {
      candidate: candidateIndex[cs.candidate_id],
      score: pillarScore!,
    };
  }).filter(x => x.score && x.candidate);

  // Ordenar por score
  candidateScoresForPillar.sort((a, b) => b.score.effective_score - a.score.effective_score);

  // Calcular promedio
  const avgScore = candidateScoresForPillar.length > 0 
    ? candidateScoresForPillar.reduce((sum, x) => sum + x.score.effective_score, 0) / candidateScoresForPillar.length
    : 0;

  return {
    pillar,
    avgScore,
    topCandidates: candidateScoresForPillar, // Devolver todos los candidatos, no solo top 5
  };
}

export function getAllPillarCardData(): PillarCardData[] {
  return pillars.map(p => getPillarCardData(p.pillar_id as PillarId));
}

// ============================================
// RANKING
// ============================================

export function getRankingWithCandidates() {
  return ranking.ranking_overall_weighted.map(entry => ({
    ...entry,
    candidate: candidateIndex[entry.candidate_id],
    analysis: analysisByCandidate[entry.candidate_id],
  }));
}

export function getPriorityRankingWithCandidates() {
  return ranking.ranking_priority_weighted.map(entry => ({
    ...entry,
    candidate: candidateIndex[entry.candidate_id],
    analysis: analysisByCandidate[entry.candidate_id],
  }));
}

export function getCriticalRankingWithCandidates() {
  return ranking.ranking_critical_weighted.map(entry => ({
    ...entry,
    candidate: candidateIndex[entry.candidate_id],
    analysis: analysisByCandidate[entry.candidate_id],
  }));
}

// ============================================
// ESTADÍSTICAS FISCALES Y DE OMISIÓN
// ============================================

export function getFiscalStats() {
  const stats = {
    total: candidates.length,
    attackFiscalRule: 0,
    proposeDebt: 0,
    lowRisk: 0,
    mediumRisk: 0,
    highRisk: 0,
    // Estadísticas de omisión
    ignoreSecurity: 0,
    ignoreCCSS: 0,
    ignoreEmployment: 0,
    ignoreOrganizedCrime: 0,
  };

  candidateScores.forEach(cs => {
    if (cs.fiscal_analysis.flags.attacks_fiscal_rule) stats.attackFiscalRule++;
    if (cs.fiscal_analysis.flags.proposes_debt_increase) stats.proposeDebt++;
    
    // Estadísticas de omisión (usando estructura v6)
    const oa = cs.omission_analysis;
    if (oa?.urgency_coverage) {
      if (!oa.urgency_coverage.security_operations?.covered) stats.ignoreSecurity++;
      if (!oa.urgency_coverage.ccss_crisis?.covered) stats.ignoreCCSS++;
      if (!oa.urgency_coverage.formal_employment?.covered) stats.ignoreEmployment++;
      if (!oa.urgency_coverage.organized_crime?.covered) stats.ignoreOrganizedCrime++;
    }
  });

  detailedAnalysis.forEach(da => {
    if (da.risk_level === 'BAJO') stats.lowRisk++;
    else if (da.risk_level === 'MEDIO') stats.mediumRisk++;
    else stats.highRisk++;
  });

  return stats;
}

// ============================================
// FUNCIONES DE PENALIZACIÓN
// ============================================

export function getAllPenalties(candidateId: string): { type: PenaltyType; label: string; value: number }[] {
  const score = scoresByCandidate[candidateId];
  if (!score) return [];

  const penalties: { type: PenaltyType; label: string; value: number }[] = [];

  // Penalizaciones por irresponsabilidad
  if (score.fiscal_analysis.flags.attacks_fiscal_rule) {
    penalties.push({ type: 'attacks_fiscal_rule', label: 'Ataca regla fiscal', value: -2 });
  }
  if (score.fiscal_analysis.flags.proposes_debt_increase) {
    penalties.push({ type: 'proposes_debt_increase', label: 'Más deuda', value: -1 });
  }

  // Penalizaciones por omisión (usando estructura v6)
  const oa = score.omission_analysis;
  if (oa?.urgency_coverage) {
    if (!oa.urgency_coverage.security_operations?.covered) {
      penalties.push({ type: 'ignores_security', label: 'Ignora seguridad', value: -1 });
    }
    if (!oa.urgency_coverage.ccss_crisis?.covered) {
      penalties.push({ type: 'ignores_ccss', label: 'Ignora CCSS', value: -1 });
    }
    if (!oa.urgency_coverage.formal_employment?.covered) {
      penalties.push({ type: 'ignores_employment', label: 'Ignora empleo', value: -0.5 });
    }
    if (!oa.urgency_coverage.organized_crime?.covered) {
      penalties.push({ type: 'ignores_organized_crime', label: 'Ignora crimen organizado', value: -0.5 });
    }
  }

  // Pilares prioritarios faltantes
  oa?.missing_pillars?.forEach(pillarId => {
    penalties.push({ 
      type: 'missing_priority_pillar', 
      label: `Falta ${pillarId}`, 
      value: -0.5 
    });
  });

  return penalties;
}

// ============================================
// UTILIDADES
// ============================================

export function formatScore(score: number, max: number = 4): string {
  return `${score}/${max}`;
}

export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

// Mapeo de pdf_id a URL oficial del TSE
const pdfUrlIndex: Record<string, string> = candidates.reduce((acc, c) => {
  acc[c.pdf_id] = c.pdf_url;
  return acc;
}, {} as Record<string, string>);

export function getPdfUrl(pdfId: string, page?: number): string {
  // Usar URL oficial del TSE si está disponible
  const officialUrl = pdfUrlIndex[pdfId];
  if (officialUrl && officialUrl !== 'no_especificado') {
    return page ? `${officialUrl}#page=${page}` : officialUrl;
  }
  // Fallback a archivo local
  const base = `/planes/${pdfId}.pdf`;
  return page ? `${base}#page=${page}` : base;
}

export function getOfficialPdfUrl(candidateId: string): string | undefined {
  const candidate = candidateIndex[candidateId];
  if (candidate?.pdf_url && candidate.pdf_url !== 'no_especificado') {
    return candidate.pdf_url;
  }
  return undefined;
}

export function getRiskColor(risk: FiscalRiskLevel): string {
  const colors: Record<FiscalRiskLevel, string> = {
    ALTO: 'text-red-600 bg-red-50 border-red-200',
    MEDIO: 'text-amber-600 bg-amber-50 border-amber-200',
    BAJO: 'text-green-600 bg-green-50 border-green-200',
  };
  return colors[risk];
}

export function getRiskEmoji(risk: FiscalRiskLevel): string {
  const emojis: Record<FiscalRiskLevel, string> = {
    ALTO: '🔴',
    MEDIO: '🟠',
    BAJO: '🟢',
  };
  return emojis[risk];
}

export function getPenaltyColor(penaltyType: PenaltyType): string {
  const fiscalPenalties = ['attacks_fiscal_rule', 'proposes_debt_increase'];
  if (fiscalPenalties.includes(penaltyType)) {
    return 'text-red-600 bg-red-50';
  }
  return 'text-amber-600 bg-amber-50';
}
