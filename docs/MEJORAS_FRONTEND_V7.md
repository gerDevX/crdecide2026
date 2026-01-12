# Mejoras Frontend para v7 - Sistema de Flags Informativos y Múltiples Propuestas

## ⚠️ IMPORTANTE: Adaptación a 3 Modos Visuales

**Este documento contempla los 3 modos visuales del sitio**:
- 📊 **Dashboard Mode**: Completo con detalles
- 🚀 **Express Mode**: Rápido y visual
- 📖 **Reading Mode**: Lectura clara

**Todas las mejoras deben implementarse en los 3 modos con adaptaciones apropiadas.**

---

## 📋 Resumen Ejecutivo

El sistema de análisis v7 introduce nuevas funcionalidades que **NO están siendo mostradas en el frontend**:

1. **Flags Informativos** (NO penalizan, solo informan)
2. **Múltiples Propuestas por Pilar** (hasta 3)
3. **Bonos por Calidad y Cantidad**
4. **Violaciones Constitucionales Detectadas**

**Estado actual**: Solo Dashboard Mode tiene implementación parcial. Express y Reading Mode necesitan implementación completa.

---

## 🎯 Mejoras Prioritarias

### 1. **Sistema de Flags Informativos** ⚠️ CRÍTICO

**Estado Actual**: ❌ No implementado  
**Ubicación en Datos**: `candidate_scores[].informative_flags`

#### 1.1 Flags de Propuestas Actuales Problemáticas

**Datos disponibles**:
```json
{
  "current_proposals": {
    "violates_separation_powers": {
      "active": true,
      "severity": "high",
      "evidence": [...]
    },
    "violates_fundamental_rights": {...},
    "violates_constitutional_guarantees": {...},
    "violates_constitutional_procedures": {...}
  }
}
```

**Mejoras necesarias**:
- ✅ Crear componente `InformativeFlags.astro`
- ✅ Mostrar sección "⚠️ Información Adicional" en página de candidato
- ✅ Diseño neutral (NO alarmante, solo informativo)
- ✅ Mostrar evidencia específica por pilar
- ✅ Explicar que NO afectan el score

**Ubicaciones** (adaptado a 3 modos):
- `/candidatos/[id].astro`:
  - **Dashboard**: Sección expandible después de alertas fiscales
  - **Express**: Badge compacto en header, modal al tocar
  - **Reading**: Sección completa de texto, sin colapsar
- `/comparar.astro`:
  - **Dashboard**: Columna adicional en tabla
  - **Express**: Badge en cards de comparación
  - **Reading**: Fila adicional en tabla de texto
- `/ranking.astro`:
  - **Dashboard**: Badge informativo en tarjetas
  - **Express**: Icono en cards de ranking
  - **Reading**: Texto descriptivo en lista

---

#### 1.2 Flags de Similitudes Dictatoriales

**Datos disponibles**:
```json
{
  "dictatorial_patterns": {
    "cuba_similarity": {
      "active": true,
      "severity": "high",
      "evidence": [...]
    },
    "venezuela_similarity": {...}
  }
}
```

**Mejoras necesarias**:
- ✅ Mostrar en sección de flags informativos
- ✅ Enfoque objetivo (patrones verificables, NO ideología)
- ✅ Incluir evidencia específica
- ✅ Diseño neutral pero claro

**Texto sugerido**:
```
⚠️ Similitudes Detectadas con Modelos Históricos

Este candidato presenta propuestas que muestran similitudes objetivas con 
patrones históricamente verificables de modelos dictatoriales.

[Ver detalles] [Cerrar]
```

---

#### 1.3 Flags de Requisitos de Negociación entre Poderes

**Datos disponibles**:
```json
{
  "power_negotiation_requirements": {
    "requires_assembly_approval": {
      "active": true,
      "evidence": [...]
    },
    "requires_qualified_majority": {...},
    "requires_inter_branch_coordination": {...}
  }
}
```

