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
// FUNCIONES DE RIESGO FISCAL
// ============================================

export function getFiscalRiskLevel(candidateId: string): FiscalRiskLevel {
  const analysis = analysisByCandidate[candidateId];
  return analysis?.risk_level || 'BAJO';
}

export function getFiscalPenalty(candidateId: string): number {
  const score = scoresByCandidate[candidateId];
  return score?.overall.fiscal_penalty_applied || 0;
}

export function getFiscalFlags(candidateId: string) {
  const score = scoresByCandidate[candidateId];
  return score?.fiscal_analysis.flags || {
    attacks_fiscal_rule: false,
    proposes_debt_increase: false,
    proposes_tax_increase: false,
    shows_fiscal_responsibility: false,
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
    topCandidates: candidateScoresForPillar.slice(0, 5),
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
// ESTADÍSTICAS FISCALES
// ============================================

export function getFiscalStats() {
  const stats = {
    total: candidates.length,
    attackFiscalRule: 0,
    proposeDebt: 0,
    proposeTax: 0,
    lowRisk: 0,
    mediumRisk: 0,
    highRisk: 0,
  };

  candidateScores.forEach(cs => {
    if (cs.fiscal_analysis.flags.attacks_fiscal_rule) stats.attackFiscalRule++;
    if (cs.fiscal_analysis.flags.proposes_debt_increase) stats.proposeDebt++;
    if (cs.fiscal_analysis.flags.proposes_tax_increase) stats.proposeTax++;
  });

  detailedAnalysis.forEach(da => {
    if (da.risk_level === 'BAJO') stats.lowRisk++;
    else if (da.risk_level === 'MEDIO') stats.mediumRisk++;
    else stats.highRisk++;
  });

  return stats;
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
