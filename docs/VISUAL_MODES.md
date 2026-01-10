# 3 Modos Visuales - Costa Rica Decide 2026

## Resumen

El sitio ofrece **3 experiencias visuales radicalmente distintas** que el usuario puede elegir según su preferencia. El sistema migra automáticamente desde el antiguo selector de rango de edad.

---

## Modo Express 🚀

**Target**: Usuarios que quieren información rápida, visual, sin fricción.
**Inspiración**: TikTok, Instagram Stories, Tinder (swipe)

### Características

| Aspecto | Especificación |
|---------|----------------|
| **Layout** | Cards full-screen, una a la vez |
| **Navegación** | Swipe horizontal (candidatos), vertical (pilares) |
| **Colores** | Gradientes bold, colores vibrantes por pilar |
| **Tipografía** | Sans-serif bold, títulos grandes |
| **Animaciones** | Transiciones suaves, micro-interacciones |
| **Contenido** | Mínimo texto, máximo visual |
| **Riesgo Fiscal** | Badge compacto con emoji y color |

### Paleta de Colores

```css
--express-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--express-card: rgba(255, 255, 255, 0.95);
--express-accent: #ff6b6b;
--express-success: #51cf66;
--express-text: #2d3436;
```

### Componentes Específicos

#### ExpressCard (Candidato)
```
┌─────────────────────────────────┐
│                                 │
│         🗳️ FA                  │
│    Frente Amplio                │
│         🟢 Riesgo BAJO          │
│                                 │
│    ████████████░░ 0.98         │
│    #1 de 20 candidatos          │
│                                 │
│  ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ P1  │ │ P2  │ │ P3  │       │
│  │ 4/4 │ │ 3/4 │ │ 4/4 │       │
│  │ ✓✓✓✓│ │ ✓✓✓○│ │ ✓✓✓✓│       │
│  └─────┘ └─────┘ └─────┘       │
│                                 │
│  ← Desliza para comparar →     │
│                                 │
│  [Ver propuestas]  [Comparar]  │
│                                 │
│      ● ○ ○ ○ ○ ○ ○ ○ ○ ○       │
└─────────────────────────────────┘
```

### Interacciones

- **Swipe left/right**: Cambiar candidato
- **Swipe up**: Ver detalles del candidato actual
- **Tap en pilar**: Expandir información
- **Double tap**: Agregar a comparación
- **Long press**: Ver propuesta destacada

### Animaciones

