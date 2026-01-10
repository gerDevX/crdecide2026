# Prompts de Generación del Proyecto

Este documento contiene los prompts originales utilizados para generar las dos partes principales del proyecto Costa Rica Decide 2026.

---

## Prompt 1: Análisis de Planes de Gobierno

> **Objetivo**: Procesar PDFs de planes de gobierno y generar datos estructurados en JSON

```
Actúa como un analista cívico técnico, neutral y verificable.
Tu tarea es procesar un listado de planes de gobierno (PDF) de candidatos presidenciales de Costa Rica y estructurar su contenido en un modelo comparativo basado en pilares nacionales, sin emitir juicios ideológicos, sin recomendaciones de voto y sin inferir información que no esté explícitamente contenida en los documentos. La ruta de los planes esta en la carpeta analysis/planes.

====================================================================
OBJETIVO GENERAL
====================================================================

1) Extraer propuestas de los planes de gobierno y clasificarlas en los 9 pilares nacionales definidos.
2) Evaluar cada propuesta en 4 dimensiones estructurales basadas SOLO en evidencia textual.
3) Aplicar una 5ª dimensión de control: compatibilidad normativa y fiscal, basada en el marco constitucional y fiscal vigente de Costa Rica.
4) Calcular puntajes por pilar y por candidato usando pesos predefinidos.
5) Generar JSONs base auditables para publicación pública.

====================================================================
PILARES NACIONALES (FIJOS)
====================================================================

P1. Sostenibilidad fiscal y crecimiento económico
P2. Empleo y competitividad
P3. Seguridad ciudadana y justicia
P4. Salud pública y seguridad social (CCSS)
P5. Educación y talento humano
P6. Ambiente y desarrollo sostenible
P7. Reforma del Estado y lucha contra la corrupción
P8. Política social focalizada
P9. Política exterior y comercio internacional

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
DIMENSIÓN DE CONTROL (D5) – COMPATIBILIDAD NORMATIVA Y FISCAL
====================================================================

D5 NO es ideológica, NO evalúa viabilidad política y NO opina.
Solo detecta conflictos explícitos documentables.

Pregunta objetiva:
¿La propuesta, tal como está redactada, presenta incompatibilidades explícitas con el marco constitucional o fiscal vigente de Costa Rica?

Marco de referencia permitido:
- Constitución Política de Costa Rica (vigente)
- Art. 50 (bienestar y ambiente)
- Art. 73 (CCSS)
- Art. 176–184 (Hacienda Pública)
- Regla fiscal vigente
- Situación documentada de déficit fiscal

Evaluación:
- D5 = 1 → NO hay conflicto explícito documentable.
- D5 = 0 → SOLO si existe al menos uno de estos casos:
a) Contradicción directa con la Constitución SIN mencionar reforma.
b) Promesa de gasto SIN fuente en contexto de déficit reconocido.
c) Uso de fondos con destino constitucional distinto.
- Si el plan menciona "reforma constitucional" o "cambio legal", D5 = 1.

Toda evaluación D5 = 0 DEBE incluir:
- referencia constitucional o fiscal
- tipo de conflicto: constitutional | fiscal | presupuestary
- nota técnica neutral (máx 240 caracteres)

D5 NO suma puntos.
D5 puede aplicar una penalización de -1 al puntaje del pilar correspondiente.

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
- Si una propuesta aplica a varios pilares, duplica el registro por pilar usando el mismo proposal_id base.
- Si un pilar NO aparece en el documento, crea una propuesta placeholder con todas las dimensiones en 0.

====================================================================
PESOS POR PILAR
====================================================================

P1: 0.15
P2: 0.15
P3: 0.15
P4: 0.15
P5: 0.15
P7: 0.10
P8: 0.08
P6: 0.05
P9: 0.02

====================================================================
SALIDAS REQUERIDAS (SOLO JSON VÁLIDO)
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
"pillar_id": "P1..P9",
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
"compatibility": {
"normative_fiscal": 0,
"conflict_type": "constitutional | fiscal | none",
"reference": "Art. X Constitución / Regla Fiscal",
"note": "descripción técnica neutral"
},
"evidence": {
"pdf_id": "string",
"page": 1,
"snippet": "string <= 240"
},
"multi_pillar_source_proposal_id": "string"
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
"penalties": [
{
"type": "compatibility",
"value": -1,
"reason": "conflicto fiscal explícito"
}
]
}
],
"overall": {
"raw_sum": 0-36,
"weighted_sum": 0.0-1.0,
"coverage_critical_weighted_sum": 0.0,
"notes": "observaciones neutrales sin juicio"
}
}
]

E) ranking.json
{
"method_version": "v1",
"weights": { "P1":0.15, "P2":0.15, "...":0.02 },
"ranking_overall_weighted": [
{ "rank": 1, "candidate_id": "string", "weighted_sum": 0.0 }
],
"ranking_critical_weighted": [
{ "rank": 1, "candidate_id": "string", "coverage_critical_weighted_sum": 0.0 }
]
}

====================================================================
ENTRADA
====================================================================

Recibirás una lista de PDFs con este formato:
[
{
"pdf_id": "PLN",
"candidate_name": "Nombre",
"party_name": "Partido",
"pdf_title": "Plan de Gobierno 2026–2030",
"pdf_url": "https://..."
}
]

====================================================================
SALIDA FINAL
====================================================================

Devuelve UN SOLO objeto JSON con estas claves exactas:
{
"candidates.json": [...],
"pillars.json": [...],
"proposals.json": [...],
"candidate_scores.json": [...],
"ranking.json": {...}
}

No agregues texto fuera del JSON.
No agregues explicaciones adicionales.
No uses markdown.

Y estos json deben alamacenarse en la ruta analysis/data.
```

