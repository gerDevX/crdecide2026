# Costa Rica Decide - Arquitectura del Sitio

## A) ESTRUCTURA DEL SITIO (IA / UX)

### Mapa de Rutas (URLs)

| Ruta | Descripción | Componentes Principales |
|------|-------------|------------------------|
| `/` | Home + Dashboard principal | `<AgeGateModal/>`, `<PillarGrid/>`, `<QuickRanking/>` |
| `/pilares` | Vista grid de 9 pilares | `<PillarCard/>` × 9 |
| `/pilares/[id]` | Detalle de pilar (P1-P9) | `<PillarHeader/>`, `<CandidateRankingByPillar/>`, `<ProposalList/>` |
| `/candidatos` | Grid de todos los candidatos | `<CandidateCard/>` × 20 |
| `/candidatos/[id]` | Perfil de candidato | `<CandidateHeader/>`, `<CandidateMatrix/>`, `<ProposalsByPillar/>` |
| `/comparar` | Comparador (2-4 candidatos) | `<CompareSelector/>`, `<CompareTable/>`, `<CompareDetail/>` |
| `/ranking` | Rankings ponderados | `<RankingTable/>`, `<RankingCritical/>` |
| `/metodologia` | Explicación del análisis | Contenido estático |
| `/acerca` | Propósito y transparencia | Contenido estático |

### Componentes por Página

#### Home (`/`)
```
┌─────────────────────────────────────────────────────────┐
│  [Logo] Costa Rica Decide 2026    [Edad ▼] [Metodología]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │  AgeGateModal (si primera visita)                │   │
│  │  "¿Cuál es tu rango de edad?"                    │   │
│  │  [18-35] [36-49] [50+]                           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  EXPLORA LOS 9 PILARES NACIONALES                      │
│  ┌────────┐ ┌────────┐ ┌────────┐                      │
│  │   P1   │ │   P2   │ │   P3   │  ...                 │
│  │ Fiscal │ │Empleo  │ │Seguri. │                      │
│  │ ████▓░ │ │ ███▓░░ │ │ ████░░ │                      │
│  └────────┘ └────────┘ └────────┘                      │
│                                                         │
│  RANKING RÁPIDO                                        │
│  1. FA ████████████ 0.98                               │
│  2. PSD ██████████░ 0.91                               │
│  3. PNR █████████░░ 0.86                               │
│                                                         │
│  [Ver ranking completo] [Comparar candidatos]          │
└─────────────────────────────────────────────────────────┘
```

#### Pilar Detalle (`/pilares/[id]`)
```
┌─────────────────────────────────────────────────────────┐
│  ← Pilares   P1: Sostenibilidad Fiscal   Peso: 15%     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  RANKING EN ESTE PILAR                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 1. FA    [4/4] ████████████ Existencia ✓ Cuándo ✓│   │
│  │ 2. PSD   [3/4] █████████░░░ Existencia ✓ Cómo ✓  │   │
│  │ 3. PNR   [3/4] █████████░░░ Existencia ✓ Fondos ✓│   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  PROPUESTAS DESTACADAS                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [FA] Reforma tributaria progresiva               │   │
│  │ Dimensiones: [E✓] [C✓] [H✓] [F✓]                 │   │
│  │ "...modificar la estructura del impuesto..."     │   │
│  │ [Ver en PDF p.23 ↗]                              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Vista por Defecto según Edad

| Edad | Vista Default | Densidad | Detalle Expandido |
|------|---------------|----------|-------------------|
| 18-35 | Cards + Barras | Alta (grid 3-4 cols) | Colapsado |
| 36-49 | Cards + Tabs | Media (grid 2-3 cols) | Tab disponible |
| 50+ | Lista vertical | Baja (1 col) | Siempre visible |

---

## B) MODELO DE DATOS (TypeScript)

### Data Contract

```typescript
// ============================================
// TIPOS BASE
// ============================================

type AgeGroup = '18-35' | '36-49' | '50+';

type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9';

type ConflictType = 'constitutional' | 'fiscal' | 'none';

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

interface Compatibility {
  normative_fiscal: 0 | 1;
  conflict_type: ConflictType;
  reference: string;
  note: string;
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
  compatibility: Compatibility;
  evidence: Evidence;
  multi_pillar_source_proposal_id: string | null;
}

interface Penalty {
  type: 'compatibility';
  value: number;
  reason: string;
}