```css
/* Transición entre cards */
.express-card-enter {
  transform: translateX(100%);
  opacity: 0;
}
.express-card-enter-active {
  transform: translateX(0);
  opacity: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Bounce en scores */
.express-score {
  animation: bounce-in 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

---

## Modo Dashboard 📊

**Target**: Usuarios que quieren overview + capacidad de profundizar.
**Inspiración**: Notion, Linear, dashboards de analytics

### Características

| Aspecto | Especificación |
|---------|----------------|
| **Layout** | Grid responsivo, cards colapsables |
| **Navegación** | Bottom nav + tabs |
| **Colores** | Neutros con acentos de color por pilar |
| **Tipografía** | System UI, jerarquía clara |
| **Animaciones** | Sutiles, solo donde aportan |
| **Contenido** | Resumen visible, detalle expandible |
| **Riesgo Fiscal** | Badge con etiqueta y descripción en hover |

### Paleta de Colores

```css
--dashboard-bg: #f8fafc;
--dashboard-card: #ffffff;
--dashboard-border: #e2e8f0;
--dashboard-text: #1e293b;
--dashboard-muted: #64748b;
--dashboard-accent: #3b82f6;
```

### Componentes Específicos

#### DashboardHome
```
┌─────────────────────────────────┐
│  Costa Rica Decide 2026    [≡] │
├─────────────────────────────────┤
│                                 │
│  📊 Resumen                     │
│  ┌─────────┬─────────┬────────┐│
│  │20       │10       │3,400+  ││
│  │Candidat.│Pilares  │Propuest││
│  └─────────┴─────────┴────────┘│
│                                 │
│  🔴 Alerta Fiscal               │
│  X candidatos atacan regla fisc.│
│                                 │
│  🏆 Top 5 Ranking               │
│  ┌─────────────────────────────┐│
│  │ 1  FA  🟢  ████████░░  0.98 ││
│  │ 2  PSD 🟢  ███████░░░  0.91 ││
│  │ 3  PNR 🟠  ██████░░░░  0.86 ││
│  │ 4  PPSO🔴  ██████░░░░  0.83 ││
│  │ 5  PNG 🟢  ██████░░░░  0.82 ││
│  └─────────────────────────────┘│
│  [Ver ranking completo →]       │
│                                 │
│  📋 Pilares                     │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ P1 │ │ P2 │ │ P3 │ │ P4 │   │
│  │15% │ │12% │ │18% │ │15% │   │
│  └────┘ └────┘ └────┘ └────┘   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ P5 │ │ P6 │ │ P7 │ │ P8 │   │
│  └────┘ └────┘ └────┘ └────┘   │
│  ┌────┐ ┌────┐                 │
│  │ P9 │ │P10 │                 │
│  └────┘ └────┘                 │
│                                 │
├─────────────────────────────────┤
│ [🏠] [📊Pilares] [⚖️Comparar] [ℹ️]│
└─────────────────────────────────┘
```

#### DashboardCandidate
```
┌─────────────────────────────────┐
│  ← FA - Frente Amplio           │
├─────────────────────────────────┤
│                                 │
│  [Resumen] [Pilares] [Propuestas]│
│  ─────────────────────────────  │
│                                 │
│  Puntaje: 0.98  │  Rank: #1     │
│  Riesgo: 🟢 BAJO                │
│                                 │
│  Matriz de Pilares              │
│  ┌─────┬─────┬─────┐           │
│  │P1 4/4│P2 3/4│P3 4/4│          │
│  ├─────┼─────┼─────┤           │
│  │P4 4/4│P5 4/4│P6 3/4│          │
│  ├─────┼─────┼─────┤           │
│  │P7 4/4│P8 3/4│P9 3/4│          │
│  └─────┴─────┴─────┘           │
│  ┌─────┐                       │
│  │P10 3/4                       │
│  └─────┘                       │
│                                 │
│  Fortalezas                     │
│  ✓ Plan fiscal detallado       │
│  ✓ Seguridad con plazos        │
│                                 │
│  Debilidades                    │
│  △ No menciona ambiente        │
│                                 │
│  [📄 Ver plan de gobierno PDF]  │
│                                 │
└─────────────────────────────────┘
```

### Interacciones

- **Tap en card**: Expandir/colapsar
- **Tab navigation**: Cambiar sección
- **Pull-to-refresh**: Actualizar vista
- **Swipe en lista**: Acciones rápidas
- **Bottom sheet**: Detalles de propuesta

---

## Modo Lectura 📖

**Target**: Usuarios que prefieren leer con calma, alto contraste, sin distracciones.
**Inspiración**: Medium, Kindle, periódicos impresos

### Características

| Aspecto | Especificación |
|---------|----------------|
| **Layout** | Una columna, vertical, sin scroll horizontal |
| **Navegación** | Menú hamburguesa, paginación clara |
| **Colores** | Alto contraste, modo claro/oscuro |
| **Tipografía** | Serif para cuerpo, 20px mínimo |
| **Animaciones** | Ninguna o mínimas |
| **Contenido** | Todo visible, sin colapsar |
| **Riesgo Fiscal** | Texto completo con explicación |

### Paleta de Colores

```css
/* Modo claro */
--reading-bg: #fffef5;
--reading-card: #ffffff;
--reading-text: #1a1a1a;
--reading-accent: #0066cc;
--reading-border: #d4d4d4;

