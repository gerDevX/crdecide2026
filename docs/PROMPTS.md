# Prompts de Generación del Proyecto

Este documento contiene los prompts utilizados para generar las dos partes principales del proyecto Costa Rica Decide 2026.

---

## Prompt 1: Análisis de Planes de Gobierno (v6)

> **Objetivo**: Procesar PDFs de planes de gobierno y generar datos estructurados en JSON con análisis fiscal

```
Actúa como un analista cívico técnico, neutral y verificable.
Tu tarea es procesar un listado de planes de gobierno (PDF) de candidatos presidenciales de Costa Rica y estructurar su contenido en un modelo comparativo basado en pilares nacionales, sin emitir juicios ideológicos, sin recomendaciones de voto y sin inferir información que no esté explícitamente contenida en los documentos. La ruta de los planes esta en la carpeta analysis/planes.

====================================================================
OBJETIVO GENERAL
====================================================================

1) Extraer propuestas de los planes de gobierno y clasificarlas en los 10 pilares nacionales definidos.
2) Evaluar cada propuesta en 4 dimensiones estructurales basadas SOLO en evidencia textual.
3) Realizar análisis fiscal: detectar ataques a la regla fiscal, propuestas de deuda e impuestos.
4) Calcular puntajes por pilar y por candidato usando pesos predefinidos.
5) Aplicar penalizaciones fiscales al puntaje final.
6) Generar análisis detallado con fortalezas, debilidades y nivel de riesgo.
7) Generar JSONs base auditables para publicación pública.

====================================================================
PILARES NACIONALES (10 PILARES)
====================================================================

P1. Sostenibilidad fiscal y crecimiento económico (15%)
P2. Empleo y competitividad (12%)
P3. Seguridad ciudadana y justicia (18%)
P4. Salud pública y seguridad social (CCSS) (15%)
P5. Educación y talento humano (12%)
P6. Ambiente y desarrollo sostenible (4%)
P7. Reforma del Estado y lucha contra la corrupción (12%)
P8. Política social focalizada (5%)
P9. Política exterior y comercio internacional (2%)
P10. Infraestructura y APPs (5%)

Pilares prioritarios (60%): P3, P4, P1, P7
Pilares críticos (81%): P3, P4, P1, P7, P2, P5

====================================================================
DIMENSIONES PRINCIPALES (D1–D4)
====================================================================

Evalúa cada propuesta SOLO con base en el texto del plan.

D1. Existencia (0/1)
→ La propuesta describe una acción, política o medida concreta.

D2. Cuándo (0/1)
→ Indica plazo, fase, horizonte temporal o periodo verificable.
→ Ejemplos válidos: "primer año", "primeros 24 meses", "durante el cuatrienio 2026–2030".
→ Frases vagas como "a futuro" o "gradualmente" NO cuentan.

D3. Cómo (0/1)
→ Describe mecanismo, instrumento, pasos, reformas, implementación o medio de ejecución.

D4. Fondos (0/1)
→ Identifica fuente de financiamiento:
- reasignación presupuestaria
- impuestos
- deuda
- recortes
- cooperación internacional
- alianzas público-privadas
→ Si hay gasto y no se menciona fuente, D4 = 0.

Si falta información en cualquier dimensión, usar exactamente:
"no_especificado"

====================================================================
SISTEMA DE PENALIZACIONES v6 (NEUTRAL + ESTRICTO)
====================================================================

NOTA IMPORTANTE: El sistema v6 ELIMINA la penalización por "proponer
más impuestos" porque representaba un sesgo ideológico. Solo se
mantienen penalizaciones OBJETIVAS basadas en ley vigente.

PENALIZACIONES FISCALES (Objetivas - Basadas en Ley)
-----------------------------------------------------

1. attacks_fiscal_rule (boolean)
   ¿Propone eliminar, flexibilizar o atacar la regla fiscal vigente?
   Penalización: -2

2. proposes_debt_increase (boolean)
   ¿Propone aumentar la deuda pública sin plan de sostenibilidad?
   Penalización: -1

3. shows_fiscal_responsibility (boolean)
   ¿Demuestra compromiso explícito con la sostenibilidad fiscal?
   (No genera penalización, es indicador positivo)

PENALIZACIONES POR OMISIÓN (Basadas en Urgencias Nacionales)
-------------------------------------------------------------

Estas penalizaciones se aplican cuando un candidato IGNORA temas
urgentes para Costa Rica en su plan de gobierno:

4. ignores_security (boolean)
   ¿NO menciona seguridad operativa en medio de crisis de violencia?
   Penalización: -1

5. ignores_ccss (boolean)
   ¿NO menciona la crisis de la CCSS (listas de espera, sostenibilidad)?
   Penalización: -1

6. ignores_employment (boolean)
   ¿NO menciona empleo/desempleo con tasa superior al 10%?
   Penalización: -0.5

7. ignores_organized_crime (boolean)
   ¿NO menciona crimen organizado, narcotráfico o sicariato?
   Penalización: -0.5

8. missing_priority_pillar (por cada pilar)
   ¿NO tiene propuesta concreta (score > 1) en pilar prioritario?
   Pilares prioritarios: P1, P3, P4, P7
   Penalización: -0.5 por cada pilar faltante

NIVEL DE RIESGO FISCAL:
- ALTO: attacks_fiscal_rule = true O total_penalty >= 3
- MEDIO: total_penalty >= 1.5 AND < 3
- BAJO: total_penalty < 1.5

====================================================================
COBERTURA DE URGENCIAS NACIONALES
====================================================================

Verificar si el plan menciona explícitamente:

- seguridad_operativa: Policía, equipamiento, presupuesto de seguridad
- salud_ccss: Crisis de la CCSS, listas de espera, sostenibilidad
- inversion_extranjera: Atracción de inversión, zonas francas
- empleo: Desempleo, creación de empleos, informalidad
- educacion: Calidad educativa, deserción, infraestructura
- infraestructura_APP: Carreteras, puentes, alianzas público-privadas
- crimen_organizado: Narcotráfico, crimen organizado, seguridad

Para cada tema:
- covered: true/false
- mentions: Array de snippets textuales (≤240 chars cada uno)

====================================================================
REGLAS DE NEUTRALIDAD Y EVIDENCIA
====================================================================

- No uses lenguaje valorativo (ej. "bueno", "malo", "realista", "populista").
- No hagas inferencias económicas ni políticas.
- No completes información ausente.
- Todo dato debe tener:
- pdf_id
- página (1-indexed)
- snippet textual (≤ 240 caracteres)
- Si un pilar NO aparece en el documento, crea una propuesta placeholder con todas las dimensiones en 0.

====================================================================
PESOS POR PILAR
====================================================================

P1: 0.15
P2: 0.12
P3: 0.18
P4: 0.15
P5: 0.12
P6: 0.04
P7: 0.12
P8: 0.05
P9: 0.02
P10: 0.05

====================================================================
SALIDAS REQUERIDAS (6 ARCHIVOS JSON)
====================================================================

A) candidates.json
[
{
"candidate_id": "string_slug",
"candidate_name": "string",
"party_name": "string",
"pdf_id": "string",
"pdf_title": "string",
"pdf_url": "string"
}
]

B) pillars.json
[
{ "pillar_id": "P1", "pillar_name": "...", "weight": 0.15 }
]

C) proposals.json
[
{
"proposal_id": "unique_string",
"candidate_id": "string_slug",
    "pillar_id": "P1..P10",
"proposal_title": "string_short",
"proposal_text": "resumen fiel sin agregar información",
"dimensions": {
"existence": 0,
"when": 0,
"how": 0,
"funding": 0
},
"extracted_fields": {
"when_text": "string | no_especificado",
"how_text": "string | no_especificado",
"funding_text": "string | no_especificado"
},
"evidence": {
"pdf_id": "string",
"page": 1,
"snippet": "string <= 240"
    }
}
]

D) candidate_scores.json
[
{
"candidate_id": "string_slug",
"pillar_scores": [
{
"pillar_id": "P1",
"raw_score": 0-4,
"effective_score": 0-4,
"normalized": 0.0-1.0,
"weighted": 0.0-1.0,
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
      "total_penalty": 0.0,
      "evidence": []
    },
"overall": {
      "raw_sum": 0-40,
      "effective_sum": 0-40,
"weighted_sum": 0.0-1.0,
      "priority_weighted_sum": 0.0-1.0,
      "critical_weighted_sum": 0.0-1.0,
      "fiscal_penalty_applied": 0.0,
"notes": "observaciones neutrales sin juicio"
}
}
]

E) detailed_analysis.json
[
  {
    "candidate_id": "string_slug",
    "pdf_id": "string",
    "total_pages": 45,
    "fiscal_responsibility": {
      "attacks_fiscal_rule": false,
      "proposes_debt_increase": false,
      "proposes_tax_increase": false,
      "shows_fiscal_responsibility": true
    },
    "fiscal_evidence": [],
    "urgency_coverage": {
      "seguridad_operativa": { "covered": true, "mentions": [] },
      "salud_ccss": { "covered": true, "mentions": [] },
      "inversion_extranjera": { "covered": false, "mentions": [] },
      "empleo": { "covered": true, "mentions": [] },
      "educacion": { "covered": true, "mentions": [] },
      "infraestructura_APP": { "covered": false, "mentions": [] },
      "crimen_organizado": { "covered": true, "mentions": [] }
    },
    "strengths": ["fortaleza 1", "fortaleza 2"],
    "weaknesses": ["debilidad 1", "debilidad 2"],
    "risk_level": "BAJO"
  }
]

F) ranking.json
{
  "method_version": "v4",
  "weights": { "P1": 0.15, "P2": 0.12, ... },
  "priority_pillars": ["P3", "P4", "P1", "P7"],
  "critical_pillars": ["P3", "P4", "P1", "P7", "P2", "P5"],
  "penalties_applied": {
    "attacks_fiscal_rule": -0.10,
    "proposes_debt_increase": -0.05,
    "proposes_tax_increase": -0.03
  },
"ranking_overall_weighted": [
    { "rank": 1, "candidate_id": "string", "weighted_sum": 0.0, "fiscal_penalty": 0.0 }
  ],
  "ranking_priority_weighted": [
    { "rank": 1, "candidate_id": "string", "priority_weighted_sum": 0.0 }
],
"ranking_critical_weighted": [
    { "rank": 1, "candidate_id": "string", "critical_weighted_sum": 0.0 }
]
}

====================================================================
SALIDA FINAL
====================================================================

Devuelve UN SOLO objeto JSON con estas claves exactas:
{
"candidates.json": [...],
"pillars.json": [...],
"proposals.json": [...],
"candidate_scores.json": [...],
  "detailed_analysis.json": [...],
"ranking.json": {...}
}

No agregues texto fuera del JSON.
No agregues explicaciones adicionales.
No uses markdown.

Y estos json deben almacenarse en la ruta analysis/data.
```

