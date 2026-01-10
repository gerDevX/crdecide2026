# Costa Rica Decide 2026 - Contexto del Proyecto

## Resumen Ejecutivo

Costa Rica Decide es una herramienta cívica que analiza y compara los planes de gobierno de los candidatos presidenciales de Costa Rica para el período 2026-2030. El proyecto consta de dos partes principales:

1. **Módulo de Análisis** (`analysis/`): Procesamiento automatizado de PDFs y generación de datos estructurados
2. **Sitio Web** (`site/`): Portal estático construido con Astro para visualizar y comparar los datos

---

## Filosofía del Proyecto

### Principios Fundamentales

- **Neutralidad total**: No se emiten juicios ideológicos ni recomendaciones de voto
- **Verificabilidad**: Todo dato debe tener evidencia textual (PDF + página + snippet)
- **Transparencia**: Código abierto, metodología documentada, datos accesibles
- **Responsabilidad fiscal**: Se evalúa el impacto fiscal de las propuestas con criterios objetivos

### Lo que NO hace el proyecto

- ❌ No evalúa viabilidad política
- ❌ No juzga calidad ideológica
- ❌ No predice resultados
- ❌ No recomienda candidatos
- ❌ No infiere información no explícita en los documentos

---

## Estructura del Proyecto

```
crdecide2026/
├── analysis/                  # Módulo de análisis de datos
│   ├── planes/               # PDFs oficiales de planes de gobierno (20)
│   ├── data/                 # JSONs generados del análisis
│   │   ├── candidates.json   # 20 candidatos
│   │   ├── pillars.json      # 10 pilares nacionales
│   │   ├── proposals.json    # ~3,400+ propuestas extraídas
│   │   ├── candidate_scores.json  # Puntajes + análisis fiscal
│   │   ├── detailed_analysis.json # Fortalezas, debilidades, riesgo
│   │   └── ranking.json      # Rankings ponderados
│   └── process_plans.py      # Script de procesamiento
│
├── site/                      # Sitio web estático (Astro)
│   ├── src/
│   │   ├── pages/            # Rutas del sitio
│   │   ├── components/       # Componentes Astro
│   │   ├── lib/              # Utilidades y tipos TS
│   │   ├── layouts/          # Layout base
│   │   └── styles/           # CSS global
│   ├── public/               # Assets estáticos
│   ├── dist/                 # Build de producción
│   └── ARCHITECTURE.md       # Documentación de arquitectura
│
└── docs/                      # Documentación del proyecto
    ├── CONTEXT.md            # Este archivo
    ├── PROMPTS.md            # Prompts de generación
    ├── DATA_SCHEMA.md        # Esquema de datos
    └── VISUAL_MODES.md       # Modos visuales
```

---

## Modelo de Datos

### 10 Pilares Nacionales

| ID | Nombre | Peso |
|----|--------|------|
| P1 | Sostenibilidad fiscal y crecimiento económico | 15% |
| P2 | Empleo y competitividad | 12% |
| P3 | Seguridad ciudadana y justicia | 18% |
| P4 | Salud pública y seguridad social (CCSS) | 15% |
| P5 | Educación y talento humano | 12% |
| P6 | Ambiente y desarrollo sostenible | 4% |
| P7 | Reforma del Estado y lucha contra la corrupción | 12% |
| P8 | Política social focalizada | 5% |
| P9 | Política exterior y comercio internacional | 2% |
| P10 | Infraestructura y APPs | 5% |

**Pilares prioritarios** (60%): P3, P4, P1, P7  
**Pilares críticos** (81%): P3, P4, P1, P7, P2, P5

### 4 Dimensiones de Evaluación (D1-D4)

Cada propuesta se evalúa con 4 preguntas binarias (0/1):

| Dimensión | Pregunta | Ejemplo válido |
|-----------|----------|----------------|
| D1. Existencia | ¿Es una acción concreta? | "Crearemos programa de becas" |
| D2. Cuándo | ¿Tiene plazo definido? | "En los primeros 100 días" |
| D3. Cómo | ¿Explica el mecanismo? | "Mediante reforma a la Ley X" |
| D4. Fondos | ¿Indica financiamiento? | "Con reasignación del presupuesto" |

**Puntaje máximo por propuesta**: 4 puntos

### Análisis Fiscal

Se evalúan indicadores de responsabilidad fiscal:

| Indicador | Descripción | Penalización |
|-----------|-------------|--------------|
| attacks_fiscal_rule | Ataca o flexibiliza la regla fiscal | -0.10 |
| proposes_debt_increase | Propone aumentar deuda | -0.05 |
| proposes_tax_increase | Propone nuevos impuestos | -0.03 |
| shows_fiscal_responsibility | Muestra compromiso fiscal | Ninguna (positivo) |

### Niveles de Riesgo Fiscal

| Nivel | Emoji | Descripción |
|-------|-------|-------------|
| ALTO | 🔴 | Propuestas con alto impacto fiscal negativo |
| MEDIO | 🟠 | Propuestas con impacto moderado |
| BAJO | 🟢 | Propuestas fiscalmente responsables |

---

## Arquitectura del Sitio Web

### Stack Técnico

- **Framework**: Astro 4.x (output estático)
- **Styling**: Tailwind CSS 3.x
- **Lenguaje**: TypeScript 5.x
- **Fuentes**: System UI con fallbacks

### Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Home + Dashboard + Quick Ranking |
| `/pilares` | Grid de 10 pilares |
| `/pilares/[id]` | Detalle de pilar con ranking |
| `/candidatos` | Grid de 20 candidatos |
| `/candidatos/[id]` | Perfil con matriz de pilares + análisis fiscal |
| `/comparar` | Comparador de 2-4 candidatos |
| `/ranking` | Rankings completos (general, prioritario, crítico) |
| `/metodologia` | Explicación del análisis |
| `/acerca` | Propósito y transparencia |