/* Modo oscuro */
--reading-dark-bg: #1a1a1a;
--reading-dark-card: #2d2d2d;
--reading-dark-text: #e5e5e5;
```

### Tipografía

```css
--reading-font-body: 'Georgia', 'Times New Roman', serif;
--reading-font-heading: 'Helvetica Neue', Arial, sans-serif;
--reading-size-body: 20px;
--reading-size-h1: 32px;
--reading-size-h2: 26px;
--reading-line-height: 1.8;
```

### Componentes Específicos

#### ReadingHome
```
┌─────────────────────────────────┐
│  ☰                              │
│                                 │
│  Costa Rica                     │
│  Decide 2026                    │
│  ═══════════════════════════    │
│                                 │
│  Compare los planes de gobierno │
│  de los 20 candidatos           │
│  presidenciales.                │
│                                 │
│  ───────────────────────────    │
│                                 │
│  Ranking General                │
│                                 │
│  1. Frente Amplio               │
│     Puntaje: 0.98 de 1.0        │
│     Riesgo fiscal: BAJO 🟢     │
│     Ver propuestas →            │
│                                 │
│  ───────────────────────────    │
│                                 │
│  2. Partido Social Demócrata    │
│     Puntaje: 0.91 de 1.0        │
│     Riesgo fiscal: MEDIO 🟠    │
│     Ver propuestas →            │
│                                 │
│  ───────────────────────────    │
│                                 │
│  [Página 1 de 4]   [Siguiente →]│
│                                 │
└─────────────────────────────────┘
```

### Interacciones

- **Tap en enlace**: Navegación clara
- **Botones grandes**: Mínimo 48x48px
- **Sin gestos complejos**: Solo tap y scroll
- **Breadcrumbs**: Siempre saber dónde estás
- **PDF inline**: Ver sin salir del sitio

---

## Selector de Modo

### Modal Inicial (Rediseñado)

```
┌─────────────────────────────────┐
│                                 │
│     🗳️ Costa Rica Decide       │
│                                 │
│     ¿Cómo prefieres explorar?   │
│                                 │
│  ┌─────────────────────────────┐│
│  │  🚀 Express                 ││
│  │  Rápido y visual            ││
│  │  ┌─────────────────────┐   ││
│  │  │   Preview animado   │   ││
│  │  └─────────────────────┘   ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │  📊 Dashboard               ││
│  │  Completo con detalles      ││
│  │  ┌─────────────────────┐   ││
│  │  │   Preview estático  │   ││
│  │  └─────────────────────┘   ││
│  └─────────────────────────────┘│
│                                 │
│  ┌─────────────────────────────┐│
│  │  📖 Lectura                 ││
│  │  Claro y sin distracciones  ││
│  │  ┌─────────────────────┐   ││
│  │  │   Preview texto     │   ││
│  │  └─────────────────────┘   ││
│  └─────────────────────────────┘│
│                                 │
│  Puedes cambiar en cualquier    │
│  momento desde el menú          │
│                                 │
└─────────────────────────────────┘
```

### Header con Selector de Modo

El Header incluye un dropdown que permite cambiar el modo visual en cualquier momento:

```
┌─────────────────────────────────────────────────┐
│  [Logo]  Pilares  Ranking  Candidatos │ 📊 ▼  │
│                                        ├──────┤
│                                        │🚀 18-35│
│                                        │📊 36-49│
│                                        │📖 50+ ✓│
│                                        └──────┘
└─────────────────────────────────────────────────┘
```

---

## Implementación Técnica

### Estructura de Archivos

```
src/
├── components/
│   ├── modes/
│   │   ├── express/
│   │   │   ├── ExpressCard.astro
│   │   │   └── ExpressSwiper.astro
│   │   │
│   │   ├── dashboard/
│   │   │   └── (usa componentes base)
│   │   │
│   │   └── reading/
│   │       └── ReadingRanking.astro
│   │
│   └── ui/
│       ├── ModeSelector.astro
│       ├── AgeGateModal.astro
│       ├── FiscalRiskBadge.astro
│       ├── ScoreBar.astro
│       └── EvidenceLink.astro
│
├── lib/
│   ├── mode.ts           # Gestión de modo
│   ├── types.ts          # Tipos (incluye FiscalRiskLevel)
│   └── data.ts           # Funciones de datos
│
└── styles/
    └── global.css
