# Esquema de Datos - Costa Rica Decide 2026

Referencia rápida de la estructura de datos JSON del proyecto.

---

## candidates.json

Array de candidatos presidenciales.

```typescript
interface Candidate {
  candidate_id: string;     // Slug único (ej: "pln", "fa")
  candidate_name: string;   // Nombre del candidato
  party_name: string;       // Nombre del partido
  pdf_id: string;           // ID del PDF (uppercase: "PLN", "FA")
  pdf_title: string;        // Título del plan de gobierno
  pdf_url: string;          // Ruta al PDF
}
```

**Ejemplo:**
```json
{
  "candidate_id": "pln",
  "candidate_name": "Marvin Taylor Dormond",
  "party_name": "Partido Liberación Nacional",
  "pdf_id": "PLN",
  "pdf_title": "Plan de Gobierno PLN 2026-2030",
  "pdf_url": "local://analysis/planes/PLN.pdf"
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

```typescript
interface Proposal {
  proposal_id: string;              // ID único
  candidate_id: string;             // Ref a candidate
  pillar_id: PillarId;              // Ref a pillar
  proposal_title: string;           // Título corto
  proposal_text: string;            // Texto resumen
  dimensions: Dimensions;           // Evaluación D1-D4
  extracted_fields: ExtractedFields;// Textos extraídos
  compatibility: Compatibility;     // Evaluación D5
  evidence: Evidence;               // Referencia al PDF
  multi_pillar_source_proposal_id: string | null;
}

interface Dimensions {
  existence: 0 | 1;  // D1: ¿Es concreta?
  when: 0 | 1;       // D2: ¿Tiene plazo?
  how: 0 | 1;        // D3: ¿Explica cómo?
  funding: 0 | 1;    // D4: ¿Indica fondos?
}

interface ExtractedFields {
  when_text: string;    // Texto del plazo o "no_especificado"
  how_text: string;     // Texto del mecanismo o "no_especificado"
  funding_text: string; // Texto del financiamiento o "no_especificado"
}

interface Compatibility {
  normative_fiscal: 0 | 1;     // D5: ¿Compatible?
  conflict_type: ConflictType; // Tipo de conflicto
  reference: string;           // Referencia legal
  note: string;                // Nota técnica
}

type ConflictType = 'constitutional' | 'fiscal' | 'none';

interface Evidence {
  pdf_id: string;   // ID del PDF
  page: number;     // Número de página (1-indexed)
  snippet: string;  // Fragmento de texto (≤240 chars)
}
```

**Ejemplo:**
```json
{
  "proposal_id": "FA_p23_i0_P1",
  "candidate_id": "fa",
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
  "compatibility": {
    "normative_fiscal": 1,
    "conflict_type": "none",
    "reference": "",
    "note": ""
  },
  "evidence": {
    "pdf_id": "FA",
    "page": 23,
    "snippet": "...modificar la estructura del impuesto sobre la renta para hacerla más progresiva..."
  },
  "multi_pillar_source_proposal_id": null
}
```

---

## candidate_scores.json

Array de puntajes calculados por candidato.

```typescript
interface CandidateScore {
  candidate_id: string;
  pillar_scores: PillarScore[];
  overall: Overall;
}

interface PillarScore {
  pillar_id: PillarId;
  raw_score: number;           // 0-4 (suma de dimensiones)
  effective_score: number;     // raw_score - penalizaciones
  normalized: number;          // 0.0-1.0 (effective/4)
  weighted: number;            // normalized * peso_pilar
  dimension_counts: Dimensions;// Conteo de dimensiones
  penalties: Penalty[];        // Penalizaciones aplicadas
  evidence_refs: EvidenceRef[];// Referencias a propuestas
}

interface Penalty {
  type: 'compatibility';
  value: number;    // -1
  reason: string;   // Explicación
}

interface EvidenceRef {
  proposal_id: string;
  page: number;
}

interface Overall {
  raw_sum: number;                      // Suma de raw_scores (0-36)
  effective_sum: number;                // Suma de effective_scores
  weighted_sum: number;                 // Suma ponderada (0.0-1.0)
  coverage_critical_weighted_sum: number;// Solo pilares críticos
  notes: string;                        // Observaciones
}
```

**Ejemplo:**
```json
{
  "candidate_id": "fa",
  "pillar_scores": [
    {
      "pillar_id": "P1",
      "raw_score": 4,
      "effective_score": 4,
      "normalized": 1.0,
      "weighted": 0.15,
      "dimension_counts": {
        "existence": 1,
        "when": 1,
        "how": 1,
        "funding": 1
      },
      "penalties": [],
      "evidence_refs": [
        { "proposal_id": "FA_p23_i0_P1", "page": 23 }
      ]
    }
  ],
  "overall": {
    "raw_sum": 34,
    "effective_sum": 34,
    "weighted_sum": 0.9825,
    "coverage_critical_weighted_sum": 0.85,
    "notes": ""
  }
}
```

---

## ranking.json

Rankings ordenados de candidatos.

```typescript
interface Ranking {
  method_version: string;                    // "v2"
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
  "method_version": "v2",
  "weights": {
    "P1": 0.15, "P2": 0.15, "P3": 0.15, "P4": 0.15, "P5": 0.15,
    "P6": 0.05, "P7": 0.10, "P8": 0.08, "P9": 0.02
  },
  "ranking_overall_weighted": [
    { "rank": 1, "candidate_id": "fa", "weighted_sum": 0.9825 },
    { "rank": 2, "candidate_id": "psd", "weighted_sum": 0.91 }
  ],
  "ranking_critical_weighted": [
    { "rank": 1, "candidate_id": "fa", "coverage_critical_weighted_sum": 0.85 },
    { "rank": 2, "candidate_id": "psd", "coverage_critical_weighted_sum": 0.775 }
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
```

---

## Ubicación de Archivos

```
analysis/
├── data/
│   ├── candidates.json      # ~5 KB
│   ├── pillars.json         # ~1 KB
│   ├── proposals.json       # ~5 MB (3,400+ propuestas)
│   ├── candidate_scores.json# ~140 KB
│   └── ranking.json         # ~4 KB
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
