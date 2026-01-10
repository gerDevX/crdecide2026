# Esquema de Datos - Costa Rica Decide 2026

Referencia rápida de la estructura de datos JSON del proyecto.

**Versión 6.0** - Sistema de penalizaciones neutral y estricto.

---

## Cambios en v6 (Respecto a v5)

| Cambio | Descripción | Razón |
|--------|-------------|-------|
| ❌ **Eliminado** | `proposes_tax_increase` | Era sesgo ideológico |
| ✅ **Mantenido** | `attacks_fiscal_rule` (-2) | Objetivo: ataca ley vigente |
| ✅ **Mantenido** | `proposes_debt_increase` (-1) | Objetivo: contexto de déficit |
| ➕ **Agregado** | `ignores_security` (-1) | No menciona seguridad operativa |
| ➕ **Agregado** | `ignores_ccss` (-1) | No menciona crisis de CCSS |
| ➕ **Agregado** | `ignores_employment` (-0.5) | No menciona empleo |
| ➕ **Agregado** | `ignores_organized_crime` (-0.5) | No menciona crimen organizado |
| ➕ **Agregado** | `missing_priority_pillar` (-0.5) | Por cada pilar prioritario sin propuesta |

---

## candidates.json

Array de candidatos presidenciales.

```typescript
interface Candidate {
  candidate_id: string;     // Slug único basado en nombre (ej: "alvaro-ramos")
  candidate_name: string;   // Nombre del candidato o "no_especificado"
  party_name: string;       // Nombre del partido o "no_especificado"
  pdf_id: string;           // ID del PDF (uppercase: "PLN", "FA")
  pdf_title: string;        // Título del plan de gobierno
  pdf_url: string;          // Ruta al PDF o "no_especificado"
}
```

---

## pillars.json

Array de los 10 pilares nacionales.

```typescript
interface Pillar {
  pillar_id: PillarId;      // "P1" - "P10"
  pillar_name: string;      // Nombre completo
  weight: number;           // Peso (0.02 - 0.18)
}

type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9' | 'P10';
```

**Pesos:**
| Pilar | Nombre | Peso |
|-------|--------|------|
| P1 | Sostenibilidad fiscal | 0.14 |
| P2 | Empleo y competitividad | 0.11 |
| P3 | Seguridad ciudadana | 0.18 |
| P4 | Salud pública (CCSS) | 0.16 |
| P5 | Educación | 0.10 |
| P6 | Ambiente | 0.03 |
| P7 | Reforma del Estado | 0.12 |
| P8 | Política social | 0.05 |
| P9 | Política exterior | 0.02 |
| P10 | Infraestructura/APPs | 0.09 |

---

## proposals.json

Array de propuestas extraídas de los planes de gobierno.

```typescript
interface Proposal {
  proposal_id: string;              // ID único (hash)
  candidate_id: string;             // Ref a candidate
  pillar_id: PillarId;              // Ref a pillar
  proposal_title: string;           // Título corto
  proposal_text: string;            // Texto resumen (máx 500 chars)
  dimensions: Dimensions;           // Evaluación D1-D4
  extracted_fields: ExtractedFields;// Textos extraídos
  evidence: Evidence;               // Referencia al PDF
}

interface Dimensions {
  existence: 0 | 1;  // D1: ¿Es acción concreta?
  when: 0 | 1;       // D2: ¿Tiene plazo verificable?
  how: 0 | 1;        // D3: ¿Describe mecanismo concreto?
  funding: 0 | 1;    // D4: ¿Indica fuente de financiamiento?
}

interface ExtractedFields {
  when_text: string;    // Texto del plazo o "no_especificado"
  how_text: string;     // Texto del mecanismo o "no_especificado"
  funding_text: string; // Texto del financiamiento o "no_especificado"
}

interface Evidence {
  pdf_id: string;   // ID del PDF
  page: number;     // Número de página (1-indexed)
  snippet: string;  // Fragmento de texto (≤240 chars)
}
```

---

## candidate_scores.json

Array de puntajes calculados por candidato, incluyendo análisis fiscal y de omisiones.

