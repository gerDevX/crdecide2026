# Costa Rica Decide - Arquitectura del Sitio

## A) ESTRUCTURA DEL SITIO (IA / UX)

### Mapa de Rutas (URLs)

| Ruta | Descripción | Componentes Principales |
|------|-------------|------------------------|
| `/` | Home + Dashboard principal | `<ModeSelector/>`, `<PillarGrid/>`, `<QuickRanking/>` |
| `/pilares` | Vista grid de 10 pilares | `<PillarCard/>` × 10 |
| `/pilares/[id]` | Detalle de pilar (P1-P10) | `<PillarHeader/>`, `<CandidateRankingByPillar/>`, `<ProposalList/>` |
| `/candidatos` | Grid de todos los candidatos | `<CandidateCard/>` × 20 |
| `/candidatos/[id]` | Perfil de candidato | `<CandidateHeader/>`, `<CandidateMatrix/>`, `<FiscalRiskBadge/>` |
| `/comparar` | Comparador (2-4 candidatos) | `<CompareSelector/>`, `<CompareTable/>`, `<CompareDetail/>` |
| `/ranking` | Rankings ponderados (3 tipos) | `<RankingTable/>`, `<FiscalRiskBadge/>` |
| `/metodologia` | Explicación del análisis | Contenido estático |
| `/acerca` | Propósito y transparencia | Contenido estático |

### Componentes por Página

#### Home (`/`)
```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo] Costa Rica Decide 2026    [Modo ▼] [🔍 Transparencia ▼]    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ModeSelector (si primera visita)                           │   │
│  │  "¿Cómo prefieres explorar?"                                │   │
│  │  [🚀 Express] [📊 Dashboard] [📖 Lectura]                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  EXPLORA LOS 10 PILARES NACIONALES                                 │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │   P1   │ │   P2   │ │   P3   │ │   P4   │ │   P5   │           │
│  │ Fiscal │ │Empleo  │ │Seguri. │ │ Salud  │ │ Educ.  │           │
│  │ ████▓░ │ │ ███▓░░ │ │ ████░░ │ │ ███▓░░ │ │ ████░░ │           │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘           │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │   P6   │ │   P7   │ │   P8   │ │   P9   │ │  P10   │           │
│  │Ambiente│ │Reforma │ │ Social │ │Exterior│ │Infraest│           │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘           │
│                                                                     │
│  🔴 ALERTA FISCAL: X candidatos atacan la regla fiscal            │
│                                                                     │
│  🏆 RANKING RÁPIDO                                                 │
│  1. FA   🟢 ████████████ 0.98                                      │
│  2. PSD  🟢 ██████████░░ 0.91                                      │
│  3. PNR  🟠 █████████░░░ 0.86                                      │
│                                                                     │
│  [Ver ranking completo] [Comparar candidatos]                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### Perfil de Candidato (`/candidatos/[id]`)
```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Candidatos   FA: Frente Amplio                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Puntaje: 0.98  │  Rank: #1  │  Riesgo: 🟢 BAJO                    │
│                                                                     │
│  MATRIZ DE PILARES                                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ P1 4/4 │ P2 3/4 │ P3 4/4 │ P4 4/4 │ P5 4/4 │               │   │
│  │ P6 3/4 │ P7 4/4 │ P8 3/4 │ P9 3/4 │P10 3/4 │               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  📊 ANÁLISIS FISCAL                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Responsabilidad fiscal: Sí ✓                                │   │
│  │ Ataca regla fiscal: No ✓                                    │   │
│  │ Propone más deuda: No ✓                                     │   │
│  │ Propone más impuestos: No ✓                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  💪 FORTALEZAS                                                     │
│  • Plan fiscal detallado con fuentes de financiamiento             │
│  • Propuestas de seguridad con plazos definidos                    │
│                                                                     │
│  ⚠️ DEBILIDADES                                                    │
│  • No menciona política exterior                                    │
│  • Ambiente recibe poca atención                                    │
│                                                                     │
│  [📄 Ver plan de gobierno PDF]                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Vista por Defecto según Modo

