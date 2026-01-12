# Implementación: Flags de Similitud con Modelos Dictatoriales

## Objetivo

Detectar similitudes **objetivas** entre propuestas actuales y patrones históricamente verificables de modelos dictatoriales, **sin juzgar ideología política**.

---

## Principios de Neutralidad

### ✅ Lo Que SÍ Detectamos (Objetivo)

**Patrones objetivos de comportamiento**:
- Eliminación de separación de poderes
- Eliminación de libertades fundamentales
- Eliminación de garantías constitucionales
- Concentración de poderes en Ejecutivo

### ❌ Lo Que NO Detectamos (Subjetivo)

**Ideología política**:
- ❌ "Socialismo" = dictadura
- ❌ "Capitalismo" = democracia
- ❌ Posiciones económicas
- ❌ Modelos de gobierno legítimos

---

## Patrones Históricamente Verificables

### Modelo Cubano (Patrones Objetivos)

**Fuentes históricas verificables**:
- Resoluciones de CIDH
- Informes de ONU
- Documentos históricos públicos

**Patrones objetivos detectables**:
1. ✅ Eliminación de separación de poderes
2. ✅ Eliminación de libertad de prensa
3. ✅ Eliminación de garantías constitucionales
4. ✅ Concentración de poderes en Ejecutivo

**Ejemplos históricos verificables**:
- Eliminación de Asamblea Legislativa independiente
- Control estatal de medios de comunicación
- Eliminación de garantías procesales
- Concentración de poder en Ejecutivo

### Modelo Venezolano (Patrones Objetivos)

**Fuentes históricas verificables**:
- Resoluciones de CIDH
- Sentencias de Corte Interamericana
- Informes de ONU

**Patrones objetivos detectables**:
1. ✅ Eliminación de independencia judicial
2. ✅ Gobernar por decreto sin Asamblea
3. ✅ Eliminación de libertad de expresión
4. ✅ Concentración de poderes en Ejecutivo

**Ejemplos históricos verificables**:
- Control del Poder Judicial por Ejecutivo
- Gobernanza por decreto sin Asamblea
- Cierre de medios de comunicación
- Concentración de poder en Ejecutivo

---

## Implementación Técnica

### Función de Detección

```python
def detect_dictatorial_patterns(proposals: List[Dict]) -> Dict:
    """
    Detecta similitudes objetivas con modelos dictatoriales históricos.
    
    NO juzga ideología, solo detecta patrones objetivos de comportamiento.
    """
    patterns = {
        "cuba_similarity": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "historical_sources": [
                "Resoluciones CIDH",
                "Informes ONU",
                "Documentos históricos verificables"
            ]
        },
        "venezuela_similarity": {
            "active": False,
            "severity": "high",
            "evidence": [],
            "historical_sources": [
                "Resoluciones CIDH",
                "Sentencias Corte Interamericana",
                "Informes ONU"
            ]
        }
    }
    
    # Patrones objetivos de Cuba (históricamente verificables)
    # NOTA: Solo patrones de comportamiento, NO ideología
    CUBA_PATTERNS = [
        r"eliminar.*separación\s+de\s+poderes",
        r"eliminar.*asamblea\s+legislativa",
        r"eliminar.*libertad\s+de\s+prensa",
        r"control.*estatal.*medios",
        r"eliminar.*garantías\s+constitucionales",
        r"concentración\s+de\s+poderes.*ejecutivo",
        r"ejecutivo.*legislativo",
    ]
    
    # Patrones objetivos de Venezuela (históricamente verificables)
    # NOTA: Solo patrones de comportamiento, NO ideología
    VENEZUELA_PATTERNS = [
        r"eliminar.*independencia\s+judicial",
        r"control.*poder\s+judicial.*ejecutivo",
        r"gobernar\s+por\s+decreto\s+sin\s+asamblea",
        r"eliminar.*libertad\s+de\s+expresión",
        r"cerrar.*medios\s+de\s+comunicación",
        r"concentración\s+de\s+poderes.*ejecutivo",
        r"asamblea\s+constituyente.*sin\s+asamblea",
    ]
    
    for proposal in proposals:
        text_lower = proposal.get("text", "").lower()
        if not text_lower:
            continue
        
        # Detectar similitudes con Cuba
        cuba_matches = []
        for pattern in CUBA_PATTERNS:
            if re.search(pattern, text_lower):
                cuba_matches.append(pattern)
        
        if cuba_matches:
            patterns["cuba_similarity"]["active"] = True
            patterns["cuba_similarity"]["evidence"].append({
                "pillar_id": proposal.get("pillar_id", "unknown"),
                "proposal_text": proposal.get("text", "")[:200],
                "matched_patterns": cuba_matches,
                "detection_method": "pattern_matching"
            })
        
        # Detectar similitudes con Venezuela
        venezuela_matches = []
        for pattern in VENEZUELA_PATTERNS:
            if re.search(pattern, text_lower):
                venezuela_matches.append(pattern)
        
        if venezuela_matches:
            patterns["venezuela_similarity"]["active"] = True
            patterns["venezuela_similarity"]["evidence"].append({
                "pillar_id": proposal.get("pillar_id", "unknown"),
                "proposal_text": proposal.get("text", "")[:200],
                "matched_patterns": venezuela_matches,
                "detection_method": "pattern_matching"
            })
    
    return patterns
```

