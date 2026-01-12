# Análisis: Neutralidad y Sesgo en Sistema de Flags Informativos

## Pregunta del Usuario

1. ¿Mantenemos neutralidad y evitamos sesgo con esta propuesta?
2. ¿Cómo agregar modelos dictatoriales (Cuba, Venezuela) sin sesgo político?

---

## Análisis de Neutralidad

### ✅ Neutralidad Mantenida (Propuesta Actual)

**Razones**:

1. **Solo evidencia verificable**:
   - Sentencias judiciales (objetivas)
   - Resoluciones de organismos oficiales (objetivas)
   - Propuestas extraídas del plan actual (objetivas)

2. **No juzga ideología**:
   - NO penaliza posiciones ideológicas legítimas
   - NO juzga si algo es "bueno" o "malo" políticamente
   - Solo informa evidencia objetiva

3. **No afecta scoring**:
   - Flags son informativos, NO penalizaciones
   - Score se mantiene neutral
   - Ciudadano decide qué hacer con la información

4. **Transparencia total**:
   - Todas las fuentes son públicas
   - Todas las evidencias son verificables
   - Ciudadano puede verificar por sí mismo

### ⚠️ Riesgos de Sesgo (A Evitar)

**Riesgos identificados**:

1. **Sesgo en selección de evidencia histórica**:
   - ❌ Incluir solo evidencia de ciertos partidos
   - ✅ Incluir evidencia de TODOS los partidos/candidatos (si existe)

2. **Sesgo en interpretación de modelos dictatoriales**:
   - ❌ Juzgar ideología (ej: "socialismo = dictadura")
   - ✅ Detectar patrones objetivos de comportamiento (ej: "eliminar separación de poderes")

3. **Sesgo en presentación**:
   - ❌ Mostrar flags de forma diferente según partido
   - ✅ Mostrar flags de forma idéntica para todos

---

## Propuesta: Detección de Modelos Dictatoriales (Objetiva)

### Concepto

**NO juzgar ideología**, solo detectar **patrones objetivos de comportamiento** que coincidan con modelos dictatoriales históricamente verificables.

### Criterios Objetivos para Modelos Dictatoriales

#### Patrones Objetivos (NO Ideológicos)

**1. Eliminación de Separación de Poderes**:
- ✅ Objetivo: "Eliminar Asamblea Legislativa"
- ✅ Objetivo: "Gobernar por decreto sin Asamblea"
- ❌ Subjetivo: "Socialismo" (ideología)

**2. Eliminación de Libertades Fundamentales**:
- ✅ Objetivo: "Suspender libertad de expresión"
- ✅ Objetivo: "Eliminar libertad de prensa"
- ❌ Subjetivo: "Regulación de medios" (puede ser legítima)

**3. Eliminación de Garantías Constitucionales**:
- ✅ Objetivo: "Eliminar hábeas corpus"
- ✅ Objetivo: "Suspender garantías individuales"
- ❌ Subjetivo: "Seguridad nacional" (puede ser legítima)

**4. Concentración de Poderes**:
- ✅ Objetivo: "Ejecutivo legisla directamente"
- ✅ Objetivo: "Concentración de poderes en Ejecutivo"
- ❌ Subjetivo: "Gobierno fuerte" (puede ser legítima)

### Ejemplos Históricos Objetivos

#### Cuba (Patrones Objetivos Verificables)

**Patrones históricamente verificables** (NO ideología):
1. ✅ Eliminación de separación de poderes (hecho histórico)
2. ✅ Eliminación de libertad de prensa (hecho histórico)
3. ✅ Eliminación de garantías constitucionales (hecho histórico)
4. ✅ Concentración de poderes en Ejecutivo (hecho histórico)

**Fuentes objetivas**:
- Resoluciones de CIDH
- Informes de ONU
- Documentos históricos verificables

#### Venezuela (Patrones Objetivos Verificables)

**Patrones históricamente verificables** (NO ideología):
1. ✅ Eliminación de separación de poderes (hecho histórico)
2. ✅ Eliminación de independencia judicial (hecho histórico)
3. ✅ Eliminación de libertad de prensa (hecho histórico)
4. ✅ Concentración de poderes en Ejecutivo (hecho histórico)

**Fuentes objetivas**:
- Resoluciones de CIDH
- Sentencias de Corte Interamericana
- Informes de ONU

---

## Propuesta: Flags de Similitud con Modelos Dictatoriales

### Concepto

**Detectar similitudes objetivas** entre propuestas actuales y patrones históricamente verificables de modelos dictatoriales.

### Criterios Objetivos

**NO juzgar**:
- ❌ Ideología política
- ❌ Posiciones económicas
- ❌ Modelos de gobierno legítimos

**SÍ detectar**:
- ✅ Patrones objetivos de comportamiento
- ✅ Similitudes con modelos históricamente verificables
- ✅ Evidencia extraída del plan actual

### Algoritmo de Detección