---

## Prompt 2: Diseño del Sitio Web

> **Objetivo**: Diseñar y construir un sitio web estático con Astro que consuma los datos del análisis

```
Actúa como un Arquitecto de Producto + Frontend Tech Lead especializado en portales cívicos, dashboards de datos públicos y experiencias web altamente accesibles.

Vas a diseñar un sitio web estático construido con Astro + Tailwind + TypeScript en la carpeta llamada "site" que consume un análisis ya generado en JSON y planes de gobierno en PDF, ambos almacenados localmente en el source code del proyecto.

El sitio debe priorizar:
- Experiencia visual y gráfica
- Claridad estadística
- Velocidad extrema
- Confianza pública
- Adaptación de UX según modo visual (Express, Dashboard, Lectura)
- Transparencia en el análisis fiscal

El estilo UX base debe ser: "Civic Data Dashboard"
(un híbrido entre dashboard estadístico, portal editorial y comparador ciudadano).

====================================================================
ENTRADA (YA EXISTE EN EL REPOSITORIO)
====================================================================

Los insumos ya fueron analizados previamente (Prompt 1) y están disponibles LOCALMENTE:

- PDFs de planes oficiales:
  Ruta: analysis/planes/

- Datos de análisis (JSON):
  Ruta: analysis/data/
  Archivos:
    candidates.json
    pillars.json
    proposals.json
    candidate_scores.json
    detailed_analysis.json
    ranking.json

Asume que:
- proposals.json incluye evidence.page y evidence.snippet.
- candidate_scores.json incluye fiscal_analysis con flags y penalties.
- detailed_analysis.json incluye strengths, weaknesses y risk_level.
- Los PDFs corresponden exactamente a los datos analizados.
- No existe backend ni base de datos externa.

====================================================================
OBJETIVOS DEL SITIO
====================================================================

1) La navegación principal se centra en los 10 PILARES (no en candidatos).
2) Cada pilar se presenta como una unidad visual (card/dashboard):
   - ranking por candidato
   - score visual (barras, chips, ratios)
   - acceso a detalle y evidencia
3) Cada candidato tiene:
   - matriz visual de cobertura por pilar (10 pilares)
   - acceso a propuestas con desglose estructural
   - análisis fiscal con indicador de riesgo
   - fortalezas y debilidades
4) Comparador:
   - comparar 2 a 4 candidatos
   - vista estadística por pilar
   - vista de detalle con dimensiones + evidencia
   - indicadores de riesgo fiscal lado a lado
5) Rankings:
   - ranking ponderado general (con penalizaciones fiscales)
   - ranking de pilares prioritarios (P3, P4, P1, P7)
   - ranking de pilares críticos (P3, P4, P1, P7, P2, P5)
6) 3 Modos visuales:
   - Express 🚀: Cards full-screen, swipe, visual rápido
   - Dashboard 📊: Grid de cards, tabs, estilo analítico
   - Lectura 📖: Tipografía grande, una columna, sin animaciones
7) Página informativa:
   - propósito del sitio
   - explicación coloquial del análisis
   - explicación del análisis fiscal y penalizaciones
   - aclaración de neutralidad y límites

====================================================================
FILOSOFÍA UX (OBLIGATORIA)
====================================================================

- "Los datos se entienden antes de leerse"
- "Los pilares mandan, no los candidatos"
- "Todo número debe tener respaldo visible"
- "Nada debe sentirse lento ni pesado"
- "El diseño inspira confianza, no propaganda"
- "El riesgo fiscal debe ser visible pero no alarmista"

====================================================================
ESTILO UX BASE: CIVIC DATA DASHBOARD
====================================================================

Debes diseñar el sitio siguiendo estos principios visuales:

VISUAL
- Cards limpias
- Barras horizontales (no gráficos de torta)
- Chips numéricos (ej. 3/4)
- Íconos neutros por pilar (emojis)
- Colores suaves (grises, azul cívico, verde neutro)
- Indicadores de riesgo fiscal (🟢🟠🔴)

ESTADÍSTICO
- Scores visibles siempre con contexto (máx /4)
- Rankings claros y ordenables
- Indicadores explícitos de "no especificado"
- Penalizaciones fiscales transparentes

PERFORMANCE
- HTML prerender (Astro)
- JSON livianos por vista
- Nada de loaders largos
- Animaciones mínimas y sutiles (excepto modo Express)

====================================================================
3 MODOS VISUALES
====================================================================

El sitio ofrece 3 experiencias completamente distintas:

Express 🚀 (Visual / Rápido)
- Cards full-screen, una a la vez
- Swipe para navegar
- Gradientes vibrantes
- Mínimo texto, máximo visual
- Riesgo fiscal como emoji badge

Dashboard 📊 (Visual + Explicativo)
- Grid responsivo de cards
- Tabs para secciones
- Colores neutros con acentos
- Resumen + expandible
- Riesgo fiscal con etiqueta

Lectura 📖 (Lectura / Confianza)
- Una columna vertical
- Tipografía serif, 20px mínimo
- Sin animaciones
- Todo visible, sin colapsar
- Riesgo fiscal con texto completo

====================================================================
RESTRICCIONES Y FILOSOFÍA TÉCNICA
====================================================================

- Sitio 100% estático (Astro).
- Datos consumidos directamente desde analysis/data/.
- PDFs servidos desde analysis/planes/.
- Accesibilidad AA mínima.
- Neutralidad total.
- Todo score debe enlazar a evidencia (PDF + página).

====================================================================
REQUERIMIENTOS DE SALIDA
====================================================================

Debes entregar, en el orden indicado:

A) Estructura final del sitio (IA / UX)
   - Mapa exacto de rutas (URLs)
   - Componentes visuales por página
   - Qué se muestra por defecto según modo

B) Modelo de datos completo
   - Data Contract con tipos TypeScript exactos
   - Índices recomendados para navegación rápida
   - Tipos para análisis fiscal y riesgo

C) UI exacta del Comparador (nivel quirúrgico)
   - Layout preciso
   - Qué es sticky, qué colapsa
   - Vista resumen vs detalle
   - Indicadores de riesgo fiscal
   - Componentes específicos

D) 3 Modos visuales
   - Diferencias concretas de:
     densidad, tipografía, animación, CTA
   - Implementación técnica:
     mode en localStorage
     selector manual en header

E) Stack y plan de implementación (Astro)
   - Astro + Tailwind + TypeScript + JSON
   - Estructura de carpetas
   - Estrategia de build y performance

F) Página /metodologia (copy listo para pegar)
   - Español coloquial
   - Explicando:
     propósito
     origen de datos
     pilares
     dimensiones
     análisis fiscal y penalizaciones
     rankings
     límites y transparencia

====================================================================
FORMATO DE RESPUESTA
====================================================================

- Responde en Markdown.
- Divide la respuesta en secciones A–F.
- Usa tablas solo si aportan claridad.
- Incluye snippets TypeScript solo para modelos de datos.
- No incluyas código completo.
- No uses enlaces externos.
- NO solicites los PDFs ni los JSON (ya existen).
```