**Mejoras necesarias**:
- ✅ Mostrar como información de complejidad (NO problema)
- ✅ Indicar que requiere coordinación entre poderes
- ✅ Diseño informativo (azul/cian, no rojo/amarillo)

**Texto sugerido**:
```
ℹ️ Complejidad de Implementación

Algunas propuestas requieren coordinación entre poderes del Estado:
- Aprobación de Asamblea Legislativa
- Mayoría calificada (2/3)
- Coordinación inter-branch

Esto indica mayor complejidad, pero NO es un problema.
```

---

#### 1.4 Flags de Evidencia Histórica

**Datos disponibles**:
```json
{
  "historical": {
    "anti_democratic_behavior": {
      "active": true,
      "severity": "high",
      "evidence": [...]
    },
    "human_rights_violations": {...},
    "corruption_convictions": {...}
  }
}
```

**Mejoras necesarias**:
- ✅ Mostrar evidencia histórica verificable
- ✅ Incluir fechas y fuentes
- ✅ Enlaces a verificaciones (si disponibles)
- ✅ Diseño neutral pero informativo

**Texto sugerido**:
```
📚 Evidencia Histórica Verificable

Este candidato/partido tiene evidencia histórica verificable de:
- Comportamiento anti-democrático (2020)
- [Fuente: Poder Judicial]

[Ver detalles] [Cerrar]
```

---

#### 1.5 Flags de Contradicciones Histórico-Actual

**Datos disponibles**:
```json
{
  "contradictions": {
    "historical_current_contradiction": {
      "active": true,
      "severity": "high",
      "evidence": {
        "historical": "...",
        "current": "...",
        "pattern": "..."
      }
    },
    "corruption_transparency_concern": {...}
  }
}
```

**Mejoras necesarias**:
- ✅ Mostrar patrón consistente detectado
- ✅ Explicar contradicción sin juzgar
- ✅ Diseño informativo (amarillo/naranja, no rojo)

**Texto sugerido**:
```
⚠️ Patrón Consistente Detectado

Evidencia histórica + Propuestas actuales muestran un patrón consistente:
- Histórico: [descripción]
- Actual: [descripción]
- Patrón: [descripción]

[Ver detalles] [Cerrar]
```

---

### 2. **Múltiples Propuestas por Pilar** 📋 IMPORTANTE

**Estado Actual**: ⚠️ Parcialmente implementado (muestra hasta 3, pero no explica el sistema)

**Datos disponibles**:
- `proposals.json` ahora contiene hasta 3 propuestas por pilar
- `pillar_scores[].num_proposals` indica cantidad de propuestas

**Mejoras necesarias**:

#### 2.1 Página de Candidato (`/candidatos/[id].astro`)

**Línea 312-318**: Actualmente muestra hasta 3 propuestas, pero:
- ❌ No explica que hay hasta 3 propuestas por pilar
- ❌ No muestra el bono por múltiples propuestas
- ❌ No indica cuántas propuestas tiene cada pilar
- ⚠️ Solo implementado en Dashboard Mode, falta Express y Reading

**Mejoras** (adaptado a 3 modos):

**Dashboard Mode** (línea ~312):
```astro
<!-- Mostrar cantidad de propuestas -->
<div class="proposal-count-badge">
  {pillarProposals.length} propuesta{pillarProposals.length !== 1 ? 's' : ''}
  {pillarProposals.length >= 3 && (
    <span class="bonus-badge">+1.0 bono</span>
  )}
</div>

<!-- Mostrar todas las propuestas (hasta 3) -->
{pillarProposals.map((proposal, idx) => (
  <div class="proposal-item">
    {idx === 0 && <span class="best-proposal-badge">⭐ Mejor propuesta</span>}
    ...
  </div>
))}
```

