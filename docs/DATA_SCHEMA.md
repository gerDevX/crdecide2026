# Esquema de Datos - Costa Rica Decide 2026

Referencia rápida de la estructura de datos JSON del proyecto.

**Versión 4.0** - Análisis fiscal completo + 10 pilares nacionales.

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

**Ejemplo:**
```json
{
  "candidate_id": "alvaro-ramos",
  "candidate_name": "Álvaro Ramos",
  "party_name": "Liberación Nacional",
  "pdf_id": "PLN",
  "pdf_title": "Plan de Gobierno 2026–2030",
  "pdf_url": "https://tse.go.cr/planes/pln.pdf"
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
| P1 | Sostenibilidad fiscal | 0.15 |
| P2 | Empleo y competitividad | 0.12 |
| P3 | Seguridad ciudadana | 0.18 |
| P4 | Salud pública (CCSS) | 0.15 |
| P5 | Educación | 0.12 |
| P6 | Ambiente | 0.04 |
| P7 | Reforma del Estado | 0.12 |
| P8 | Política social | 0.05 |
| P9 | Política exterior | 0.02 |
| P10 | Infraestructura/APPs | 0.05 |

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

**Ejemplo:**
```json
{
  "proposal_id": "pln-a1b2c3d4",
  "candidate_id": "alvaro-ramos",
  "pillar_id": "P1",
  "proposal_title": "Reforma tributaria progresiva",
  "proposal_text": "Modificar la estructura del impuesto sobre la renta...",
  "dimensions": {
    "existence": 1,
    "when": 1,
    "how": 1,
    "funding": 1
  },
  "extracted_fields": {
    "when_text": "primer año de gobierno",
    "how_text": "reforma a la Ley del Impuesto sobre la Renta",
    "funding_text": "reasignación de exoneraciones fiscales"
  },
  "evidence": {
    "pdf_id": "PLN",
    "page": 23,
    "snippet": "...modificar la estructura del impuesto sobre la renta..."
  }
}
```

---

## candidate_scores.json

Array de puntajes calculados por candidato, incluyendo análisis fiscal.

```typescript
interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  fiscal_analysis: FiscalAnalysis;
  overall: Overall;
}

interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;           // 0-4 (suma de D1+D2+D3+D4)
  effective_score: number;     // raw_score con ajustes
  normalized: number;          // 0.0-1.0 (effective/4)
  weighted: number;            // normalized * peso_pilar
  penalties: FiscalPenalty[];  // Penalizaciones aplicadas
}

interface FiscalPenalty {
  type: 'attacks_fiscal_rule' | 'proposes_debt_increase' | 'proposes_tax_increase' | 'urgency_omission';
  value: number;               // Valor negativo
  reason: string;              // Explicación
  evidence?: string;           // Texto de evidencia
}

interface FiscalAnalysis {
  flags: FiscalFlags;
  total_penalty: number;
  evidence: string[];
}

interface FiscalFlags {
  attacks_fiscal_rule: boolean;      // ¿Ataca la regla fiscal?
  proposes_debt_increase: boolean;   // ¿Propone más deuda?
  proposes_tax_increase: boolean;    // ¿Propone más impuestos?
  shows_fiscal_responsibility: boolean; // ¿Muestra responsabilidad fiscal?
}

interface Overall {
  raw_sum: number;                   // Suma de raw_scores (0-40)
  effective_sum: number;             // Suma efectiva con ajustes
  weighted_sum: number;              // Suma ponderada (0.0-1.0)
  priority_weighted_sum: number;     // Solo pilares prioritarios
  critical_weighted_sum: number;     // Solo pilares críticos
  fiscal_penalty_applied: number;    // Total de penalizaciones fiscales
  notes: string;                     // Observaciones técnicas neutrales
}
```

**Ejemplo:**
```json
{
  "candidate_id": "alvaro-ramos",
  "pillar_scores": [
    {
      "pillar_id": "P1",
      "raw_score": 4,
      "effective_score": 4,
      "normalized": 1.0,
      "weighted": 0.15,
      "penalties": []
    }
  ],
  "fiscal_analysis": {
    "flags": {
      "attacks_fiscal_rule": false,
      "proposes_debt_increase": false,
      "proposes_tax_increase": false,
      "shows_fiscal_responsibility": true
    },
    "total_penalty": 0,
    "evidence": []
  },
  "overall": {
    "raw_sum": 28,
    "effective_sum": 28,
    "weighted_sum": 0.82,
    "priority_weighted_sum": 0.68,
    "critical_weighted_sum": 0.72,
    "fiscal_penalty_applied": 0,
    "notes": "Sin propuestas identificadas: P9"
  }
}
```

---

## detailed_analysis.json

Array de análisis detallado por candidato (fortalezas, debilidades, riesgo).

```typescript
interface DetailedAnalysis {
  candidate_id: string;
  pdf_id: string;
  total_pages: number;
  fiscal_responsibility: FiscalFlags;
  fiscal_evidence: string[];
  urgency_coverage: UrgencyCoverage;
  strengths: string[];           // Fortalezas identificadas
  weaknesses: string[];          // Debilidades identificadas
  risk_level: FiscalRiskLevel;   // 'ALTO' | 'MEDIO' | 'BAJO'
}