```python
def detect_dictatorial_patterns(proposals: List[Dict]) -> Dict:
    """
    Detecta similitudes objetivas con modelos dictatoriales históricos.
    
    NO juzga ideología, solo detecta patrones objetivos.
    """
    patterns = {
        "cuba_similarity": {
            "active": False,
            "evidence": []
        },
        "venezuela_similarity": {
            "active": False,
            "evidence": []
        }
    }
    
    # Patrones objetivos de Cuba (históricamente verificables)
    CUBA_PATTERNS = [
        "eliminar separación de poderes",
        "eliminar asamblea legislativa",
        "eliminar libertad de prensa",
        "concentración de poderes en ejecutivo",
        "eliminar garantías constitucionales"
    ]
    
    # Patrones objetivos de Venezuela (históricamente verificables)
    VENEZUELA_PATTERNS = [
        "eliminar independencia judicial",
        "gobernar por decreto sin asamblea",
        "eliminar libertad de expresión",
        "concentración de poderes en ejecutivo",
        "eliminar separación de poderes"
    ]
    
    for proposal in proposals:
        text_lower = proposal["text"].lower()
        
        # Detectar similitudes con Cuba
        cuba_matches = [p for p in CUBA_PATTERNS if p in text_lower]
        if cuba_matches:
            patterns["cuba_similarity"]["active"] = True
            patterns["cuba_similarity"]["evidence"].append({
                "pillar_id": proposal["pillar_id"],
                "proposal_text": proposal["text"][:200],
                "matched_patterns": cuba_matches
            })
        
        # Detectar similitudes con Venezuela
        venezuela_matches = [p for p in VENEZUELA_PATTERNS if p in text_lower]
        if venezuela_matches:
            patterns["venezuela_similarity"]["active"] = True
            patterns["venezuela_similarity"]["evidence"].append({
                "pillar_id": proposal["pillar_id"],
                "proposal_text": proposal["text"][:200],
                "matched_patterns": venezuela_matches
            })
    
    return patterns
```

### Presentación al Ciudadano (Neutral)

**Ejemplo de presentación**:

```
⚠️ Información Adicional

Este candidato tiene propuestas que muestran similitudes objetivas 
con patrones históricamente verificables de modelos dictatoriales:

📋 Similitudes Detectadas:
├─ Cuba: Eliminación de separación de poderes
│  └─ Propuesta: "Eliminar Asamblea Legislativa..."
│  └─ Fuente: Plan de gobierno actual
│
└─ Venezuela: Concentración de poderes en Ejecutivo
   └─ Propuesta: "Gobernar por decreto sin Asamblea..."
   └─ Fuente: Plan de gobierno actual

NOTA: Esta información se basa en patrones objetivos de comportamiento,
NO en ideología política. Ver fuentes históricas →
```

**Características**:
- ✅ Menciona "patrones objetivos" (no ideología)
- ✅ Menciona "históricamente verificables"
- ✅ Muestra evidencia del plan actual
- ✅ NO juzga ideología política

---

## Garantías de Neutralidad

### ✅ Criterios Objetivos

1. **Solo patrones objetivos**:
   - Eliminación de instituciones (objetivo)
   - Violación de derechos (objetivo)
   - Concentración de poderes (objetivo)

2. **NO ideología**:
   - NO "socialismo" = dictadura
   - NO "capitalismo" = democracia
   - Solo patrones de comportamiento verificables

3. **Fuentes históricas verificables**:
   - Resoluciones de CIDH
   - Informes de ONU
   - Documentos históricos públicos

4. **Aplicación igualitaria**:
   - Mismos criterios para todos los candidatos
   - Misma presentación para todos
   - Misma transparencia para todos

### ⚠️ Evitar Sesgo

**NO hacer**:
- ❌ Juzgar ideología política
- ❌ Incluir solo ciertos partidos
- ❌ Presentar información de forma diferente
- ❌ Usar lenguaje sesgado

**SÍ hacer**:
- ✅ Detectar solo patrones objetivos
- ✅ Aplicar a todos los candidatos
- ✅ Presentar de forma idéntica
- ✅ Usar lenguaje neutral y objetivo

---

## Ejemplo de Implementación Neutral

### Caso: Candidato con Propuestas Problemáticas

**Propuestas actuales**:
- "Eliminar la Asamblea Legislativa"
- "Gobernar por decreto sin Asamblea"
- "Suspender libertad de expresión"

**Detección objetiva**:
1. ✅ Viola separación de poderes (sistema actual)
2. ✅ Viola derechos fundamentales (sistema actual)
3. ✅ Similitud con Cuba: Eliminación de separación de poderes
4. ✅ Similitud con Venezuela: Concentración de poderes

**Presentación neutral**:
```
⚠️ Información Adicional

Este candidato tiene propuestas que muestran similitudes objetivas 
con patrones históricamente verificables:

📋 Similitudes Detectadas:
├─ Cuba: Eliminación de separación de poderes
│  └─ Evidencia: "Eliminar la Asamblea Legislativa"
│
└─ Venezuela: Concentración de poderes en Ejecutivo
   └─ Evidencia: "Gobernar por decreto sin Asamblea"

NOTA: Esta información se basa en patrones objetivos de comportamiento
verificables históricamente, NO en ideología política.

[Ver fuentes históricas] [Ver propuestas completas]
```

**Score**: NO se afecta (solo informa)

---

## Conclusión

### ✅ Neutralidad Mantenida

**Razones**:
1. ✅ Solo evidencia objetiva y verificable
2. ✅ NO juzga ideología política
3. ✅ NO afecta scoring
4. ✅ Transparencia total
5. ✅ Aplicación igualitaria

### ✅ Modelos Dictatoriales (Objetivos)

**Implementación**:
1. ✅ Detectar solo patrones objetivos (NO ideología)
2. ✅ Basarse en hechos históricamente verificables
3. ✅ Usar fuentes objetivas (CIDH, ONU)
4. ✅ Presentar de forma neutral

**Resultado**:
- Ciudadano informado sobre riesgos objetivos
- Neutralidad mantenida
- Sin sesgo político
- Transparencia total

---

**Fecha**: 2026-01-11  
**Estado**: Análisis completado, propuesta neutral validada