**Express Mode** (línea ~492):
```astro
<!-- Mostrar propuestas de forma compacta -->
<div class="express-proposals-list">
  {pillarProposals.slice(0, 2).map((proposal, idx) => (
    <div class="express-proposal-card">
      {idx === 0 && <span class="express-best-badge">⭐</span>}
      <h3>{proposal.proposal_title}</h3>
      <p>{proposal.proposal_text.slice(0, 100)}...</p>
      {pillarProposals.length >= 3 && (
        <span class="express-bonus-badge">+1.0</span>
      )}
    </div>
  ))}
  {pillarProposals.length > 2 && (
    <button class="express-see-more">Ver {pillarProposals.length - 2} más</button>
  )}
</div>
```

**Reading Mode** (línea ~655):
```astro
<!-- Mostrar todas las propuestas en texto completo -->
<div class="reading-proposals-section">
  <h3>Propuestas para {pillar.pillar_name}</h3>
  <p class="reading-proposal-count">
    {pillarProposals.length} propuesta{pillarProposals.length !== 1 ? 's' : ''} encontrada{pillarProposals.length !== 1 ? 's' : ''}
    {pillarProposals.length >= 3 && (
      <span class="reading-bonus-text">(Bono de +1.0 por múltiples propuestas)</span>
    )}
  </p>
  {pillarProposals.map((proposal, idx) => (
    <div class="reading-proposal-item">
      {idx === 0 && <strong>Mejor propuesta:</strong>}
      <h4>{proposal.proposal_title}</h4>
      <p>{proposal.proposal_text}</p>
    </div>
  ))}
</div>
```

---

#### 2.2 Página de Comparación (`/comparar.astro`)

**Línea 37-44**: Actualmente solo guarda la primera propuesta por pilar

**Mejoras**:
- ✅ Mostrar hasta 3 propuestas por pilar en comparación
- ✅ Indicar cantidad total de propuestas
- ✅ Mostrar bono por múltiples propuestas

---

#### 2.3 Página de Pilares (`/pilares/[id].astro`)

**Mejoras**:
- ✅ Mostrar todas las propuestas de cada candidato (hasta 3)
- ✅ Indicar cuál es la mejor propuesta
- ✅ Mostrar bonos recibidos

---

### 3. **Sistema de Bonos** 🎁 IMPORTANTE

**Estado Actual**: ❌ No mostrado en frontend

**Datos disponibles**:
```json
{
  "pillar_scores": [{
    "bonus_multiple": 1.0,  // Bono por 3+ propuestas
    "bonus_quality": 0.25, // Bono por propuesta completa
    "bonus_funding": 0.1    // Bono por propuesta con financiamiento
  }]
}
```

**Mejoras necesarias**:

#### 3.1 Mostrar Bonos en Página de Candidato

**Ubicación**: `/candidatos/[id].astro` - Sección de pilares (3 modos)

**Diseño sugerido** (adaptado por modo):

**Dashboard Mode**:
```astro
<div class="bonus-section">
  <h4>Bonos Recibidos</h4>
  {ps.bonus_multiple > 0 && (
    <div class="bonus-item">
      <span class="bonus-icon">🎯</span>
      <span>+{ps.bonus_multiple} por múltiples propuestas (3+)</span>
    </div>
  )}
  {ps.bonus_quality > 0 && (
    <div class="bonus-item">
      <span class="bonus-icon">⭐</span>
      <span>+{ps.bonus_quality} por propuesta completa</span>
    </div>
  )}
  {ps.bonus_funding > 0 && (
    <div class="bonus-item">
      <span class="bonus-icon">💰</span>
      <span>+{ps.bonus_funding} por financiamiento</span>
    </div>
  )}
</div>
```

**Express Mode**:
```astro
<div class="express-bonus-badges">
  {ps.bonus_multiple > 0 && (
    <span class="express-bonus-badge" title="Bono por múltiples propuestas">
      🎯 +{ps.bonus_multiple}
    </span>
  )}
  {ps.bonus_quality > 0 && (
    <span class="express-bonus-badge" title="Bono por calidad">
      ⭐ +{ps.bonus_quality}
    </span>
  )}
  {ps.bonus_funding > 0 && (
    <span class="express-bonus-badge" title="Bono por financiamiento">
      💰 +{ps.bonus_funding}
    </span>
  )}
</div>
```