### Componentes Principales

```
src/components/
├── ui/
│   ├── ModeSelector.astro      # Selector de modo visual
│   ├── AgeGateModal.astro      # Modal inicial de selección
│   ├── ScoreBar.astro          # Barra visual de puntaje
│   ├── DimensionBadges.astro   # Badges E/C/H/F
│   ├── EvidenceLink.astro      # Link a PDF + página
│   └── FiscalRiskBadge.astro   # Badge de riesgo fiscal
├── modes/
│   ├── express/
│   │   ├── ExpressCard.astro   # Card full-screen de candidato
│   │   └── ExpressSwiper.astro # Contenedor con swipe
│   ├── dashboard/
│   │   └── (usa componentes base)
│   └── reading/
│       └── ReadingRanking.astro # Vista de ranking con paginación
├── pillars/
│   ├── PillarCard.astro        # Card de pilar individual
│   └── PillarGrid.astro        # Grid de 10 pilares
├── candidates/
│   ├── CandidateCard.astro     # Card de candidato
│   └── CandidateMatrix.astro   # Matriz de pilares
├── ranking/
│   ├── RankingTable.astro      # Tabla completa de ranking
│   └── QuickRanking.astro      # Top 10 rápido
└── layout/
    ├── Header.astro            # Navegación + selector de modo
    └── Footer.astro            # Pie de página
```

### 3 Modos Visuales

| Modo | Emoji | Estilo | Target |
|------|-------|--------|--------|
| **Express** | 🚀 | Cards full-screen, swipe, gradientes vibrantes | Visual rápido |
| **Dashboard** | 📊 | Grid de cards, tabs, estilo analítico | Vista completa |
| **Lectura** | 📖 | Tipografía serif, 20px, una columna | Lectura calmada |

**Almacenamiento**: `localStorage.setItem('costarica-decide-mode', value)`

### PWA (Progressive Web App)

El sitio es instalable como app:
- **manifest.json**: Configuración de la app
- **sw.js**: Service Worker para cache offline
- **offline.html**: Página de fallback sin conexión

---

## Flujo de Datos

```
PDFs (analysis/planes/)
        ↓
   Procesamiento (prompt)
        ↓
JSONs (analysis/data/)
        ↓
   Importación (src/lib/data.ts)
        ↓
   Componentes Astro (build time)
        ↓
   HTML estático (dist/)
```

### Archivos JSON Principales

| Archivo | Contenido |
|---------|-----------|
| `candidates.json` | 20 candidatos con metadata |
| `pillars.json` | 10 pilares con pesos |
| `proposals.json` | ~3,400 propuestas con evidencia |
| `candidate_scores.json` | Puntajes + análisis fiscal por candidato |
| `detailed_analysis.json` | Fortalezas, debilidades, riesgo fiscal |
| `ranking.json` | Rankings ponderados (3 tipos) |

---

## Tipos TypeScript

Los tipos principales están en `site/src/lib/types.ts`:

```typescript
type AgeGroup = '18-35' | '36-49' | '50+';
type VisualMode = 'express' | 'dashboard' | 'reading';
type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9' | 'P10';
type FiscalRiskLevel = 'ALTO' | 'MEDIO' | 'BAJO';

interface Candidate { ... }
interface Pillar { ... }
interface Proposal { ... }
interface CandidateScore { ... }
interface DetailedAnalysis { ... }
interface Ranking { ... }
interface FiscalAnalysis { ... }
interface FiscalFlags { ... }
```

Ver `site/src/lib/types.ts` para definiciones completas.

---

## Comandos de Desarrollo

```bash
# Desde site/
npm install        # Instalar dependencias
npm run dev        # Servidor de desarrollo
npm run build      # Generar build de producción
npm run preview    # Preview del build
```

---

## Consideraciones para Futuras Intervenciones

### Al modificar datos

1. Los JSONs en `analysis/data/` deben mantener la estructura definida
2. Cualquier cambio en tipos debe reflejarse en `site/src/lib/types.ts`
3. Las propuestas deben incluir evidencia verificable (pdf_id, page, snippet)
4. El análisis fiscal debe tener evidencia textual del plan

### Al modificar el sitio

1. Respetar la filosofía de neutralidad y verificabilidad
2. Mantener los 3 modos visuales
3. Seguir el estilo "Civic Data Dashboard":
   - Cards limpias
   - Barras horizontales (no gráficos de torta)
   - Colores suaves (grises, azul cívico, verde neutro)
   - Indicadores de riesgo fiscal visibles
   - Performance extrema (Astro estático)

### Al agregar nuevos candidatos

1. Agregar PDF a `analysis/planes/`
2. Re-ejecutar análisis
3. Verificar que el nuevo candidato aparezca en todos los JSONs
4. Rebuild del sitio

---

## Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| v1 | 2025 | Versión inicial |
| v2 | Enero 2026 | Estructura con 20 candidatos |
| v3 | Enero 2026 | Scoring estructural sin penalizaciones |
| v4 | Enero 2026 | Análisis fiscal completo + 10 pilares |

---

## Referencias

- Arquitectura detallada: `site/ARCHITECTURE.md`
- Modos visuales: `docs/VISUAL_MODES.md`
- Metodología pública: `/metodologia` en el sitio
- Tipos TypeScript: `site/src/lib/types.ts`
- Datos de ejemplo: `site/src/lib/data.ts`