| Modo | Vista Default | Densidad | Detalle Expandido |
|------|---------------|----------|-------------------|
| Express | Cards full-screen | Una a la vez | Swipe para ver |
| Dashboard | Cards + Grid | Alta (grid 2-3 cols) | Tabs disponibles |
| Lectura | Lista vertical | Baja (1 col) | Siempre visible |

---

## B) MODELO DE DATOS (TypeScript)

### Data Contract

```typescript
// ============================================
// TIPOS BASE
// ============================================

type AgeGroup = '18-35' | '36-49' | '50+';
type VisualMode = 'express' | 'dashboard' | 'reading';
type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9' | 'P10';
type FiscalRiskLevel = 'ALTO' | 'MEDIO' | 'BAJO';

// ============================================
// ENTIDADES PRINCIPALES
// ============================================

interface Candidate {
  candidate_id: string;
  candidate_name: string;
  party_name: string;
  pdf_id: string;
  pdf_title: string;
  pdf_url: string;
}

interface Pillar {
  pillar_id: PillarId;
  pillar_name: string;
  weight: number;
}

interface Dimensions {
  existence: 0 | 1;
  when: 0 | 1;
  how: 0 | 1;
  funding: 0 | 1;
}

interface ExtractedFields {
  when_text: string;
  how_text: string;
  funding_text: string;
}

interface Evidence {
  pdf_id: string;
  page: number;
  snippet: string;
}

interface Proposal {
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
// ANÁLISIS FISCAL
// ============================================

interface FiscalPenalty {
  type: 'attacks_fiscal_rule' | 'proposes_debt_increase' | 'proposes_tax_increase' | 'urgency_omission';
  value: number;
  reason: string;
  evidence?: string;
}

interface FiscalFlags {
  attacks_fiscal_rule: boolean;
  proposes_debt_increase: boolean;
  proposes_tax_increase: boolean;
  shows_fiscal_responsibility: boolean;
}

interface FiscalAnalysis {
  flags: FiscalFlags;
  total_penalty: number;
  evidence: string[];
}

// ============================================
// SCORES
// ============================================

interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;
  effective_score: number;
  normalized: number;
  weighted: number;
  penalties: FiscalPenalty[];
}

interface CandidateScore {
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

// ============================================
// ANÁLISIS DETALLADO
// ============================================

interface DetailedAnalysis {
  candidate_id: string;
  pdf_id: string;
  total_pages: number;
  fiscal_responsibility: FiscalFlags;
  fiscal_evidence: string[];
  urgency_coverage: UrgencyCoverage;
  strengths: string[];
  weaknesses: string[];
  risk_level: FiscalRiskLevel;
}

// ============================================
// RANKING
// ============================================

interface RankingEntry {
  rank: number;
  candidate_id: string;
  weighted_sum?: number;
  fiscal_penalty?: number;
  priority_weighted_sum?: number;
  critical_weighted_sum?: number;
}

interface Ranking {
  method_version: string;
  weights: Record<PillarId, number>;
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
// ÍNDICES PARA NAVEGACIÓN RÁPIDA
// ============================================

interface CandidateIndex {
  [candidate_id: string]: Candidate;
}

interface PillarIndex {
  [pillar_id: string]: Pillar;
}

interface ScoresByCandidate {
  [candidate_id: string]: CandidateScore;
}

interface AnalysisByCandidate {
  [candidate_id: string]: DetailedAnalysis;
}

// ============================================
// CONSTANTES DE UI
// ============================================

const PILLAR_ICONS: Record<PillarId, string> = {
  P1: '💰', P2: '💼', P3: '🛡️', P4: '🏥', P5: '📚',
  P6: '🌿', P7: '⚖️', P8: '🤝', P9: '🌎', P10: '🏗️',
};

const PRIORITY_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7'];
const CRITICAL_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7', 'P2', 'P5'];
```

