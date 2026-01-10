import type { AgeGroup } from './types';

const STORAGE_KEY = 'costarica-decide-age-group';

export function getAgeGroup(): AgeGroup | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(STORAGE_KEY) as AgeGroup | null;
}

export function setAgeGroup(age: AgeGroup): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, age);
  document.documentElement.setAttribute('data-age-group', age);
  // Dispatch custom event for reactive updates
  window.dispatchEvent(new CustomEvent('age-group-changed', { detail: age }));
}

export function hasAgeGroup(): boolean {
  if (typeof window === 'undefined') return false;
  return localStorage.getItem(STORAGE_KEY) !== null;
}

export function initAgeGroup(): AgeGroup {
  const stored = getAgeGroup();
  if (stored) {
    document.documentElement.setAttribute('data-age-group', stored);
    return stored;
  }
  return '36-49'; // Default
}

// ============================================
// CLASES CSS POR GRUPO DE EDAD
// ============================================

export interface AgeGroupStyles {
  container: string;
  card: string;
  text: string;
  heading: string;
  button: string;
  grid: string;
}

export function getAgeGroupStyles(age: AgeGroup): AgeGroupStyles {
  const styles: Record<AgeGroup, AgeGroupStyles> = {
    '18-35': {
      container: 'max-w-7xl',
      card: 'p-4',
      text: 'text-base',
      heading: 'text-xl font-semibold',
      button: 'py-2 px-4 text-sm',
      grid: 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4',
    },
    '36-49': {
      container: 'max-w-6xl',
      card: 'p-5',
      text: 'text-base',
      heading: 'text-2xl font-semibold',
      button: 'py-2.5 px-5 text-base',
      grid: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5',
    },
    '50+': {
      container: 'max-w-4xl',
      card: 'p-6',
      text: 'text-lg leading-relaxed',
      heading: 'text-3xl font-semibold',
      button: 'py-3 px-6 text-lg',
      grid: 'grid-cols-1 gap-6',
    },
  };
  return styles[age];
}

// ============================================
// CTAs POR GRUPO DE EDAD
// ============================================

export interface AgeGroupCTAs {
  viewDetail: string;
  compare: string;
  evidence: string;
  ranking: string;
  viewProposal: string;
}

export function getAgeGroupCTAs(age: AgeGroup): AgeGroupCTAs {
  const ctas: Record<AgeGroup, AgeGroupCTAs> = {
    '18-35': {
      viewDetail: 'Ver más',
      compare: 'Comparar',
      evidence: 'PDF ↗',
      ranking: 'Top 10',
      viewProposal: 'Ver',
    },
    '36-49': {
      viewDetail: 'Ver detalle',
      compare: 'Comparar candidatos',
      evidence: 'Ver en plan oficial',
      ranking: 'Ver ranking completo',
      viewProposal: 'Ver propuesta',
    },
    '50+': {
      viewDetail: 'Ver información completa',
      compare: 'Comparar propuestas de candidatos',
      evidence: 'Abrir documento oficial (PDF)',
      ranking: 'Ver todos los candidatos ordenados',
      viewProposal: 'Ver propuesta completa',
    },
  };
  return ctas[age];
}