```typescript
interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  fiscal_analysis: FiscalAnalysis;
  omission_analysis: OmissionAnalysis;  // NUEVO en v6
  overall: Overall;
}

interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;           // 0-4 (suma de D1+D2+D3+D4)
  effective_score: number;     // raw_score con ajustes
  normalized: number;          // 0.0-1.0 (effective/4)
  weighted: number;            // normalized * peso_pilar
  penalties: Penalty[];        // Penalizaciones aplicadas
}

interface Penalty {
  type: PenaltyType;
  value: number;               // Valor negativo
  reason: string;              // Explicación
  evidence?: string;           // Texto de evidencia
}

// Tipos de penalización (v6)
type PenaltyType = 
  | 'attacks_fiscal_rule'      // Ataca la regla fiscal
  | 'proposes_debt_increase'   // Propone más deuda
  | 'ignores_security'         // No menciona seguridad
  | 'ignores_ccss'             // No menciona CCSS
  | 'ignores_employment'       // No menciona empleo
  | 'ignores_organized_crime'  // No menciona crimen organizado
  | 'missing_priority_pillar'; // Falta pilar prioritario

interface FiscalAnalysis {
  flags: FiscalFlags;
  total_penalty: number;
  evidence: string[];
}

// NOTA: proposes_tax_increase fue ELIMINADO (sesgo ideológico)
interface FiscalFlags {
  attacks_fiscal_rule: boolean;      // ¿Ataca la regla fiscal?
  proposes_debt_increase: boolean;   // ¿Propone más deuda sin plan?
  shows_fiscal_responsibility: boolean; // ¿Muestra responsabilidad fiscal?
}

// NUEVO en v6: Análisis de omisiones
interface OmissionAnalysis {
  ignores_security: boolean;          // No menciona seguridad operativa
  ignores_ccss: boolean;              // No menciona crisis de CCSS
  ignores_employment: boolean;        // No menciona empleo
  ignores_organized_crime: boolean;   // No menciona crimen organizado
  missing_priority_pillars: string[]; // Pilares prioritarios sin propuesta
  total_penalty: number;              // Suma de penalizaciones por omisión
  details: string[];                  // Descripciones de las omisiones
}

interface Overall {
  raw_sum: number;                      // Suma de raw_scores (0-40)
  effective_sum: number;                // Suma efectiva con ajustes
  weighted_sum: number;                 // Suma ponderada (0.0-1.0)
  priority_weighted_sum: number;        // Solo pilares prioritarios
  critical_weighted_sum: number;        // Solo pilares críticos
  fiscal_penalty_applied: number;       // Penalizaciones fiscales
  omission_penalty_applied: number;     // Penalizaciones por omisión (NUEVO)
  total_penalty_applied: number;        // Total de penalizaciones (NUEVO)
  notes: string;                        // Observaciones técnicas neutrales
}
```

---

## detailed_analysis.json

Array de análisis detallado por candidato.

```typescript
interface DetailedAnalysis {
  candidate_id: string;
  pdf_id: string;
  total_pages: number;
  fiscal_responsibility: FiscalFlags;
  fiscal_evidence: string[];
  urgency_coverage: UrgencyCoverageMap;
  strengths: string[];           // Fortalezas identificadas
  weaknesses: string[];          // Debilidades (incluye omisiones v6)
  risk_level: FiscalRiskLevel;   // 'ALTO' | 'MEDIO' | 'BAJO'
}

interface UrgencyCoverageMap {
  seguridad_operativa: UrgencyCoverage;
  salud_ccss: UrgencyCoverage;
  inversion_extranjera: UrgencyCoverage;
  empleo: UrgencyCoverage;
  educacion: UrgencyCoverage;
  infraestructura_APP: UrgencyCoverage;
  crimen_organizado: UrgencyCoverage;
}

interface UrgencyCoverage {
  covered: boolean;
  mentions: string[];
}

type FiscalRiskLevel = 'ALTO' | 'MEDIO' | 'BAJO';
```

---

## ranking.json

Rankings ordenados de candidatos.