### Estructura de Datos JSON

```
analysis/data/
├── candidates.json          # 20 candidatos
├── pillars.json             # 10 pilares con pesos
├── proposals.json           # ~3,400 propuestas
├── candidate_scores.json    # Scores + análisis fiscal
├── detailed_analysis.json   # Fortalezas, debilidades, riesgo
└── ranking.json             # 3 tipos de ranking
```

---

## C) UI DEL COMPARADOR (Nivel Quirúrgico)

### Layout Comparador (`/comparar`)

```
┌─────────────────────────────────────────────────────────────────────┐
│  COMPARAR CANDIDATOS                                    [X Limpiar] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SELECCIONA 2 A 4 CANDIDATOS                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ [FA ✓] [PLN ✓] [PUSC ✓] [PNR ○] [PSD ○] [+15 más...]       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│  ┌─────────── STICKY HEADER ───────────┐                           │
│  │        │ FA      │ PLN     │ PUSC   │                           │
│  │        │ 0.98    │ 0.68    │ 0.75   │                           │
│  │ Riesgo │ 🟢 BAJO │ 🟠 MEDIO│ 🔴 ALTO│                           │
│  └────────┴─────────┴─────────┴────────┘                           │
│                                                                     │
│  ┌─────────── SCROLLABLE BODY ─────────┐                           │
│  │ P1 Fiscal                           │                           │
│  │        │ 4/4 ████│ 2/4 ██░░│ 3/4 ███│                           │
│  │        │ [E✓C✓H✓F✓]│[E✓C○H✓F○]│[E✓C✓H✓F○]                       │
│  │        │         │         │        │                           │
│  │ ─ ─ ─ ─│─ ─ ─ ─ ─│─ ─ ─ ─ ─│─ ─ ─ ─ │                           │
│  │ P2 Empleo                           │                           │
│  │        │ 3/4 ████│ 3/4 ████│ 2/4 ██░│                           │
│  │ ...                                 │                           │
│  └─────────────────────────────────────┘                           │
│                                                                     │
│  [Vista: ○ Resumen  ● Detalle con evidencia]                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Comportamiento de Elementos

| Elemento | Comportamiento | Breakpoint |
|----------|---------------|------------|
| Header con candidatos | **Sticky** top:0 | Siempre |
| Selector de candidatos | Colapsa a dropdown | < 768px |
| Filas de pilares | Scroll vertical | Siempre |
| Columnas de candidatos | Scroll horizontal | < 1024px |
| Toggle Resumen/Detalle | Fixed bottom | Mobile |

### Vista Resumen vs Detalle

**Resumen (default Express)**
- Solo score y barra
- Badge de riesgo fiscal compacto
- Sin snippet

**Detalle (default Dashboard, Lectura)**
- Score + barra + dimensiones expandidas
- Snippet de evidencia visible
- Link a PDF con página
- Análisis fiscal completo

### Componentes Específicos

#### `<ModeSelector/>`
```
Props: { onSelect: (mode: VisualMode) => void }
State: isOpen (true si no hay preferencia guardada)
UI: Modal con 3 opciones visuales, cierra al seleccionar
Storage: localStorage.setItem('costarica-decide-mode', value)
```

#### `<PillarCard/>`
```
Props: {
  pillar: Pillar;
  avgScore: number;
  topCandidate?: { name: string; score: number };
  mode: VisualMode;
}
UI Express: Card compacta, barra horizontal, sin texto extra
UI Dashboard: Card con descripción corta expandible
UI Lectura: Card vertical, texto grande, barra ancha
```

#### `<ScoreBar/>`
```
Props: {
  score: number;
  max: number;
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}
UI: Barra horizontal con segmentos (1-4), color gradiente
```

#### `<DimensionBadges/>`
```
Props: {
  dimensions: Dimensions;
  compact?: boolean;
}
UI Compact: [E✓] [C✓] [H○] [F○]
UI Expanded: Existencia ✓ | Cuándo ✓ | Cómo ○ | Fondos ○
Colors: ✓ = green-600, ○ = gray-400
```

#### `<FiscalRiskBadge/>`
```
Props: {
  risk: FiscalRiskLevel;
  compact?: boolean;
}
UI Compact: 🟢 / 🟠 / 🔴
UI Expanded: 🟢 BAJO / 🟠 MEDIO / 🔴 ALTO + tooltip con explicación
Colors: BAJO = green, MEDIO = amber, ALTO = red
```

#### `<CandidateMatrix/>`
```
Props: {
  candidate: Candidate;
  scores: PillarScore[];
  mode: VisualMode;
}
UI: Grid de 10 pilares con score visual
Hover: Muestra nombre del pilar y score numérico
```

#### `<EvidenceLink/>`
```
Props: {
  pdfId: string;
  page: number;
  snippet: string;
}
UI: Link con ícono PDF + "Ver en plan oficial (p.23)"
Href: /planes/{pdfId}.pdf#page={page}
```

---

## D) 3 MODOS VISUALES

### Diferencias Concretas

| Aspecto | Express 🚀 | Dashboard 📊 | Lectura 📖 |
|---------|------------|--------------|------------|
| **Layout** | Full-screen cards | Grid responsivo | Una columna |
| **Base font** | 16px | 16px | 20px |
| **Headings** | text-2xl bold | text-xl semibold | text-3xl bold |
| **Card padding** | p-4 | p-5 | p-6 |
| **Grid columns** | 1 | 2-3 | 1 |
| **Animaciones** | Sí (suaves) | Sutiles | Ninguna |
| **Riesgo fiscal** | Emoji | Badge + texto | Texto completo |

### CTAs por Modo

| Acción | Express | Dashboard | Lectura |
|--------|---------|-----------|---------|
| Ver detalle | "Ver más" | "Ver detalle" | "Ver propuesta completa" |
| Comparar | "Comparar" | "Comparar candidatos" | "Comparar propuestas" |
| Evidencia | "PDF ↗" | "Ver en plan oficial" | "Abrir documento oficial (PDF)" |
| Ranking | "Top 10" | "Ver ranking completo" | "Ver todos los candidatos" |

### Implementación Técnica

```typescript
// lib/mode.ts

