# 3 Modos Visuales - Costa Rica Decide 2026

## Resumen

En lugar de ajustes graduales por edad, el sitio ofrece **3 experiencias visuales radicalmente distintas** que el usuario puede elegir según su preferencia.

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

#### ExpressPillar (Pilar)
```
┌─────────────────────────────────┐
│                                 │
│    💰 P1: Sostenibilidad Fiscal │
│    Peso: 15%                    │
│                                 │
│    Top 3                        │
│    ┌─────────────────────────┐ │
│    │ 🥇 FA      ████████ 4/4 │ │
│    │ 🥈 PSD     ███████░ 3/4 │ │
│    │ 🥉 PNR     ███████░ 3/4 │ │
│    └─────────────────────────┘ │
│                                 │
│    Promedio: 2.8/4              │
│                                 │
│    ↑ Desliza para ver más ↑    │
│                                 │
└─────────────────────────────────┘
```

#### ExpressCompare (Comparador)
```
┌─────────────────────────────────┐
│  FA  vs  PLN                    │
├─────────────────────────────────┤
│                                 │
│  ┌──────────┐  ┌──────────┐    │
│  │   0.98   │  │   0.68   │    │
│  │  ██████  │  │  ████░░  │    │
│  │   #1     │  │   #15    │    │
│  └──────────┘  └──────────┘    │
│                                 │
│  P1 Fiscal                      │
│  4/4  ████████  vs  ██░░  2/4  │
│                                 │
│  P2 Empleo                      │
│  3/4  ██████░░  vs  ███░  3/4  │
│                                 │
│  [+ Agregar candidato]          │
│                                 │
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
│  │20       │9        │3,400+  ││
│  │Candidat.│Pilares  │Propuest││
│  └─────────┴─────────┴────────┘│
│                                 │
│  🏆 Top 5 Ranking               │
│  ┌─────────────────────────────┐│
│  │ 1  FA     ████████░░  0.98 ││
│  │ 2  PSD    ███████░░░  0.91 ││
│  │ 3  PNR    ██████░░░░  0.86 ││
│  │ 4  PPSO   ██████░░░░  0.83 ││
│  │ 5  PNG    ██████░░░░  0.82 ││
│  └─────────────────────────────┘│
│  [Ver ranking completo →]       │
│                                 │
│  📋 Pilares                     │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ P1 │ │ P2 │ │ P3 │ │ P4 │   │
│  │15% │ │15% │ │15% │ │15% │   │
│  └────┘ └────┘ └────┘ └────┘   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│  │ P5 │ │ P6 │ │ P7 │ │ P8 │   │
│  └────┘ └────┘ └────┘ └────┘   │
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
│                                 │
│  Matriz de Pilares              │
│  ┌─────┬─────┬─────┐           │
│  │P1 4/4│P2 3/4│P3 4/4│          │
│  ├─────┼─────┼─────┤           │
│  │P4 4/4│P5 4/4│P6 3/4│          │
│  ├─────┼─────┼─────┤           │
│  │P7 4/4│P8 3/4│P9 3/4│          │
│  └─────┴─────┴─────┘           │
│                                 │
│  Dimensiones Fuertes            │
│  ✓ Existencia (9/9 pilares)    │
│  ✓ Mecanismo (8/9 pilares)     │
│  △ Financiamiento (6/9 pilares)│
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
│     Ver propuestas →            │
│                                 │
│  ───────────────────────────    │
│                                 │
│  2. Partido Social Demócrata    │
│     Puntaje: 0.91 de 1.0        │
│     Ver propuestas →            │
│                                 │
│  ───────────────────────────    │
│                                 │
│  [Página 1 de 4]   [Siguiente →]│
│                                 │
└─────────────────────────────────┘
```

#### ReadingCandidate
```
┌─────────────────────────────────┐
│  ← Volver                       │
│                                 │
│  Frente Amplio                  │
│  ═══════════════════════════    │
│                                 │
│  Candidato: Por determinar      │
│  Posición en ranking: #1 de 20  │
│  Puntaje general: 0.98          │
│                                 │
│  ───────────────────────────    │
│                                 │
│  Sostenibilidad Fiscal (P1)     │
│  Puntaje: 4 de 4                │
│                                 │
│  ✓ Propuesta concreta           │
│  ✓ Plazo definido               │
│  ✓ Mecanismo explicado          │
│  ✓ Financiamiento indicado      │
│                                 │
│  Propuesta destacada:           │
│                                 │
│  "Reforma tributaria progresiva │
│   mediante modificación de la   │
│   Ley del Impuesto sobre la     │
│   Renta para hacerla más        │
│   equitativa..."                │
│                                 │
│  📄 Ver en documento original   │
│     (página 23)                 │
│                                 │
│  ───────────────────────────    │
│                                 │
│  [← Anterior pilar]             │
│  [Siguiente pilar →]            │
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

---

## Implementación Técnica

### Estructura de Archivos

```
src/
├── components/
│   ├── modes/
│   │   ├── express/
│   │   │   ├── ExpressCard.astro
│   │   │   ├── ExpressNav.astro
│   │   │   ├── ExpressCompare.astro
│   │   │   └── ExpressSwiper.astro
│   │   │
│   │   ├── dashboard/
│   │   │   ├── DashboardCard.astro
│   │   │   ├── DashboardNav.astro
│   │   │   ├── DashboardTabs.astro
│   │   │   └── DashboardBottomSheet.astro
│   │   │
│   │   └── reading/
│   │       ├── ReadingArticle.astro
│   │       ├── ReadingNav.astro
│   │       ├── ReadingPagination.astro
│   │       └── ReadingMenu.astro
│   │
│   └── shared/
│       ├── ModeSelector.astro
│       ├── ScoreBar.astro
│       └── EvidenceLink.astro
│
├── layouts/
│   ├── ExpressLayout.astro
│   ├── DashboardLayout.astro
│   └── ReadingLayout.astro
│
├── styles/
│   ├── modes/
│   │   ├── express.css
│   │   ├── dashboard.css
│   │   └── reading.css
│   └── global.css
│
└── lib/
    ├── mode.ts          # Gestión de modo
    └── swipe.ts         # Utilidades de gestos
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

### JavaScript para Gestos (Express)

```typescript
// lib/swipe.ts
export function initSwipe(container: HTMLElement, options: SwipeOptions) {
  let startX = 0;
  let currentX = 0;
  
  container.addEventListener('touchstart', (e) => {
    startX = e.touches[0].clientX;
  });
  
  container.addEventListener('touchmove', (e) => {
    currentX = e.touches[0].clientX;
    const diff = currentX - startX;
    // Aplicar transform durante el drag
    container.style.transform = `translateX(${diff}px)`;
  });
  
  container.addEventListener('touchend', () => {
    const diff = currentX - startX;
    if (Math.abs(diff) > options.threshold) {
      if (diff > 0) options.onSwipeRight?.();
      else options.onSwipeLeft?.();
    }
    container.style.transform = '';
  });
}
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

## Próximos Pasos

1. ✅ Documentar los 3 modos (este archivo)
2. ⏳ Configurar PWA (manifest + service worker)
3. ⏳ Crear estructura de componentes por modo
4. ⏳ Implementar Modo Express (swipe cards)
5. ⏳ Refinar Modo Dashboard
6. ⏳ Crear Modo Lectura
7. ⏳ Actualizar selector de modo con previews
