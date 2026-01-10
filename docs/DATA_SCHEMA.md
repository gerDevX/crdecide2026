# Esquema de Datos - Costa Rica Decide 2026

Referencia rápida de la estructura de datos JSON del proyecto.

**Versión 3.0** - Scoring estructural sin penalizaciones + Coherencia contextual separada.

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
  "pdf_url": "no_especificado"
}
```

---

## pillars.json

Array de los 9 pilares nacionales.

```typescript
interface Pillar {
  pillar_id: PillarId;      // "P1" - "P9"
  pillar_name: string;      // Nombre completo
  weight: number;           // Peso (0.02 - 0.15)
}

type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9';
```

**Pesos:**
| Pilar | Peso |
|-------|------|
| P1, P2, P3, P4, P5 | 0.15 |
| P7 | 0.10 |
| P8 | 0.08 |
| P6 | 0.05 |
| P9 | 0.02 |

---

## proposals.json

Array de propuestas extraídas de los planes de gobierno.

**Regla clave:** MÁXIMO 1 propuesta por pilar por candidato (9 propuestas máximo por candidato).

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
  multi_pillar_source_proposal_id: string; // "no_especificado" o ID
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
  },
  "multi_pillar_source_proposal_id": "no_especificado"
}
```

---

## candidate_scores.json

Array de puntajes calculados por candidato.

**Nota:** NO se aplican penalizaciones en el scoring. Las evaluaciones de coherencia están en archivo separado.

```typescript
interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  overall: Overall;
}

interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;           // 0-4 (suma de D1+D2+D3+D4)
  effective_score: number;     // = raw_score (sin penalizaciones)
  normalized: number;          // 0.0-1.0 (effective/4)
  weighted: number;            // normalized * peso_pilar
  penalties: [];               // Siempre vacío en v3
}

interface Overall {
  raw_sum: number;                      // Suma de raw_scores (0-36)
  weighted_sum: number;                 // Suma ponderada (0.0-1.0)
  coverage_critical_weighted_sum: number;// Solo pilares críticos
  notes: string;                        // Observaciones técnicas neutrales
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
  "overall": {
    "raw_sum": 28,
    "weighted_sum": 0.82,
    "coverage_critical_weighted_sum": 0.72,
    "notes": "Sin propuestas identificadas: P9"
  }
}
```

---

## ranking.json

Rankings ordenados de candidatos.

```typescript
interface Ranking {
  method_version: string;                    // "v3"
  weights: Record<string, number>;           // Pesos por pilar
  ranking_overall_weighted: RankingEntry[];  // Ranking general
  ranking_critical_weighted: RankingEntry[]; // Ranking pilares críticos
}

interface RankingEntry {
  rank: number;                              // Posición (1-20)
  candidate_id: string;                      // ID del candidato
  weighted_sum?: number;                     // Para overall
  coverage_critical_weighted_sum?: number;   // Para critical
}
```

**Ejemplo:**
```json
{
  "method_version": "v3",
  "weights": {
    "P1": 0.15, "P2": 0.15, "P3": 0.15, "P4": 0.15, "P5": 0.15,
    "P6": 0.05, "P7": 0.10, "P8": 0.08, "P9": 0.02
  },
  "ranking_overall_weighted": [
    { "rank": 1, "candidate_id": "alvaro-ramos", "weighted_sum": 0.82 },
    { "rank": 2, "candidate_id": "claudia-dobles", "weighted_sum": 0.78 }
  ],
  "ranking_critical_weighted": [
    { "rank": 1, "candidate_id": "alvaro-ramos", "coverage_critical_weighted_sum": 0.72 },
    { "rank": 2, "candidate_id": "claudia-dobles", "coverage_critical_weighted_sum": 0.68 }
  ]
}
```

---

## contextual_coherence.json (NUEVO)

Array de análisis de coherencia contextual por candidato.

**Esta información NO afecta puntajes ni ranking.** Es una capa informativa adicional.

```typescript
interface ContextualCoherence {
  candidate_id: string;
  contextual_coherence: {
    constitutional_alignment: CoherenceAlignment;
    fiscal_context_alignment: CoherenceAlignment;
    national_context_notes: ContextNote[];
  };
}

interface CoherenceAlignment {
  status: 'aligned' | 'potential_conflict' | 'unclear';
  reference: string;   // Artículo o norma
  note: string;        // Nota técnica neutral (≤240 chars)
}

interface ContextNote {
  topic: string;       // Tema
  observation: string; // Observación neutral (≤240 chars)
}
```

**Ejemplo:**
```json
{
  "candidate_id": "alvaro-ramos",
  "contextual_coherence": {
    "constitutional_alignment": {
      "status": "aligned",
      "reference": "",
      "note": ""
    },
    "fiscal_context_alignment": {
      "status": "unclear",
      "reference": "Regla fiscal vigente - Déficit fiscal",
      "note": "El plan propone gastos sin especificar fuentes de financiamiento claras."
    },
    "national_context_notes": [
      {
        "topic": "Inversión extranjera",
        "observation": "No se menciona inversión extranjera directa pese a su peso en empleo nacional."
      }
    ]
  }
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

candidates.json ←──── candidate_id ────→ contextual_coherence.json
```

---

## Ubicación de Archivos

```
analysis/
├── data/
│   ├── candidates.json           # 20 candidatos
│   ├── pillars.json              # 9 pilares
│   ├── proposals.json            # 180 propuestas (9 por candidato)
│   ├── candidate_scores.json     # Scores por candidato/pilar
│   ├── ranking.json              # Rankings ponderados
│   └── contextual_coherence.json # Coherencia contextual (informativo)
└── planes/
    ├── PLN.pdf
    ├── FA.pdf
    └── ... (20 PDFs)
```

---

## Pilares Críticos

Los pilares críticos (usados para `coverage_critical_weighted_sum`) son:

```typescript
const CRITICAL_PILLARS: PillarId[] = ['P1', 'P2', 'P3', 'P4', 'P5', 'P7'];
```

Suman el **85%** del peso total.

---

## Dimensiones D1-D4

| Dimensión | Nombre | Pregunta | Ejemplos Válidos |
|-----------|--------|----------|------------------|
| D1 | Existencia | ¿Es acción concreta? | "Crear...", "Implementar...", "Reformar..." |
| D2 | Cuándo | ¿Tiene plazo verificable? | "primer año", "primeros 100 días", "2026–2030" |
| D3 | Cómo | ¿Describe mecanismo? | programa definido, reforma legal, creación de institución |
| D4 | Fondos | ¿Indica financiamiento? | presupuesto, impuestos, cooperación, APP |

**raw_score = D1 + D2 + D3 + D4** (0-4)
