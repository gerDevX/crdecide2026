# 🗳️ Costa Rica Decide 2026

Herramienta cívica para comparar los planes de gobierno de los candidatos presidenciales de Costa Rica (período 2026-2030).

**Sin sesgos. Sin recomendaciones. Solo datos verificables.**

---

## ¿Qué es esto?

Costa Rica Decide extrae, analiza y presenta de forma estructurada las propuestas contenidas en los planes de gobierno oficiales de los 20 partidos políticos registrados ante el TSE.

El proyecto evalúa cada propuesta en **4 dimensiones objetivas**:

| Dimensión | Pregunta |
|-----------|----------|
| **Existencia** | ¿Es una acción concreta? |
| **Cuándo** | ¿Tiene plazo definido? |
| **Cómo** | ¿Explica el mecanismo? |
| **Fondos** | ¿Indica financiamiento? |

Las propuestas se organizan en **10 pilares nacionales** para facilitar la comparación temática.

### Sistema de Penalizaciones v6 (Neutral + Estricto)

Además de las dimensiones estructurales, se evalúan **penalizaciones objetivas**:

#### Penalizaciones Fiscales (Basadas en Ley Vigente)

| Indicador | Descripción | Penalización |
|-----------|-------------|--------------|
| ⚠️ Ataca regla fiscal | Propone flexibilizar o eliminar la regla fiscal | -2 |
| 💰 Más deuda | Propone aumentar deuda sin plan de sostenibilidad | -1 |

#### Penalizaciones por Omisión (Basadas en Urgencias de CR)

| Indicador | Descripción | Penalización |
|-----------|-------------|--------------|
| 🚨 Ignora seguridad | No menciona seguridad operativa | -1 |
| 🏥 Ignora CCSS | No menciona crisis de la CCSS | -1 |
| 💼 Ignora empleo | No menciona empleo/desempleo | -0.5 |
| 🔫 Ignora crimen organizado | No menciona narcotráfico | -0.5 |
| 📋 Falta pilar prioritario | Sin propuesta en P1, P3, P4 o P7 | -0.5 c/u |

> **Nota**: Se eliminó la penalización por "proponer más impuestos" porque representaba un sesgo ideológico.

---

## Estructura del Proyecto

```
crdecide2026/
├── analysis/           # Módulo de análisis
│   ├── planes/        # 20 PDFs de planes de gobierno
│   └── data/          # JSONs generados del análisis
│       ├── candidates.json
│       ├── pillars.json
│       ├── proposals.json
│       ├── candidate_scores.json
│       ├── detailed_analysis.json
│       └── ranking.json
│
├── site/              # Sitio web (Astro + Tailwind + TS)
│   ├── src/
│   └── dist/          # Build de producción
│
└── docs/              # Documentación del proyecto
    ├── CONTEXT.md     # Contexto general
    ├── PROMPTS.md     # Prompts de generación
    ├── DATA_SCHEMA.md # Esquema de datos
    └── VISUAL_MODES.md # Modos visuales
```

---

## Los 10 Pilares Nacionales

| ID | Pilar | Peso |
|----|-------|------|
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

### Pilares Prioritarios (60%)
P3 (Seguridad), P4 (Salud), P1 (Fiscal), P7 (Reforma Estado)

### Pilares Críticos (81%)
P3, P4, P1, P7, P2 (Empleo), P5 (Educación)

---

## Sitio Web

El sitio está construido con **Astro** (100% estático) y ofrece:

- 📊 **Dashboard de pilares**: Vista comparativa de los 10 temas nacionales
- 👥 **Perfiles de candidatos**: Matriz visual de cobertura por pilar
- ⚖️ **Comparador**: Compara hasta 4 candidatos lado a lado
- 🏆 **Rankings**: Ranking general, prioritario y de pilares críticos
- 📄 **Evidencia**: Cada propuesta enlaza al PDF y página exacta
- 🔴 **Riesgo Fiscal**: Indicadores de responsabilidad fiscal por candidato

### 3 Modos Visuales

El sitio adapta la experiencia según la preferencia del usuario:

| Modo | Emoji | Target | Características |
|------|-------|--------|-----------------|
| Express | 🚀 | Visual rápido | Cards full-screen, swipe, colores vibrantes |
| Dashboard | 📊 | Detalle analítico | Grid de cards, tabs, estilo neutro |
| Lectura | 📖 | Lectura calmada | Tipografía grande, una columna, sin animaciones |

---

## Desarrollo

### Requisitos

- Node.js 18+
- npm

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/usuario/crdecide2026.git
cd crdecide2026

# Instalar dependencias del sitio
cd site
npm install
```

### Comandos

```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview
```

---

## Stack Técnico

| Categoría | Tecnología |
|-----------|------------|
| Framework | Astro 4.x |
| Styling | Tailwind CSS 3.x |
| Lenguaje | TypeScript 5.x |
| Datos | JSON estático |
| Deploy | Estático (cualquier CDN) |

---

## Filosofía

### Lo que hacemos

- ✅ Extraer información textual de documentos públicos
- ✅ Estructurar propuestas en dimensiones objetivas
- ✅ Evaluar responsabilidad fiscal con criterios transparentes
- ✅ Facilitar la comparación entre candidatos
- ✅ Enlazar cada dato a su fuente original

### Lo que NO hacemos

- ❌ Recomendar candidatos
- ❌ Evaluar ideologías
- ❌ Predecir resultados
- ❌ Hacer juicios de viabilidad política

---

## Documentación

- [Contexto del Proyecto](docs/CONTEXT.md) - Visión general y arquitectura
- [Prompts de Generación](docs/PROMPTS.md) - Prompts originales del análisis
- [Esquema de Datos](docs/DATA_SCHEMA.md) - Estructura de los JSONs
- [Modos Visuales](docs/VISUAL_MODES.md) - Los 3 modos de experiencia
- [Arquitectura del Sitio](site/ARCHITECTURE.md) - Diseño UX y componentes

---

## Datos

Los datos provienen exclusivamente de los **planes de gobierno oficiales** presentados al Tribunal Supremo de Elecciones (TSE). Los PDFs originales están disponibles en `analysis/planes/` y en el sitio web.

**Candidatos analizados**: 20  
**Propuestas extraídas**: 3,400+  
**Pilares nacionales**: 10  
**Versión del análisis**: v6 (neutral + estricto)

---

## Licencia

Este proyecto es de código abierto. Los datos de análisis son públicos y verificables.

---

## Contacto

Si encuentras errores o tienes sugerencias, abre un issue en el repositorio.

---

*Costa Rica Decide 2026 · Enero 2026*