interface PillarScore {
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

interface CandidateScore {
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

interface RankingEntry {
  rank: number;
  candidate_id: string;
  weighted_sum?: number;
  coverage_critical_weighted_sum?: number;
}

interface Ranking {
  method_version: string;
  weights: Record<PillarId, number>;
  ranking_overall_weighted: RankingEntry[];
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

interface ProposalsByCandidate {
  [candidate_id: string]: Proposal[];
}

interface ProposalsByPillar {
  [pillar_id: string]: Proposal[];
}

interface ScoresByCandidate {
  [candidate_id: string]: CandidateScore;
}

// ============================================
// TIPOS PARA UI
// ============================================

interface PillarCardData {
  pillar: Pillar;
  avgScore: number;
  topCandidates: Array<{
    candidate: Candidate;
    score: PillarScore;
  }>;
}

interface CompareData {
  candidates: Candidate[];
  scores: CandidateScore[];
  proposalsByPillar: Record<PillarId, Proposal[]>;
}
```

### Estrategia de Partición de JSON

```
analysis/data/
├── candidates.json          # 5 KB  - Cargado globalmente
├── pillars.json             # 1 KB  - Cargado globalmente
├── ranking.json             # 4 KB  - Cargado globalmente
├── candidate_scores.json    # 140 KB - Cargado globalmente
├── proposals.json           # 5 MB  - Particionado ↓
│
└── partitioned/             # Generado en build
    ├── proposals-by-pillar/
    │   ├── P1.json
    │   ├── P2.json
    │   └── ...
    ├── proposals-by-candidate/
    │   ├── fa.json
    │   ├── pln.json
    │   └── ...
    └── indexes/
        ├── candidate-index.json
        ├── pillar-index.json
        └── score-index.json
```

### Estructura Recomendada para `analysis/data/`

Los JSONs actuales están bien. Solo agregar durante el build:
- Índices invertidos por candidato y pilar
- Propuestas particionadas para carga lazy

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
│  │ [FA ✓] [PLN ✓] [PUSC ✓] [PNR ○] [PSD ○] [+12 más...]       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ═══════════════════════════════════════════════════════════════   │
│                                                                     │
│  ┌─────────── STICKY HEADER ───────────┐                           │
│  │        │ FA      │ PLN     │ PUSC   │                           │
│  │        │ 0.98    │ 0.68    │ 0.75   │                           │
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
│  │        │ [E✓C✓H✓F○]│[E✓C○H✓F✓]│[E✓C○H✓F○]                       │
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

**Resumen (default 18-35)**
- Solo score y barra
- Badges de dimensiones compactos
- Sin snippet

**Detalle (default 36-49, 50+)**
- Score + barra + dimensiones expandidas
- Snippet de evidencia visible
- Link a PDF con página

### Componentes Específicos

#### `<AgeGateModal/>`
```
Props: { onSelect: (age: AgeGroup) => void }
State: isOpen (true si no hay preferencia guardada)
UI: Modal centrado, 3 botones grandes, cierra al seleccionar
Storage: localStorage.setItem('ageGroup', value)
```

#### `<PillarCard/>`
```
Props: {
  pillar: Pillar;
  avgScore: number;
  topCandidate?: { name: string; score: number };
  ageGroup: AgeGroup;
}
UI 18-35: Card compacta, barra horizontal, sin texto extra
UI 36-49: Card con descripción corta expandible
UI 50+: Card vertical, texto grande, barra ancha
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

#### `<CandidateMatrix/>`
```
Props: {
  candidate: Candidate;
  scores: PillarScore[];
  ageGroup: AgeGroup;
}
UI: Grid 3x3 de los 9 pilares con score visual
Hover: Muestra nombre del pilar y score numérico
```

#### `<CompareTable/>`
```
Props: {
  candidates: Candidate[];
  scores: CandidateScore[];
  view: 'summary' | 'detail';
}
UI: Tabla sticky-header con filas por pilar
Columns: Pilar | Candidato1 | Candidato2 | ...
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

## D) UX ADAPTATIVA POR EDAD

### Diferencias Concretas

| Aspecto | 18-35 | 36-49 | 50+ |
|---------|-------|-------|-----|
| **Base font** | 16px | 16px | 20px |
| **Headings** | text-xl | text-2xl | text-3xl |
| **Line height** | 1.4 | 1.5 | 1.7 |
| **Grid columns** | 3-4 | 2-3 | 1 |
| **Card padding** | p-4 | p-5 | p-6 |
| **Button size** | py-2 px-4 | py-2.5 px-5 | py-3 px-6 |
| **Animations** | Sí (subtle) | Mínimas | Ninguna |
| **Hover effects** | Sí | Sí | No |
| **Default view** | Resumen | Resumen + tabs | Detalle completo |
| **Scroll behavior** | Smooth | Smooth | Auto |

### CTAs por Edad

| Acción | 18-35 | 36-49 | 50+ |
|--------|-------|-------|-----|
| Ver detalle | "Ver más" | "Ver detalle" | "Ver propuesta completa" |
| Comparar | "Comparar" | "Comparar candidatos" | "Comparar propuestas" |
| Evidencia | "PDF ↗" | "Ver en plan oficial" | "Abrir documento oficial (PDF)" |
| Ranking | "Top 10" | "Ver ranking completo" | "Ver todos los candidatos" |

### Implementación Técnica

```typescript
// lib/age-group.ts

export type AgeGroup = '18-35' | '36-49' | '50+';

const STORAGE_KEY = 'costarica-decide-age-group';

export function getAgeGroup(): AgeGroup | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(STORAGE_KEY) as AgeGroup | null;
}

export function setAgeGroup(age: AgeGroup): void {
  localStorage.setItem(STORAGE_KEY, age);
  document.documentElement.setAttribute('data-age-group', age);
}

export function getAgeGroupClasses(age: AgeGroup): Record<string, string> {
  const classes = {
    '18-35': {
      container: 'grid-cols-3 lg:grid-cols-4 gap-4',
      card: 'p-4',
      text: 'text-base',
      heading: 'text-xl',
      button: 'py-2 px-4 text-sm',
    },
    '36-49': {
      container: 'grid-cols-2 lg:grid-cols-3 gap-5',
      card: 'p-5',
      text: 'text-base',
      heading: 'text-2xl',
      button: 'py-2.5 px-5 text-base',
    },
    '50+': {
      container: 'grid-cols-1 gap-6',
      card: 'p-6',
      text: 'text-lg leading-relaxed',
      heading: 'text-3xl',
      button: 'py-3 px-6 text-lg',
    },
  };
  return classes[age];
}
```

### Selector Manual en Header

```
┌─────────────────────────────────────────────────┐
│  [Logo]  Pilares  Candidatos  Comparar  │ 50+ ▼│
│                                         ├──────┤
│                                         │18-35 │
│                                         │36-49 │
│                                         │50+ ✓ │
│                                         └──────┘
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
| Iconos | Lucide Icons |
| Fuentes | Inter (system-ui fallback) |
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
│   └── planes/              # Symlink a analysis/planes/
│
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.astro
│   │   │   ├── Footer.astro
│   │   │   └── Layout.astro
│   │   │
│   │   ├── ui/
│   │   │   ├── ScoreBar.astro
│   │   │   ├── DimensionBadges.astro
│   │   │   ├── EvidenceLink.astro
│   │   │   ├── Button.astro
│   │   │   └── Card.astro
│   │   │
│   │   ├── pillars/
│   │   │   ├── PillarCard.astro
│   │   │   ├── PillarGrid.astro
│   │   │   └── PillarHeader.astro
│   │   │
│   │   ├── candidates/
│   │   │   ├── CandidateCard.astro
│   │   │   ├── CandidateMatrix.astro
│   │   │   └── CandidateHeader.astro
│   │   │
│   │   ├── compare/
│   │   │   ├── CompareSelector.astro
│   │   │   ├── CompareTable.astro
│   │   │   └── CompareDetail.astro
│   │   │
│   │   ├── ranking/
│   │   │   ├── RankingTable.astro
│   │   │   └── QuickRanking.astro
│   │   │
│   │   └── modals/
│   │       └── AgeGateModal.astro
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
│   │   ├── data.ts           # Carga de JSON
│   │   ├── types.ts          # TypeScript types
│   │   ├── age-group.ts      # Gestión de edad
│   │   ├── pillars.ts        # Helpers de pilares
│   │   └── format.ts         # Formateo de datos
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
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'proposals': ['./src/lib/proposals.ts'],
          },
        },
      },
    },
  },
});
```

**Optimizaciones:**
1. Pre-render todas las rutas estáticas
2. JSON pequeños (<50KB) inlineados
3. Proposals cargado lazy por página
4. Sin JavaScript para páginas informativas
5. Islands solo para interactividad (compare, age selector)

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

Organizamos las propuestas en **9 áreas temáticas** que consideramos fundamentales para el país:

| Pilar | ¿De qué trata? | Peso |
|-------|----------------|------|
| **P1. Sostenibilidad fiscal** | Impuestos, deuda, gasto público | 15% |
| **P2. Empleo y competitividad** | Trabajo, empresas, inversión | 15% |
| **P3. Seguridad ciudadana** | Policía, crimen, justicia | 15% |
| **P4. Salud pública (CCSS)** | Hospitales, medicina, pensiones | 15% |
| **P5. Educación** | Escuelas, universidades, capacitación | 15% |
| **P6. Ambiente** | Cambio climático, conservación | 5% |
| **P7. Reforma del Estado** | Corrupción, eficiencia, transparencia | 10% |
| **P8. Política social** | Pobreza, vulnerabilidad, subsidios | 8% |
| **P9. Política exterior** | Comercio internacional, diplomacia | 2% |

Los **pilares críticos** (P1-P5 y P7) suman el 85% del peso total porque son los temas que más impactan el día a día de los costarricenses.

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

## ¿Qué es la compatibilidad normativa?

Además de las 4 preguntas anteriores, verificamos si la propuesta **presenta conflictos claros** con:

- La **Constitución Política** de Costa Rica
- La **regla fiscal** vigente
- El **destino legal** de ciertos fondos (como los de la CCSS)

**Importante:** Solo marcamos conflicto cuando es **explícito y documentable**. Si el candidato propone reformar la ley para hacer algo, no hay conflicto.

---

## ¿Cómo se calcula el puntaje?

Cada propuesta puede obtener hasta **4 puntos** (uno por cada dimensión cumplida).

Para cada pilar, tomamos la **mejor propuesta** del candidato en ese tema.

El puntaje final se calcula así:
1. Se normaliza el puntaje de cada pilar (0 a 1)
2. Se multiplica por el peso del pilar
3. Se suman todos los pilares

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
*Versión del análisis: v2*
```