**Reading Mode**:
```astro
<div class="reading-bonus-section">
  <h4>Bonos Recibidos en este Pilar</h4>
  {ps.bonus_multiple > 0 && (
    <p>
      <strong>Bono por múltiples propuestas:</strong> +{ps.bonus_multiple} puntos 
      (tiene {ps.num_proposals} propuestas válidas, el máximo es 3)
    </p>
  )}
  {ps.bonus_quality > 0 && (
    <p>
      <strong>Bono por calidad:</strong> +{ps.bonus_quality} puntos 
      (propuesta completa con todas las dimensiones)
    </p>
  )}
  {ps.bonus_funding > 0 && (
    <p>
      <strong>Bono por financiamiento:</strong> +{ps.bonus_funding} puntos 
      (propuesta incluye plan de financiamiento)
    </p>
  )}
</div>
```

---

#### 3.2 Mostrar Bonos en Comparación

**Ubicación**: `/comparar.astro`

**Mejoras**:
- ✅ Columna adicional "Bonos" en tabla de comparación
- ✅ Mostrar total de bonos por candidato
- ✅ Tooltip explicando sistema de bonos

---

### 4. **Violaciones Constitucionales** ⚖️ IMPORTANTE

**Estado Actual**: ⚠️ Se penalizan pero no se muestran como información

**Datos disponibles**:
```json
{
  "pillar_scores": [{
    "viability_penalty": -1.0,
    "viability_flags": {
      "violates_separation_powers": true,
      "violates_fundamental_rights": false,
      ...
    }
  }]
}
```

**Mejoras necesarias**:

#### 4.1 Mostrar Violaciones en Página de Candidato

**Ubicación**: `/candidatos/[id].astro` - Sección de pilares (3 modos)

**Diseño sugerido** (adaptado por modo):

**Dashboard Mode**:
```astro
{ps.viability_penalty < 0 && (
  <div class="viability-alert">
    <span class="alert-icon">⚖️</span>
    <div class="alert-content">
      <strong>Violación Constitucional Detectada</strong>
      <p>
        {ps.viability_flags.violates_separation_powers && "Viola separación de poderes"}
        {ps.viability_flags.violates_fundamental_rights && "Viola derechos fundamentales"}
        ...
      </p>
      <span class="penalty-amount">Penalización: {ps.viability_penalty}</span>
    </div>
  </div>
)}
```

**Express Mode**:
```astro
{ps.viability_penalty < 0 && (
  <div class="express-viability-badge">
    ⚖️ -{Math.abs(ps.viability_penalty)}
  </div>
)}
```

**Reading Mode**:
```astro
{ps.viability_penalty < 0 && (
  <div class="reading-viability-alert">
    <h4>⚠️ Violación Constitucional Detectada</h4>
    <p>
      Este pilar tiene una penalización de {ps.viability_penalty} puntos por violaciones constitucionales:
    </p>
    <ul>
      {ps.viability_flags.violates_separation_powers && (
        <li>Viola separación de poderes</li>
      )}
      {ps.viability_flags.violates_fundamental_rights && (
        <li>Viola derechos fundamentales</li>
      )}
      {ps.viability_flags.violates_constitutional_guarantees && (
        <li>Viola garantías constitucionales</li>
      )}
      {ps.viability_flags.violates_constitutional_procedures && (
        <li>Viola procedimientos constitucionales</li>
      )}
    </ul>
    <p>
      <strong>Penalización aplicada:</strong> {ps.viability_penalty} puntos
    </p>
  </div>
)}
```

---

#### 4.2 Integrar con Flags Informativos

