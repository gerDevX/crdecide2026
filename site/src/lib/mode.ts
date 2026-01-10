// ============================================
// VISUAL MODE MANAGEMENT
// ============================================

export type VisualMode = 'express' | 'dashboard' | 'reading';

const STORAGE_KEY = 'costarica-decide-mode';

// Mode metadata
export const MODE_INFO: Record<VisualMode, {
  name: string;
  emoji: string;
  description: string;
  tagline: string;
}> = {
  express: {
    name: 'Express',
    emoji: '🚀',
    description: 'Rápido y visual',
    tagline: 'Desliza para explorar',
  },
  dashboard: {
    name: 'Dashboard',
    emoji: '📊',
    description: 'Completo con detalles',
    tagline: 'Todo en un vistazo',
  },
  reading: {
    name: 'Lectura',
    emoji: '📖',
    description: 'Claro y sin distracciones',
    tagline: 'Lee con calma',
  },
};

// Default mode based on old age preference (migration)
function migrateFromAgeGroup(): VisualMode | null {
  if (typeof window === 'undefined') return null;
  
  const ageGroup = localStorage.getItem('costarica-decide-age-group');
  if (!ageGroup) return null;
  
  // Migrate old preference
  const modeMap: Record<string, VisualMode> = {
    '18-35': 'express',
    '36-49': 'dashboard',
    '50+': 'reading',
  };
  
  return modeMap[ageGroup] || null;
}

// Get current mode
export function getMode(): VisualMode | null {
  if (typeof window === 'undefined') return null;
  
  const stored = localStorage.getItem(STORAGE_KEY) as VisualMode | null;
  if (stored && isValidMode(stored)) return stored;
  
  // Try migration from old age system
  const migrated = migrateFromAgeGroup();
  if (migrated) {
    setMode(migrated);
    return migrated;
  }
  
  return null;
}

// Set mode
export function setMode(mode: VisualMode): void {
  if (typeof window === 'undefined') return;
  
  localStorage.setItem(STORAGE_KEY, mode);
  document.documentElement.setAttribute('data-mode', mode);
  
  // Also set the corresponding age group for backward compatibility
  const ageMap: Record<VisualMode, string> = {
    express: '18-35',
    dashboard: '36-49',
    reading: '50+',
  };
  localStorage.setItem('costarica-decide-age-group', ageMap[mode]);
  document.documentElement.setAttribute('data-age-group', ageMap[mode]);
}

// Validate mode
export function isValidMode(mode: string): mode is VisualMode {
  return ['express', 'dashboard', 'reading'].includes(mode);
}

// Check if mode is selected
export function hasSelectedMode(): boolean {
  return getMode() !== null;
}

// Get CSS class for current mode
export function getModeClasses(mode: VisualMode): {
  container: string;
  card: string;
  text: string;
  heading: string;
  button: string;
  grid: string;
} {
  const classes = {
    express: {
      container: 'px-4 py-6',
      card: 'p-4 rounded-2xl shadow-lg',
      text: 'text-base',
      heading: 'text-2xl font-bold',
      button: 'py-3 px-6 text-base font-semibold rounded-xl',
      grid: 'grid-cols-1',
    },
    dashboard: {
      container: 'px-4 sm:px-6 lg:px-8 py-8',
      card: 'p-5 rounded-xl',
      text: 'text-base',
      heading: 'text-xl font-semibold',
      button: 'py-2 px-4 text-sm font-medium rounded-lg',
      grid: 'grid-cols-2 lg:grid-cols-3 gap-4',
    },
    reading: {
      container: 'px-6 py-10 max-w-2xl mx-auto',
      card: 'p-6 rounded-lg',
      text: 'text-lg leading-relaxed',
      heading: 'text-3xl font-bold',
      button: 'py-4 px-8 text-lg font-medium rounded-lg',
      grid: 'grid-cols-1 gap-6',
    },
  };
  
  return classes[mode];
}

// Initialize mode on page load
export function initMode(): void {
  if (typeof window === 'undefined') return;
  
  const mode = getMode();
  if (mode) {
    document.documentElement.setAttribute('data-mode', mode);
  }
}
