import type {
  Candidate,
  Pillar,
  Proposal,
  CandidateScore,
  Ranking,
  PillarId,
  CandidateIndex,
  PillarIndex,
  ScoresByCandidate,
  PillarCardData,
} from './types';

// Importar datos JSON
import candidatesData from '../../../analysis/data/candidates.json';
import pillarsData from '../../../analysis/data/pillars.json';
import proposalsData from '../../../analysis/data/proposals.json';
import candidateScoresData from '../../../analysis/data/candidate_scores.json';
import rankingData from '../../../analysis/data/ranking.json';

// ============================================
// DATOS BASE
// ============================================

export const candidates: Candidate[] = candidatesData as Candidate[];
export const pillars: Pillar[] = pillarsData as Pillar[];
export const proposals: Proposal[] = proposalsData as Proposal[];
export const candidateScores: CandidateScore[] = candidateScoresData as CandidateScore[];
export const ranking: Ranking = rankingData as Ranking;

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
  }).filter(x => x.score);

  // Ordenar por score
  candidateScoresForPillar.sort((a, b) => b.score.effective_score - a.score.effective_score);

  // Calcular promedio
  const avgScore = candidateScoresForPillar.reduce((sum, x) => sum + x.score.effective_score, 0) / candidateScoresForPillar.length;

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
  }));
}

export function getCriticalRankingWithCandidates() {
  return ranking.ranking_critical_weighted.map(entry => ({
    ...entry,
    candidate: candidateIndex[entry.candidate_id],
  }));
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

export function getPdfUrl(pdfId: string, page?: number): string {
  const base = `/planes/${pdfId}.pdf`;
  return page ? `${base}#page=${page}` : base;
}