**Mejoras**:
- ✅ Mostrar violaciones tanto como penalización (afecta score) como flag informativo (solo informa)
- ✅ Explicar diferencia entre penalización y flag informativo

---

### 5. **Actualización de Tipos TypeScript** 🔧 TÉCNICO

**Estado Actual**: ❌ Tipos no incluyen nuevos campos

**Archivo**: `/site/src/lib/types.ts`

**Mejoras necesarias**:

```typescript
// Agregar tipos para flags informativos
export interface InformativeFlags {
  current_proposals: {
    violates_separation_powers: FlagInfo;
    violates_fundamental_rights: FlagInfo;
    violates_constitutional_guarantees: FlagInfo;
    violates_constitutional_procedures: FlagInfo;
  };
  dictatorial_patterns: {
    cuba_similarity?: FlagInfo;
    venezuela_similarity?: FlagInfo;
  };
  power_negotiation_requirements: {
    requires_assembly_approval?: FlagInfo;
    requires_qualified_majority?: FlagInfo;
    requires_inter_branch_coordination?: FlagInfo;
  };
  historical: {
    anti_democratic_behavior?: FlagInfo;
    human_rights_violations?: FlagInfo;
    corruption_convictions?: FlagInfo;
  };
  contradictions: {
    historical_current_contradiction?: ContradictionFlag;
    corruption_transparency_concern?: ContradictionFlag;
  };
}

export interface FlagInfo {
  active: boolean;
  severity: 'high' | 'medium' | 'low';
  evidence: Array<{
    pillar_id?: string;
    evidence: string;
    detected_by: string;
  }>;
}

export interface ContradictionFlag extends FlagInfo {
  evidence: {
    historical: string | null;
    current: string | null;
    pattern: string | null;
  };
  description: string;
}

// Actualizar CandidateScore
export interface CandidateScore {
  // ... campos existentes
  informative_flags?: InformativeFlags;
}

// Actualizar PillarScore
export interface PillarScore {
  // ... campos existentes
  bonus_multiple?: number;
  bonus_quality?: number;
  bonus_funding?: number;
  viability_penalty?: number;
  viability_flags?: {
    violates_separation_powers: boolean;
    violates_fundamental_rights: boolean;
    violates_constitutional_guarantees: boolean;
    violates_constitutional_procedures: boolean;
  };
  num_proposals?: number;
}
```

---

### 6. **Actualización de Funciones de Datos** 🔧 TÉCNICO

**Archivo**: `/site/src/lib/data.ts`

**Mejoras necesarias**:

```typescript
// Agregar función para obtener flags informativos
export function getInformativeFlags(candidateId: string): InformativeFlags | undefined {
  const score = scoresByCandidate[candidateId];
  return score?.informative_flags;
}

// Agregar función para verificar si tiene flags activos
export function hasActiveInformativeFlags(candidateId: string): boolean {
  const flags = getInformativeFlags(candidateId);
  if (!flags) return false;
  
  // Verificar cada categoría
  const hasCurrentProposals = Object.values(flags.current_proposals || {})
    .some(f => f.active);
  const hasDictatorial = Object.values(flags.dictatorial_patterns || {})
    .some(f => f?.active);
  const hasNegotiation = Object.values(flags.power_negotiation_requirements || {})
    .some(f => f?.active);
  const hasHistorical = Object.values(flags.historical || {})
    .some(f => f?.active);
  const hasContradictions = Object.values(flags.contradictions || {})
    .some(f => f?.active);
  
  return hasCurrentProposals || hasDictatorial || hasNegotiation || 
         hasHistorical || hasContradictions;
}

// Agregar función para obtener bonos totales
export function getTotalBonuses(candidateId: string): number {
  const score = scoresByCandidate[candidateId];
  if (!score) return 0;
  
  return score.pillar_scores.reduce((sum, ps) => {
    return sum + (ps.bonus_multiple || 0) + 
                 (ps.bonus_quality || 0) + 
                 (ps.bonus_funding || 0);
  }, 0);
}
```