export type VisualMode = 'express' | 'dashboard' | 'reading';

const STORAGE_KEY = 'costarica-decide-mode';

export function getMode(): VisualMode | null;
export function setMode(mode: VisualMode): void;
export function hasSelectedMode(): boolean;
export function getModeClasses(mode: VisualMode): Record<string, string>;
```

### Selector en Header

```
┌─────────────────────────────────────────────────┐
│  [Logo]  Pilares  Ranking  Candidatos  │ 📊 ▼  │
│                                        ├──────┤
│                                        │🚀 18-35│
│                                        │📊 36-49│
│                                        │📖 50+ ✓│
│                                        └──────┘
└─────────────────────────────────────────────────┘
```

---

## E) STACK Y PLAN DE IMPLEMENTACIÓN

### Stack Técnico

| Categoría | Tecnología |
|-----------|------------|
| Framework | Astro 4.x |
| Styling | Tailwind CSS 3.x |
| Lenguaje | TypeScript 5.x |
| Iconos | Emojis + Lucide Icons |
| Fuentes | System UI (fallbacks) |
| PDF Viewer | Link externo (navegador nativo) |

### Estructura de Carpetas

```
site/
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
├── package.json
│
├── public/
│   ├── planes/              # PDFs de planes de gobierno
│   ├── favicon.svg
│   ├── icons/
│   ├── manifest.json
│   ├── sw.js
│   └── offline.html
│
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.astro
│   │   │   └── Footer.astro
│   │   │
│   │   ├── ui/
│   │   │   ├── ModeSelector.astro
│   │   │   ├── AgeGateModal.astro
│   │   │   ├── ScoreBar.astro
│   │   │   ├── DimensionBadges.astro
│   │   │   ├── EvidenceLink.astro
│   │   │   └── FiscalRiskBadge.astro
│   │   │
│   │   ├── modes/
│   │   │   ├── express/
│   │   │   │   ├── ExpressCard.astro
│   │   │   │   └── ExpressSwiper.astro
│   │   │   ├── dashboard/
│   │   │   └── reading/
│   │   │       └── ReadingRanking.astro
│   │   │
│   │   ├── pillars/
│   │   │   ├── PillarCard.astro
│   │   │   └── PillarGrid.astro
│   │   │
│   │   ├── candidates/
│   │   │   ├── CandidateCard.astro
│   │   │   └── CandidateMatrix.astro
│   │   │
│   │   └── ranking/
│   │       ├── RankingTable.astro
│   │       └── QuickRanking.astro
│   │
│   ├── layouts/
│   │   └── BaseLayout.astro
│   │
│   ├── pages/
│   │   ├── index.astro
│   │   ├── pilares/
│   │   │   ├── index.astro
│   │   │   └── [id].astro
│   │   ├── candidatos/
│   │   │   ├── index.astro
│   │   │   └── [id].astro
│   │   ├── comparar.astro
│   │   ├── ranking.astro
│   │   ├── metodologia.astro
│   │   └── acerca.astro
│   │
│   ├── lib/
│   │   ├── data.ts           # Carga de JSON + funciones
│   │   ├── types.ts          # TypeScript types
│   │   ├── mode.ts           # Gestión de modo visual
│   │   └── age-group.ts      # Backward compatibility
│   │
│   └── styles/
│       └── global.css
│
└── analysis/                 # Symlink a ../analysis/
    ├── data/
    └── planes/
