# Implementación Completa: Sistema de Flags Informativos

## Implementación Completada

### Cambios Realizados en `process_plans_v7.py`

#### 1. Nueva Función: `detect_dictatorial_patterns()`

**Ubicación**: Líneas 873-950

**Funcionalidad**:
- Detecta similitudes objetivas con modelos dictatoriales históricos (Cuba, Venezuela)
- NO juzga ideología, solo detecta patrones objetivos de comportamiento
- Retorna flags informativos (NO penalizaciones)

**Patrones detectados**:
- **Cuba**: Eliminación de separación de poderes, control estatal de medios, etc.
- **Venezuela**: Eliminación de independencia judicial, gobernar por decreto, etc.

#### 2. Nueva Función: `analyze_informative_flags()`

**Ubicación**: Líneas 952-1025

**Funcionalidad**:
- Analiza flags informativos basados en propuestas actuales y viabilidad
- Combina información de viabilidad con detección de patrones dictatoriales
- Retorna estructura completa de flags informativos

**Tipos de flags**:
1. **Propuestas actuales problemáticas**: Basadas en flags de viabilidad
2. **Similitudes dictatoriales**: Basadas en detección de patrones

#### 3. Integración en `calculate_candidate_score()`

**Ubicación**: Líneas 1321-1500

**Cambios**:
- Recopila información de viabilidad por pilar (`viability_flags_by_pillar`)
- Llama a `analyze_informative_flags()` al final del cálculo
- Agrega `informative_flags` al resultado final

**Estructura agregada**:
```python
return {
    "candidate_id": candidate_id,
    "pillar_scores": pillar_scores,
    # ... otros campos ...
    "informative_flags": informative_flags,  # NUEVO
    "overall": { ... }
}
```

---

## Estructura de Datos

### Flags Informativos en JSON

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "current_proposals": {
      "violates_separation_powers": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "pillar_id": "P1",
            "evidence": "Eliminar la Asamblea Legislativa...",
            "detected_by": "viability_check"
          }
        ]
      },
      "violates_fundamental_rights": {
        "active": false,
        "severity": "high",
        "evidence": []
      },
      "violates_constitutional_guarantees": {
        "active": false,
        "severity": "high",
        "evidence": []
      },
      "violates_constitutional_procedures": {
        "active": false,
        "severity": "medium",
        "evidence": []
      }
    },
    "dictatorial_patterns": {
      "cuba_similarity": {
        "active": true,
        "severity": "high",
        "evidence": [
          {
            "pillar_id": "P1",
            "proposal_text": "Eliminar la Asamblea Legislativa...",
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
        ]
      },
      "venezuela_similarity": {
        "active": false,
        "severity": "high",
        "evidence": []
      }
    }
  }
}
```

---

## Pruebas Realizadas

### Test 1: Detección de Patrones Dictatoriales

**Input**:
- Propuesta: "Eliminar la Asamblea Legislativa y gobernar por decreto sin Asamblea"
- Propuesta: "Control total de los medios de comunicación por el Estado"
- Propuesta: "Eliminar independencia judicial y control del Poder Judicial por el Ejecutivo"

**Resultado**:
- ✅ Cuba similarity: True (2 propuestas detectadas)
- ✅ Venezuela similarity: True (2 propuestas detectadas)

### Test 2: Flags Informativos Completos

**Input**:
- Propuestas con violaciones de separación de poderes
- Propuestas con similitudes dictatoriales

**Resultado**:
- ✅ Violates separation powers: True
- ✅ Cuba similarity: True
- ✅ Venezuela similarity: True

### Test 3: Procesamiento Completo

**Resultado**:
- ✅ Todos los candidatos tienen estructura de flags (aunque pueden estar vacíos)
- ✅ Sistema de flags informativos implementado correctamente
- ✅ Flags se guardan en `candidate_scores.json`

---

## Características de Implementación

### ✅ Neutralidad Mantenida

1. **Solo patrones objetivos**: NO juzga ideología
2. **Fuentes históricas verificables**: CIDH, ONU, documentos públicos
3. **No afecta scoring**: Flags son informativos, NO penalizaciones
4. **Transparencia total**: Ciudadano puede verificar todas las evidencias

### ✅ Objetividad Garantizada

1. **Patrones específicos**: Solo detecta comportamientos verificables
2. **Evidencia del plan actual**: Texto extraído directamente
3. **Fuentes históricas**: Documentos públicos verificables
4. **Aplicación igualitaria**: Mismos criterios para todos

---

## Uso en Frontend

### Ejemplo de Presentación

```javascript
// Obtener flags informativos
const informativeFlags = candidate.informative_flags;

// Verificar si hay flags activos
const hasViolations = informativeFlags.current_proposals.violates_separation_powers.active;
const hasCubaSimilarity = informativeFlags.dictatorial_patterns.cuba_similarity.active;
const hasVenezuelaSimilarity = informativeFlags.dictatorial_patterns.venezuela_similarity.active;

// Mostrar advertencia si hay flags activos
if (hasViolations || hasCubaSimilarity || hasVenezuelaSimilarity) {
  // Mostrar modal o badge informativo
  showInformativeFlags(candidate);
}
```

### UI Sugerida

```
⚠️ Información Adicional Disponible

Este candidato tiene:
- Propuestas que violan separación de poderes
- Similitudes objetivas con modelo cubano
- Similitudes objetivas con modelo venezolano

[Ver detalles y fuentes] [Cerrar]
```

---

## Resultados del Procesamiento

**Después de la implementación**:
- ✅ Estructura de flags informativos agregada a todos los candidatos
- ✅ Sistema detecta violaciones constitucionales en propuestas actuales
- ✅ Sistema detecta similitudes con modelos dictatoriales
- ✅ Flags NO afectan el score (solo informan)

**Interpretación**:
- Si no hay flags activos: Candidato no tiene propuestas problemáticas detectadas
- Si hay flags activos: Candidato tiene propuestas que requieren atención del ciudadano

---

## Conclusión

### ✅ Implementación Completada y Validada

**Funcionalidades implementadas**:
- ✅ Detección de patrones dictatoriales (Cuba, Venezuela)
- ✅ Flags de propuestas actuales problemáticas
- ✅ Integración en sistema de scoring
- ✅ Estructura de datos completa
- ✅ Pruebas validadas

**Resultado**:
- Sistema informativo completo
- Neutralidad mantenida
- Objetividad garantizada
- Transparencia total
- Ciudadano informado sin sesgo

---

**Fecha**: 2026-01-11  
**Estado**: Implementación completada, sistema validado