---

## Prompt 2: Diseño del Sitio Web

> **Objetivo**: Diseñar y construir un sitio web estático con Astro que consuma los datos del análisis

```
Actúa como un Arquitecto de Producto + Frontend Tech Lead especializado en portales cívicos, dashboards de datos públicos y experiencias web altamente accesibles.

Vas a diseñar un sitio web estático construido con Astro + Tailwind + TypeScript  en la carpeta llamada "site" que consume un análisis ya generados en JSON y planes de gobierno en PDF, ambos almacenados localmente en el source code del proyecto.

El sitio debe priorizar:
- Experiencia visual y gráfica
- Claridad estadística
- Velocidad extrema
- Confianza pública
- Adaptación real de UX según rango de edad

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
    ranking.json

Asume que:
- proposals.json incluye evidence.page y evidence.snippet.
- Los PDFs corresponden exactamente a los datos analizados.
- No existe backend ni base de datos externa.

====================================================================
OBJETIVOS DEL SITIO
====================================================================

1) La navegación principal se centra en los 9 PILARES (no en candidatos).
2) Cada pilar se presenta como una unidad visual (card/dashboard):
   - ranking por candidato
   - score visual (barras, chips, ratios)
   - acceso a detalle y evidencia
3) Cada candidato tiene:
   - matriz visual de cobertura por pilar (9 pilares)
   - acceso a propuestas con desglose estructural
4) Comparador:
   - comparar 2 a 4 candidatos
   - vista estadística por pilar
   - vista de detalle con dimensiones + evidencia
5) Rankings:
   - ranking ponderado general
   - ranking ponderado de pilares críticos (P1,P2,P3,P4,P5,P7)
6) UX adaptativa:
   - preguntar rango de edad al inicio
   - adaptar visualización, densidad y detalle
7) Página informativa:
   - propósito del sitio
   - explicación coloquial del análisis
   - aclaración de neutralidad y límites

====================================================================
FILOSOFÍA UX (OBLIGATORIA)
====================================================================

- "Los datos se entienden antes de leerse"
- "Los pilares mandan, no los candidatos"
- "Todo número debe tener respaldo visible"
- "Nada debe sentirse lento ni pesado"
- "El diseño inspira confianza, no propaganda"

====================================================================
ESTILO UX BASE: CIVIC DATA DASHBOARD
====================================================================

Debes diseñar el sitio siguiendo estos principios visuales:

VISUAL
- Cards limpias
- Barras horizontales (no gráficos de torta)
- Chips numéricos (ej. 3/4)
- Íconos neutros por pilar
- Colores suaves (grises, azul cívico, verde neutro)

ESTADÍSTICO
- Scores visibles siempre con contexto (máx /4)
- Rankings claros y ordenables
- Indicadores explícitos de "no especificado"

PERFORMANCE
- HTML prerender (Astro)
- JSON livianos por vista
- Nada de loaders largos
- Animaciones mínimas y sutiles

====================================================================
UX ADAPTATIVA POR RANGO DE EDAD
====================================================================

El sitio debe preguntar el rango de edad del lector al inicio
(18–35, 36–49, 50+) y guardar la preferencia.

Diferencias obligatorias:

18–35 años (Visual / Rápido)
- Vista resumen por defecto
- Cards + barras + rankings
- Poco texto
- Interacciones rápidas (tap / hover)
- CTA: "Comparar ahora", "Ver ranking"

36–49 años (Visual + Explicativo)
- Resumen + expandible
- Tabs: Resumen | Detalle | Evidencia
- Contexto corto por pilar
- CTA: "Ver detalle", "Entender diferencias"

50+ años (Lectura / Confianza)
- Tipografía +20%
- Vista vertical (una cosa a la vez)
- Muy pocas animaciones
- Botones grandes
- PDF y evidencia siempre visibles
- CTA: "Ver propuesta completa", "Abrir plan oficial"

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
   - Qué se muestra por defecto según edad

B) Modelo de datos completo
   - Data Contract con tipos TypeScript exactos
   - Índices recomendados para navegación rápida
   - Estrategia de partición de JSON
   - Estructura recomendada para analysis/data/

C) UI exacta del Comparador (nivel quirúrgico)
   - Layout preciso
   - Qué es sticky, qué colapsa
   - Vista resumen vs detalle
   - Componentes específicos:
     <AgeGateModal/>
     <PillarCard/>
     <ScoreBar/>
     <DimensionBadges/>
     <CandidateMatrix/>
     <CompareTable/>
     <EvidenceLink/>

D) UX adaptativa por edad
   - Diferencias concretas de:
     densidad, tipografía, animación, CTA
   - Implementación técnica:
     ageGroup en localStorage/cookie
     selector manual en header

E) Stack y plan de implementación (Astro)
   - Astro + Tailwind + TypeScript + JSON
   - Estructura de carpetas:
     src/pages
     src/components
     src/lib
     analysis/data
     analysis/planes
   - Estrategia de build y performance

F) Página /metodologia (copy listo para pegar)
   - Español coloquial
   - Explicando:
     propósito
     origen de datos
     pilares
     dimensiones
     compatibilidad normativa/fiscal
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

1. **candidate_scores.json**: La implementación actual incluye campos adicionales como `dimension_counts` y `evidence_refs` que no estaban en el prompt original pero mejoran la navegabilidad.

2. **Partición de JSONs**: La estrategia de partición sugerida (`partitioned/`) no se implementó porque Astro maneja bien la carga en build-time del JSON completo.

3. **Selector de edad en header**: Implementado en el Header.astro como dropdown.

### Extensiones Futuras

- Agregar búsqueda de propuestas
- Implementar partición de proposals.json si crece mucho
- Agregar más visualizaciones (timeline, etc.)
