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
- **Accesibilidad**: UX adaptativa según rango de edad del usuario

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
│   │   ├── pillars.json      # 9 pilares nacionales
│   │   ├── proposals.json    # ~3,400+ propuestas extraídas
│   │   ├── candidate_scores.json  # Puntajes por candidato
│   │   └── ranking.json      # Rankings ordenados
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
    └── CONTEXT.md            # Este archivo
```

---

## Modelo de Datos

### 9 Pilares Nacionales

| ID | Nombre | Peso |
|----|--------|------|
| P1 | Sostenibilidad fiscal y crecimiento económico | 15% |
| P2 | Empleo y competitividad | 15% |
| P3 | Seguridad ciudadana y justicia | 15% |
| P4 | Salud pública y seguridad social (CCSS) | 15% |
| P5 | Educación y talento humano | 15% |
| P6 | Ambiente y desarrollo sostenible | 5% |
| P7 | Reforma del Estado y lucha contra la corrupción | 10% |
| P8 | Política social focalizada | 8% |
| P9 | Política exterior y comercio internacional | 2% |

**Pilares críticos**: P1, P2, P3, P4, P5, P7 (suman 85%)

### 4 Dimensiones de Evaluación (D1-D4)

Cada propuesta se evalúa con 4 preguntas binarias (0/1):

| Dimensión | Pregunta | Ejemplo válido |
|-----------|----------|----------------|
| D1. Existencia | ¿Es una acción concreta? | "Crearemos programa de becas" |
| D2. Cuándo | ¿Tiene plazo definido? | "En los primeros 100 días" |
| D3. Cómo | ¿Explica el mecanismo? | "Mediante reforma a la Ley X" |
| D4. Fondos | ¿Indica financiamiento? | "Con reasignación del presupuesto" |

**Puntaje máximo por propuesta**: 4 puntos

### Dimensión de Control (D5) - Compatibilidad Normativa

Verifica conflictos explícitos con:
- Constitución Política de Costa Rica
- Regla fiscal vigente
- Destino legal de fondos

**D5 = 1**: Sin conflicto documentable
**D5 = 0**: Conflicto explícito (aplica penalización de -1 al pilar)

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
| `/pilares` | Grid de 9 pilares |
| `/pilares/[id]` | Detalle de pilar con ranking |
| `/candidatos` | Grid de 20 candidatos |
| `/candidatos/[id]` | Perfil con matriz de pilares |
| `/comparar` | Comparador de 2-4 candidatos |
| `/ranking` | Rankings completos |
| `/metodologia` | Explicación del análisis |
| `/acerca` | Propósito y transparencia |

### Componentes Principales

```
src/components/
├── ui/
│   ├── ModeSelector.astro    # Modal de selección de modo visual
│   ├── ScoreBar.astro        # Barra visual de puntaje
│   ├── DimensionBadges.astro # Badges E/C/H/F
│   └── EvidenceLink.astro    # Link a PDF + página
├── modes/
│   ├── express/
│   │   ├── ExpressCard.astro     # Card full-screen de candidato
│   │   └── ExpressSwiper.astro   # Contenedor con swipe
│   ├── dashboard/
│   │   └── (usa componentes base)
│   └── reading/
│       └── ReadingRanking.astro  # Vista de ranking con paginación
├── pillars/
│   ├── PillarCard.astro      # Card de pilar individual
│   └── PillarGrid.astro      # Grid de 9 pilares
├── candidates/
│   ├── CandidateCard.astro   # Card de candidato
│   └── CandidateMatrix.astro # Matriz 3x3 de pilares
├── ranking/
│   ├── RankingTable.astro    # Tabla completa de ranking
│   └── QuickRanking.astro    # Top 10 rápido
└── layout/
    ├── Header.astro          # Navegación + selector de modo
    └── Footer.astro          # Pie de página
```

### 3 Modos Visuales

El sitio ofrece 3 experiencias visuales completamente distintas:

| Modo | Emoji | Estilo | Target |
|------|-------|--------|--------|
| **Express** | 🚀 | Cards full-screen, swipe, gradientes vibrantes | Usuarios que quieren info rápida |
| **Dashboard** | 📊 | Grid de cards, tabs, estilo analítico | Vista completa con detalles |
| **Lectura** | 📖 | Tipografía serif, 20px, una columna | Usuarios que prefieren leer con calma |

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
   Procesamiento (prompt 1)
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

| Archivo | Tamaño aprox. | Contenido |
|---------|---------------|-----------|
| `candidates.json` | 5 KB | 20 candidatos con metadata |
| `pillars.json` | 1 KB | 9 pilares con pesos |
| `proposals.json` | 5 MB | ~3,400 propuestas con evidencia |
| `candidate_scores.json` | 140 KB | Puntajes por pilar y overall |
| `ranking.json` | 4 KB | Rankings ordenados |

---

## Tipos TypeScript

Los tipos principales están en `site/src/lib/types.ts`:

```typescript
type AgeGroup = '18-35' | '36-49' | '50+';
type PillarId = 'P1' | 'P2' | 'P3' | 'P4' | 'P5' | 'P6' | 'P7' | 'P8' | 'P9';
type ConflictType = 'constitutional' | 'fiscal' | 'none';

interface Candidate { ... }
interface Pillar { ... }
interface Proposal { ... }
interface CandidateScore { ... }
interface Ranking { ... }
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

### Al modificar el sitio

1. Respetar la filosofía de neutralidad y verificabilidad
2. Mantener la UX adaptativa por edad
3. Seguir el estilo "Civic Data Dashboard":
   - Cards limpias
   - Barras horizontales (no gráficos de torta)
   - Colores suaves (grises, azul cívico, verde neutro)
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
| v2 | Enero 2026 | Estructura actual con 20 candidatos |

---

## Referencias

- Arquitectura detallada: `site/ARCHITECTURE.md`
- Metodología pública: `/metodologia` en el sitio
- Tipos TypeScript: `site/src/lib/types.ts`
- Datos de ejemplo: `site/src/lib/data.ts`