```

### Gestión de Modo (mode.ts)

```typescript
export type VisualMode = 'express' | 'dashboard' | 'reading';

const STORAGE_KEY = 'costarica-decide-mode';

export const MODE_INFO: Record<VisualMode, {
  name: string;
  emoji: string;
  description: string;
  tagline: string;
}> = {
  express: {
    name: 'Express',
    emoji: '🚀',
    description: 'Rápido y visual',
    tagline: 'Desliza para explorar',
  },
  dashboard: {
    name: 'Dashboard',
    emoji: '📊',
    description: 'Completo con detalles',
    tagline: 'Todo en un vistazo',
  },
  reading: {
    name: 'Lectura',
    emoji: '📖',
    description: 'Claro y sin distracciones',
    tagline: 'Lee con calma',
  },
};

export function getMode(): VisualMode | null;
export function setMode(mode: VisualMode): void;
export function hasSelectedMode(): boolean;
export function getModeClasses(mode: VisualMode): object;
```

### CSS Variables por Modo

```css
/* Base - se sobrescribe por modo */
:root {
  --bg-primary: var(--mode-bg);
  --text-primary: var(--mode-text);
  --card-bg: var(--mode-card);
  --accent: var(--mode-accent);
  --font-body: var(--mode-font);
  --font-size: var(--mode-size);
}

[data-mode="express"] {
  --mode-bg: linear-gradient(135deg, #667eea, #764ba2);
  --mode-text: #2d3436;
  --mode-card: rgba(255,255,255,0.95);
  --mode-accent: #ff6b6b;
  --mode-font: 'SF Pro Display', system-ui;
  --mode-size: 16px;
}

[data-mode="dashboard"] {
  --mode-bg: #f8fafc;
  --mode-text: #1e293b;
  --mode-card: #ffffff;
  --mode-accent: #3b82f6;
  --mode-font: system-ui;
  --mode-size: 16px;
}

[data-mode="reading"] {
  --mode-bg: #fffef5;
  --mode-text: #1a1a1a;
  --mode-card: #ffffff;
  --mode-accent: #0066cc;
  --mode-font: Georgia, serif;
  --mode-size: 20px;
}
```

### Migración desde Age Group

El sistema migra automáticamente las preferencias del antiguo selector de edad:

```typescript
// Mapeo de edad a modo
const modeMap: Record<string, VisualMode> = {
  '18-35': 'express',
  '36-49': 'dashboard',
  '50+': 'reading',
};
```

---

## PWA Configuration

### manifest.json

```json
{
  "name": "Costa Rica Decide 2026",
  "short_name": "CR Decide",
  "description": "Compara los planes de gobierno",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker (básico)

```javascript
// sw.js
const CACHE_NAME = 'crdecide-v1';
const ASSETS = [
  '/',
  '/pilares',
  '/candidatos',
  '/ranking',
  '/styles/global.css'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
```

---

## Riesgo Fiscal por Modo

El componente `FiscalRiskBadge.astro` se adapta a cada modo:

| Modo | Visualización |
|------|---------------|
| Express | Badge compacto: `🟢` |
| Dashboard | Badge con texto: `🟢 BAJO` + tooltip |
| Lectura | Texto completo: `Riesgo fiscal: BAJO 🟢` |

---

## Estado de Implementación

1. ✅ Documentar los 3 modos (este archivo)
2. ✅ Configurar PWA (manifest + service worker)
3. ✅ Crear estructura de componentes por modo
4. ✅ Implementar Modo Express (swipe cards)
5. ✅ Refinar Modo Dashboard
6. ✅ Crear Modo Lectura
7. ✅ Selector de modo con previews
8. ✅ Integrar indicadores de riesgo fiscal