---

## 📐 Diseño y UX

### ⚠️ IMPORTANTE: Adaptación a los 3 Modos Visuales

**El sitio tiene 3 modos visuales distintos que DEBEN ser contemplados**:

1. **Dashboard Mode** (📊): Completo con detalles, grid responsivo
2. **Express Mode** (🚀): Rápido y visual, cards full-screen, mínimo texto
3. **Reading Mode** (📖): Lectura, una columna, tipografía grande, serif

**Cada mejora debe implementarse en los 3 modos con adaptaciones apropiadas.**

---

### Principios de Diseño para Flags Informativos

1. **Neutralidad Visual**:
   - NO usar colores alarmantes (rojo intenso)
   - Usar tonos informativos (azul, cian, amarillo suave)
   - Iconos informativos (ℹ️, ⚠️, 📚) no alarmantes (🚨, ⛔)

2. **Claridad de Mensaje**:
   - Siempre explicar que NO afectan el score
   - Mostrar evidencia específica
   - Permitir expandir/colapsar detalles

3. **Jerarquía Visual**:
   - Flags informativos después de penalizaciones
   - Separación clara entre "afecta score" y "solo informa"
   - Diseño consistente en todos los modos (Dashboard, Express, Reading)

4. **Adaptación por Modo**:
   - **Dashboard**: Sección expandible con detalles completos
   - **Express**: Badge compacto con modal al tocar
   - **Reading**: Texto completo, sin colapsar, alto contraste

---

### Componentes Nuevos Necesarios

1. **`InformativeFlags.astro`**
   - Componente principal para mostrar flags
   - Soporte para todas las categorías
   - **Adaptación por modo**:
     - Dashboard: Sección expandible con grid de flags
     - Express: Badge compacto + modal
     - Reading: Lista completa de texto

2. **`FlagCard.astro`**
   - Tarjeta individual para cada flag
   - **Adaptación por modo**:
     - Dashboard: Card expandible/colapsable
     - Express: Card compacta con icono
     - Reading: Texto completo, sin colapsar
   - Muestra evidencia

3. **`BonusBadge.astro`**
   - Badge para mostrar bonos recibidos
   - **Adaptación por modo**:
     - Dashboard: Badge con tooltip
     - Express: Badge compacto con emoji
     - Reading: Texto descriptivo completo
   - Tooltip explicativo

4. **`ViabilityAlert.astro`**
   - Alerta para violaciones constitucionales
   - **Adaptación por modo**:
     - Dashboard: Alerta expandible
     - Express: Badge compacto
     - Reading: Texto completo con explicación
   - Diferencia entre penalización y flag informativo

---

## 🎨 Estilos CSS Necesarios

```css
/* Flags Informativos */
.informative-flags-section {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 2px solid #bae6fd;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.flag-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-left: 4px solid #06b6d4;
}

.flag-card.high-severity {
  border-left-color: #f59e0b;
}

.flag-card.medium-severity {
  border-left-color: #3b82f6;
}

/* Bonos */
.bonus-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: #dcfce7;
  color: #15803d;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.bonus-section {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 0.75rem;
  padding: 1rem;
  margin-top: 1rem;
}

/* Violaciones Constitucionales */
.viability-alert {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #fef2f2;
  border-left: 4px solid #ef4444;
  border-radius: 0.5rem;
  margin-top: 0.75rem;
}
```

---

## 📊 Priorización de Implementación

### Fase 1: Crítico (Semana 1)
1. ✅ Actualizar tipos TypeScript
2. ✅ Crear componente `InformativeFlags.astro`
3. ✅ Mostrar flags en página de candidato
4. ✅ Actualizar funciones de datos

### Fase 2: Importante (Semana 2)
1. ✅ Mostrar múltiples propuestas correctamente
2. ✅ Mostrar bonos en página de candidato
3. ✅ Mostrar violaciones constitucionales
4. ✅ Integrar flags en comparación