```

### Estrategia de Build y Performance

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'static',
  build: {
    assets: '_assets',
    inlineStylesheets: 'auto',
  },
});
```

**Optimizaciones:**
1. Pre-render todas las rutas estáticas
2. JSON pequeños (<50KB) inlineados
3. Sin JavaScript para páginas informativas
4. Islands solo para interactividad (compare, mode selector)

### Comandos de Desarrollo

```bash
# Desarrollo
npm run dev

# Build
npm run build

# Preview
npm run preview
```

---

## F) PÁGINA /METODOLOGIA (Copy Listo)

```markdown
# ¿Cómo funciona Costa Rica Decide?

## ¿Qué es esto?

Costa Rica Decide es una herramienta ciudadana que te ayuda a entender qué proponen los candidatos presidenciales para el período 2026-2030. 

**No te decimos por quién votar.** Solo organizamos la información de los planes de gobierno oficiales para que puedas compararlos fácilmente.

---

## ¿De dónde salen los datos?

Todos los datos provienen de los **planes de gobierno oficiales** presentados por cada partido político al Tribunal Supremo de Elecciones (TSE). 

Estos documentos son públicos y los puedes descargar directamente desde este sitio.

---

## ¿Qué son los pilares?

Organizamos las propuestas en **10 áreas temáticas** que consideramos fundamentales para el país:

| Pilar | ¿De qué trata? | Peso |
|-------|----------------|------|
| **P1. Sostenibilidad fiscal** | Impuestos, deuda, gasto público | 15% |
| **P2. Empleo y competitividad** | Trabajo, empresas, inversión | 12% |
| **P3. Seguridad ciudadana** | Policía, crimen, justicia | 18% |
| **P4. Salud pública (CCSS)** | Hospitales, medicina, pensiones | 15% |
| **P5. Educación** | Escuelas, universidades, capacitación | 12% |
| **P6. Ambiente** | Cambio climático, conservación | 4% |
| **P7. Reforma del Estado** | Corrupción, eficiencia, transparencia | 12% |
| **P8. Política social** | Pobreza, vulnerabilidad, subsidios | 5% |
| **P9. Política exterior** | Comercio internacional, diplomacia | 2% |
| **P10. Infraestructura** | Carreteras, puentes, APPs | 5% |

Los **pilares prioritarios** (P3, P4, P1, P7) suman el 60% del peso total.
Los **pilares críticos** (incluye P2 y P5) suman el 81%.

---

## ¿Cómo evaluamos cada propuesta?

Para cada propuesta que encontramos, respondemos **4 preguntas simples**:

### 1. ¿Existe la propuesta? (Existencia)
¿El plan menciona una acción concreta, no solo un deseo vago?

✓ "Crearemos un programa de becas para estudiantes de zonas rurales"  
✗ "Mejoraremos la educación"

### 2. ¿Dice cuándo? (Plazo)
¿Hay un plazo específico, no solo "en el futuro"?

✓ "En los primeros 100 días" o "Durante el cuatrienio 2026-2030"  
✗ "Gradualmente" o "Cuando sea posible"

### 3. ¿Dice cómo? (Mecanismo)
¿Explica el método, la ley, el programa o los pasos?

✓ "Mediante una reforma a la Ley de Contratación Pública"  
✗ "Implementaremos mejoras"

### 4. ¿Dice con qué fondos? (Financiamiento)
¿Indica de dónde saldrá el dinero?

✓ "Financiado con una reasignación del presupuesto del MOPT"  
✗ "Invertiremos millones" (sin decir de dónde)

---

## ¿Qué es el análisis fiscal?

Además de las 4 dimensiones, evaluamos la **responsabilidad fiscal** de cada candidato:

| Indicador | Qué significa | Penalización |
|-----------|---------------|--------------|
| 🔴 **Ataca regla fiscal** | Propone eliminar o flexibilizar la regla fiscal que mantiene las finanzas de CR a flote | -10% |
| 💰 **Más deuda** | Propone aumentar la deuda pública sin un plan claro de sostenibilidad | -5% |
| 📈 **Más impuestos** | Propone nuevos impuestos al pueblo costarricense | -3% |

### Niveles de Riesgo Fiscal

| Nivel | Emoji | Qué significa |
|-------|-------|---------------|
| **BAJO** | 🟢 | Candidato fiscalmente responsable |
| **MEDIO** | 🟠 | Algunas propuestas con impacto fiscal |
| **ALTO** | 🔴 | Propuestas que ponen en riesgo las finanzas del país |

---

## ¿Cómo se calcula el puntaje?

Cada propuesta puede obtener hasta **4 puntos** (uno por cada dimensión cumplida).

Para cada pilar, tomamos la **mejor propuesta** del candidato en ese tema.

El puntaje final se calcula así:
1. Se normaliza el puntaje de cada pilar (0 a 1)
2. Se multiplica por el peso del pilar
3. Se suman todos los pilares
4. Se aplican las penalizaciones fiscales

**Máximo posible:** 1.0 (todas las propuestas perfectas en todos los pilares)

---

## ¿Qué NO hace este análisis?

- ❌ **No evalúa viabilidad política** (si es posible aprobar algo en la Asamblea)
- ❌ **No juzga calidad ideológica** (si algo es "de izquierda" o "de derecha")
- ❌ **No predice resultados** (si funcionará o no)
- ❌ **No recomienda candidatos** (esa decisión es tuya)

---

## ¿Quién hizo esto?

Este proyecto fue desarrollado con herramientas de análisis automatizado. El código es abierto y los datos son verificables.

**Si encuentras un error**, puedes:
1. Descargar el PDF del candidato
2. Ir a la página indicada
3. Verificar el snippet de evidencia
4. Reportar inconsistencias

---

## Transparencia

- Todos los PDFs originales están disponibles en el sitio
- Cada propuesta tiene enlace a la página exacta del documento
- El código de análisis está disponible públicamente
- No recibimos financiamiento de partidos políticos

---

*Última actualización: Enero 2026*
*Versión del análisis: v4 (con análisis fiscal)*
```