### Integración en Sistema de Flags

```python
def analyze_democratic_flags(
    candidate_id: str,
    historical_evidence: Dict,
    current_proposals: List[Dict]
) -> Dict:
    """
    Analiza flags informativos incluyendo similitudes con modelos dictatoriales.
    """
    flags = {
        "historical": {},
        "current_proposals": {},
        "contradictions": {},
        "dictatorial_patterns": {}  # NUEVO
    }
    
    # ... código existente ...
    
    # 4. Detectar similitudes con modelos dictatoriales (NUEVO)
    dictatorial_patterns = detect_dictatorial_patterns(current_proposals)
    flags["dictatorial_patterns"] = dictatorial_patterns
    
    return flags
```

---

## Estructura de Datos

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "dictatorial_patterns": {
      "cuba_similarity": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "pillar_id": "P1",
            "proposal_text": "Eliminar la Asamblea Legislativa y gobernar por decreto...",
            "matched_patterns": [
              "eliminar.*asamblea\\s+legislativa",
              "concentración\\s+de\\s+poderes.*ejecutivo"
            ],
            "detection_method": "pattern_matching"
          }
        ],
        "historical_sources": [
          "Resoluciones CIDH",
          "Informes ONU",
          "Documentos históricos verificables"
        ],
        "summary": "Similitudes objetivas con patrones históricamente verificables del modelo cubano"
      },
      "venezuela_similarity": {
        "active": false,
        "evidence": []
      }
    }
  }
}
```

---

## Presentación al Ciudadano (Neutral)

### Ejemplo de UI

```
⚠️ Información Adicional

Este candidato tiene propuestas que muestran similitudes objetivas 
con patrones históricamente verificables de modelos dictatoriales:

📋 Similitudes Detectadas:

├─ 🇨🇺 Cuba: Eliminación de separación de poderes
│  └─ Evidencia: "Eliminar la Asamblea Legislativa..."
│  └─ Fuente: Plan de gobierno actual
│  └─ Patrones históricos: Resoluciones CIDH, Informes ONU
│
└─ 🇻🇪 Venezuela: Concentración de poderes en Ejecutivo
   └─ Evidencia: "Gobernar por decreto sin Asamblea..."
   └─ Fuente: Plan de gobierno actual
   └─ Patrones históricos: Sentencias Corte Interamericana

⚠️ NOTA IMPORTANTE:
Esta información se basa en patrones objetivos de comportamiento
históricamente verificables, NO en ideología política.

El objetivo es alertar sobre riesgos de deterioro democrático basado
en evidencia objetiva y verificable.

[Ver fuentes históricas] [Ver propuestas completas] [Cerrar]
```

### Características de Presentación

1. **Lenguaje neutral**:
   - "Similitudes objetivas" (no "es como Cuba")
   - "Patrones históricamente verificables" (no "modelo dictatorial")
   - "Riesgos de deterioro democrático" (no "dictadura")

2. **Transparencia total**:
   - Muestra evidencia del plan actual
   - Muestra fuentes históricas
   - Permite verificación

3. **No afecta scoring**:
   - Claramente marcado como "información"
   - No se resta del score
   - Ciudadano decide

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
- ❌ Incluir solo ciertos modelos
- ❌ Presentar información de forma diferente
- ❌ Usar lenguaje sesgado

**SÍ hacer**:
- ✅ Detectar solo patrones objetivos
- ✅ Aplicar a todos los candidatos
- ✅ Presentar de forma idéntica
- ✅ Usar lenguaje neutral y objetivo

---

## Ejemplo de Uso

### Caso: Candidato con Propuestas Problemáticas

**Propuestas actuales**:
- "Eliminar la Asamblea Legislativa"
- "Gobernar por decreto sin Asamblea"
- "Suspender libertad de expresión"

**Detección**:
1. ✅ Viola separación de poderes (sistema actual)
2. ✅ Viola derechos fundamentales (sistema actual)
3. ✅ Similitud con Cuba: Eliminación de separación de poderes
4. ✅ Similitud con Venezuela: Concentración de poderes

**Presentación**:
```
⚠️ Información Adicional

Similitudes objetivas detectadas:
- Cuba: Eliminación de separación de poderes
- Venezuela: Concentración de poderes en Ejecutivo

NOTA: Basado en patrones objetivos verificables históricamente,
NO en ideología política.

[Ver detalles] [Cerrar]
```

**Score**: NO se afecta (solo informa)

---

## Conclusión

### ✅ Neutralidad Mantenida

**Implementación**:
- ✅ Solo patrones objetivos (NO ideología)
- ✅ Basado en hechos históricamente verificables
- ✅ Fuentes objetivas (CIDH, ONU)
- ✅ Presentación neutral
- ✅ No afecta scoring

**Resultado**:
- Ciudadano informado sobre riesgos objetivos
- Neutralidad mantenida
- Sin sesgo político
- Transparencia total

---

**Fecha**: 2026-01-11  
**Estado**: Propuesta lista para implementación