### Fase 3: Mejoras (Semana 3)
1. ✅ Mejorar UX de flags informativos
2. ✅ Agregar tooltips explicativos
3. ✅ Optimizar para móviles
4. ✅ Agregar animaciones sutiles

---

## ✅ Checklist de Implementación

### Tipos y Datos
- [ ] Actualizar `types.ts` con nuevos tipos
- [ ] Agregar funciones en `data.ts`
- [ ] Verificar que datos se cargan correctamente

### Componentes
- [ ] Crear `InformativeFlags.astro`
- [ ] Crear `FlagCard.astro`
- [ ] Crear `BonusBadge.astro`
- [ ] Crear `ViabilityAlert.astro`

### Páginas (adaptado a 3 modos)
- [ ] Actualizar `/candidatos/[id].astro`:
  - [ ] Sección Dashboard Mode
  - [ ] Sección Express Mode
  - [ ] Sección Reading Mode
- [ ] Actualizar `/comparar.astro`:
  - [ ] Tabla Dashboard Mode
  - [ ] Cards Express Mode
  - [ ] Tabla Reading Mode
- [ ] Actualizar `/pilares/[id].astro`:
  - [ ] Grid Dashboard Mode
  - [ ] Cards Express Mode
  - [ ] Lista Reading Mode
- [ ] Actualizar `/ranking.astro`:
  - [ ] Tabla Dashboard Mode
  - [ ] Swiper Express Mode
  - [ ] Lista Reading Mode

### Estilos
- [ ] Agregar estilos para flags informativos
- [ ] Agregar estilos para bonos
- [ ] Agregar estilos para violaciones
- [ ] Responsive design

### Testing (por modo)
- [ ] **Dashboard Mode**:
  - [ ] Flags informativos se muestran correctamente
  - [ ] Bonos visibles en sección de pilares
  - [ ] Múltiples propuestas se muestran
  - [ ] Responsive en desktop/tablet/móvil
- [ ] **Express Mode**:
  - [ ] Badges compactos funcionan
  - [ ] Modales se abren correctamente
  - [ ] Swipe no interfiere con flags
  - [ ] Performance en móviles
- [ ] **Reading Mode**:
  - [ ] Texto completo legible
  - [ ] Alto contraste mantenido
  - [ ] Sin elementos colapsables
  - [ ] Accesibilidad (screen readers)
- [ ] **General**:
  - [ ] Verificar neutralidad visual
  - [ ] Verificar que no afecta performance
  - [ ] Verificar consistencia entre modos

---

## 📝 Notas Importantes

1. **Neutralidad**: Los flags informativos NO deben ser alarmantes. Son información objetiva para que el ciudadano decida.

2. **Performance**: Verificar que cargar múltiples propuestas y flags no afecte el rendimiento.

3. **Accesibilidad**: Asegurar que los flags sean accesibles (ARIA labels, contraste, etc.).

4. **Consistencia entre Modos**: 
   - Misma información en los 3 modos
   - Adaptación visual apropiada por modo
   - No perder funcionalidad al cambiar de modo

5. **Estructura de Código**:
   - Cada página debe tener 3 secciones: `.mode-dashboard-content`, `.mode-express-content`, `.mode-reading-content`
   - Usar CSS con `html[data-mode="..."]` para mostrar/ocultar
   - Componentes deben aceptar prop `mode` para adaptarse

6. **Ejemplo de Estructura**:
```astro
<!-- Dashboard Mode -->
<div class="mode-dashboard-content">
  <!-- Contenido completo con detalles -->
</div>

<!-- Express Mode -->
<div class="mode-express-content">
  <!-- Contenido compacto y visual -->
</div>

<!-- Reading Mode -->
<div class="mode-reading-content">
  <!-- Contenido de texto completo -->
</div>
```

---

**Fecha**: 2026-01-11  
**Versión**: v7.0  
**Estado**: Pendiente de implementación