---

## Notas de Implementación

### Diferencias entre Prompts y Realidad

1. **10 pilares**: La implementación actual usa 10 pilares (se agregó P10: Infraestructura).

2. **Sistema de penalizaciones v6**:
   - **Eliminado**: `proposes_tax_increase` (era sesgo ideológico)
   - **Mantenido**: `attacks_fiscal_rule` (-2), `proposes_debt_increase` (-1)
   - **Agregado**: Penalizaciones por omisión de urgencias nacionales
   - **Agregado**: `OmissionAnalysis` en candidate_scores.json
   - Script de recálculo: `analysis/recalculate_scores_v6.py`

3. **3 tipos de ranking**: 
   - ranking_overall_weighted (general)
   - ranking_priority_weighted (pilares prioritarios: P3, P4, P1, P7)
   - ranking_critical_weighted (pilares críticos: P3, P4, P1, P7, P2, P5)

4. **3 Modos visuales**: Reemplazan el antiguo selector de edad:
   - Express 🚀 (antes 18-35)
   - Dashboard 📊 (antes 36-49)
   - Lectura 📖 (antes 50+)

5. **Componentes para penalizaciones**:
   - `FiscalRiskBadge.astro`: Muestra nivel de riesgo
   - Funciones en `data.ts`: `getAllPenalties()`, `getOmissionAnalysis()`

### Historial de Versiones del Sistema

| Versión | Cambios |
|---------|---------|
| v1-v3 | Versiones iniciales |
| v4 | Análisis fiscal con 3 penalizaciones |
| v5 | Penalizaciones fiscales más estrictas |
| v6 | Sistema neutral (sin sesgo) + penalizaciones por omisión |

### Extensiones Futuras

- Agregar búsqueda de propuestas
- Implementar filtros por tipo de penalización
- Agregar gráficos de comparación temporal (si hay actualizaciones)
- Implementar dark mode para modo Lectura