```typescript
interface Ranking {
  method_version: string;                    // "v6_neutral_strict"
  weights: Record<string, number>;           // Pesos por pilar
  priority_pillars: string[];                // ['P3', 'P4', 'P1', 'P7']
  critical_pillars: string[];                // ['P3', 'P4', 'P1', 'P7', 'P2', 'P5']
  penalties_applied: {
    // Fiscales (objetivas)
    attacks_fiscal_rule: number;             // -2
    proposes_debt_increase: number;          // -1
    // Por omisión (NUEVO v6)
    ignores_security: number;                // -1
    ignores_ccss: number;                    // -1
    ignores_employment: number;              // -0.5
    ignores_organized_crime: number;         // -0.5
    missing_priority_pillar: number;         // -0.5 (por cada uno)
  };
  ranking_overall_weighted: RankingEntry[];  // Ranking general
  ranking_priority_weighted: RankingEntry[]; // Ranking pilares prioritarios
  ranking_critical_weighted: RankingEntry[]; // Ranking pilares críticos
}

interface RankingEntry {
  rank: number;                              // Posición (1-20)
  candidate_id: string;                      // ID del candidato
  weighted_sum?: number;                     // Para overall
  fiscal_penalty?: number;                   // Penalización fiscal
  omission_penalty?: number;                 // Penalización por omisión (NUEVO)
  total_penalty?: number;                    // Total de penalizaciones (NUEVO)
  priority_weighted_sum?: number;            // Para priority
  critical_weighted_sum?: number;            // Para critical
}
```

---

## Sistema de Penalizaciones v6

### Penalizaciones Fiscales (Objetivas - Basadas en Ley)

| Tipo | Descripción | Penalización |
|------|-------------|--------------|
| `attacks_fiscal_rule` | Propone eliminar/flexibilizar la regla fiscal | **-2** |
| `proposes_debt_increase` | Propone aumentar deuda sin plan de sostenibilidad | **-1** |

### Penalizaciones por Omisión (Basadas en Urgencias de CR)

| Tipo | Descripción | Penalización |
|------|-------------|--------------|
| `ignores_security` | No menciona seguridad operativa | **-1** |
| `ignores_ccss` | No menciona crisis de la CCSS | **-1** |
| `ignores_employment` | No menciona empleo/desempleo | **-0.5** |
| `ignores_organized_crime` | No menciona crimen organizado | **-0.5** |
| `missing_priority_pillar` | Falta propuesta en P1, P3, P4 o P7 | **-0.5** (por cada uno) |

### Criterios de Riesgo Fiscal

| Nivel | Emoji | Criterio |
|-------|-------|----------|
| **ALTO** | 🔴 | `attacks_fiscal_rule = true` O `total_penalty >= 3` |
| **MEDIO** | 🟠 | `total_penalty >= 1.5` AND `< 3` |
| **BAJO** | 🟢 | `total_penalty < 1.5` |

---

## Pilares Prioritarios y Críticos

```typescript
// Pilares prioritarios: 60% del peso (Seguridad, Salud, Finanzas, Reforma Estado)
const PRIORITY_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7'];

// Pilares críticos: 81% del peso (incluye Empleo y Educación)
const CRITICAL_PILLARS: PillarId[] = ['P3', 'P4', 'P1', 'P7', 'P2', 'P5'];
```

---

## Dimensiones D1-D4

| Dimensión | Nombre | Pregunta | Ejemplos Válidos |
|-----------|--------|----------|------------------|
| D1 | Existencia | ¿Es acción concreta? | "Crear...", "Implementar...", "Reformar..." |
| D2 | Cuándo | ¿Tiene plazo verificable? | "primer año", "primeros 100 días", "2026–2030" |
| D3 | Cómo | ¿Describe mecanismo? | programa definido, reforma legal, creación de institución |
| D4 | Fondos | ¿Indica financiamiento? | presupuesto, impuestos, cooperación, APP |

**raw_score = D1 + D2 + D3 + D4** (0-4)

---

## Metadata de Pilares (UI)

```typescript
const PILLAR_ICONS: Record<PillarId, string> = {
  P1: '💰', P2: '💼', P3: '🛡️', P4: '🏥', P5: '📚',
  P6: '🌿', P7: '⚖️', P8: '🤝', P9: '🌎', P10: '🏗️'
};

const PILLAR_COLORS: Record<PillarId, string> = {
  P1: 'emerald', P2: 'blue', P3: 'red', P4: 'pink', P5: 'amber',
  P6: 'green', P7: 'purple', P8: 'orange', P9: 'cyan', P10: 'slate'
};
```

---

## Ubicación de Archivos

```
analysis/
├── data/
│   ├── candidates.json           # 20 candidatos
│   ├── pillars.json              # 10 pilares
│   ├── proposals.json            # Propuestas por candidato/pilar
│   ├── candidate_scores.json     # Scores + análisis fiscal + omisiones
│   ├── detailed_analysis.json    # Fortalezas, debilidades, riesgo
│   └── ranking.json              # Rankings ponderados (3 tipos)
├── planes/
│   └── ... (20 PDFs)
└── recalculate_scores_v6.py      # Script de recálculo
```