interface UrgencyCoverage {
  seguridad_operativa: Coverage;
  salud_ccss: Coverage;
  inversion_extranjera: Coverage;
  empleo: Coverage;
  educacion: Coverage;
  infraestructura_APP: Coverage;
  crimen_organizado: Coverage;
}

interface Coverage {
  covered: boolean;
  mentions: string[];
}

type FiscalRiskLevel = 'ALTO' | 'MEDIO' | 'BAJO';
```

**Ejemplo:**
```json
{
  "candidate_id": "alvaro-ramos",
  "pdf_id": "PLN",
  "total_pages": 45,
  "fiscal_responsibility": {
    "attacks_fiscal_rule": false,
    "proposes_debt_increase": false,
    "proposes_tax_increase": false,
    "shows_fiscal_responsibility": true
  },
  "fiscal_evidence": [],
  "urgency_coverage": {
    "seguridad_operativa": {
      "covered": true,
      "mentions": ["Fortalecimiento de la policía nacional..."]
    }
  },
  "strengths": [
    "Plan fiscal detallado con fuentes de financiamiento",
    "Propuestas de seguridad con plazos definidos"
  ],
  "weaknesses": [
    "No menciona política exterior",
    "Ambiente recibe poca atención"
  ],
  "risk_level": "BAJO"
}
```

---

## ranking.json

Rankings ordenados de candidatos.

```typescript
interface Ranking {
  method_version: string;                    // "v4"
  weights: Record<string, number>;           // Pesos por pilar
  priority_pillars: string[];                // ['P3', 'P4', 'P1', 'P7']
  critical_pillars: string[];                // ['P3', 'P4', 'P1', 'P7', 'P2', 'P5']
  penalties_applied: {
    attacks_fiscal_rule: number;             // -0.10
    proposes_debt_increase: number;          // -0.05
    proposes_tax_increase: number;           // -0.03
  };
  ranking_overall_weighted: RankingEntry[];  // Ranking general
  ranking_priority_weighted: RankingEntry[]; // Ranking pilares prioritarios
  ranking_critical_weighted: RankingEntry[]; // Ranking pilares críticos
}

interface RankingEntry {
  rank: number;                              // Posición (1-20)
  candidate_id: string;                      // ID del candidato
  weighted_sum?: number;                     // Para overall
  fiscal_penalty?: number;                   // Penalización fiscal aplicada
  priority_weighted_sum?: number;            // Para priority
  critical_weighted_sum?: number;            // Para critical
}
```

**Ejemplo:**
```json
{
  "method_version": "v4",
  "weights": {
    "P1": 0.15, "P2": 0.12, "P3": 0.18, "P4": 0.15, "P5": 0.12,
    "P6": 0.04, "P7": 0.12, "P8": 0.05, "P9": 0.02, "P10": 0.05
  },
  "priority_pillars": ["P3", "P4", "P1", "P7"],
  "critical_pillars": ["P3", "P4", "P1", "P7", "P2", "P5"],
  "penalties_applied": {
    "attacks_fiscal_rule": -0.10,
    "proposes_debt_increase": -0.05,
    "proposes_tax_increase": -0.03
  },
  "ranking_overall_weighted": [
    { "rank": 1, "candidate_id": "alvaro-ramos", "weighted_sum": 0.82, "fiscal_penalty": 0 },
    { "rank": 2, "candidate_id": "claudia-dobles", "weighted_sum": 0.78, "fiscal_penalty": -0.05 }
  ],
  "ranking_priority_weighted": [
    { "rank": 1, "candidate_id": "alvaro-ramos", "priority_weighted_sum": 0.68 }
  ],
  "ranking_critical_weighted": [
    { "rank": 1, "candidate_id": "alvaro-ramos", "critical_weighted_sum": 0.72 }
  ]
}
```

---

## Relaciones

```
candidates.json ←──── candidate_id ────→ proposals.json
                                              ↓
                                         pillar_id
                                              ↓
pillars.json ←───── pillar_id ─────→ candidate_scores.json
                                              ↓
                                         candidate_id
                                              ↓
                                      ranking.json

candidates.json ←──── candidate_id ────→ detailed_analysis.json
```

---

## Ubicación de Archivos

```
analysis/
├── data/
│   ├── candidates.json           # 20 candidatos
│   ├── pillars.json              # 10 pilares
│   ├── proposals.json            # Propuestas por candidato/pilar
│   ├── candidate_scores.json     # Scores + análisis fiscal
│   ├── detailed_analysis.json    # Fortalezas, debilidades, riesgo
│   └── ranking.json              # Rankings ponderados (3 tipos)
└── planes/
    ├── PLN.pdf
    ├── FA.pdf
    └── ... (20 PDFs)
```

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

## Penalizaciones Fiscales

| Tipo | Descripción | Penalización |
|------|-------------|--------------|
| attacks_fiscal_rule | Propone eliminar/flexibilizar la regla fiscal | -0.10 |
| proposes_debt_increase | Propone aumentar deuda sin plan de sostenibilidad | -0.05 |
| proposes_tax_increase | Propone aumentar impuestos | -0.03 |

---

## Niveles de Riesgo Fiscal

| Nivel | Emoji | Descripción |
|-------|-------|-------------|
| ALTO | 🔴 | Alto riesgo: ataca regla fiscal o propone deuda excesiva |
| MEDIO | 🟠 | Riesgo moderado: algunas propuestas con impacto fiscal |
| BAJO | 🟢 | Bajo riesgo: fiscalmente responsable |

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
