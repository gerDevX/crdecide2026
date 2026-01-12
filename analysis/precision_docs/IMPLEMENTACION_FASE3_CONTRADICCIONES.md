# Implementación: Fase 3 - Sistema de Contradicciones Histórico-Actual

## Implementación Completada

### Nueva Funcionalidad Agregada

**Sistema de detección de contradicciones**: Detecta patrones consistentes entre evidencia histórica y propuestas actuales.

**Objetivo**: Alertar sobre candidatos que tienen tanto evidencia histórica problemática como propuestas actuales problemáticas, indicando un patrón consistente.

---

## Cambios Realizados en `process_plans_v7.py`

### Nueva Función: `detect_historical_current_contradictions()`

**Ubicación**: Líneas 1310-1380

**Funcionalidad**:
- Detecta contradicciones entre evidencia histórica y propuestas actuales
- Identifica patrones consistentes de comportamiento problemático
- Retorna flags informativos (NO penalizaciones)

**Tipos de contradicciones detectadas**:

#### 1. Contradicción Histórico-Actual
- **Condición**: Evidencia histórica anti-democrática + Propuestas actuales que violan principios constitucionales
- **Flag**: `historical_current_contradiction`
- **Severidad**: Alta
- **Descripción**: Patrón consistente de comportamiento no democrático

#### 2. Preocupación Corrupción-Transparencia
- **Condición**: Evidencia histórica de corrupción + Propuestas actuales problemáticas
- **Flag**: `corruption_transparency_concern`
- **Severidad**: Media
- **Descripción**: Preocupación sobre transparencia y rendición de cuentas

#### 3. Histórico Problemático + Similitudes Dictatoriales
- **Condición**: Evidencia histórica problemática + Similitudes con modelos dictatoriales en propuestas actuales
- **Flag**: `historical_current_contradiction` (mismo flag, diferente evidencia)
- **Severidad**: Alta
- **Descripción**: Patrón consistente de comportamiento problemático

---

## Estructura de Datos

### Flags de Contradicciones en JSON

```json
{
  "candidate_id": "ejemplo-candidato",
  "informative_flags": {
    "contradictions": {
      "historical_current_contradiction": {
        "active": true,
        "severity": "high",
        "evidence": {
          "historical": "Comportamiento anti-democrático histórico verificable",
          "current": "Propuestas actuales que violan principios constitucionales",
          "pattern": "Patrón consistente de comportamiento no democrático"
        },
        "description": "Patrón consistente: evidencia histórica problemática + propuestas actuales problemáticas"
      },
      "corruption_transparency_concern": {
        "active": false,
        "severity": "medium",
        "evidence": {
          "historical": null,
          "current": null,
          "pattern": null
        },
        "description": "Evidencia histórica de corrupción + propuestas actuales sin mecanismos de transparencia"
      }
    }
  }
}
```

---

## Pruebas Realizadas

### Test 1: Contradicción Histórico-Actual

**Input**:
- Histórico: Comportamiento anti-democrático (True)
- Actual: Viola separación de poderes (True)

**Resultado**: ✅ `historical_current_contradiction`: True

### Test 2: Preocupación Corrupción-Transparencia

**Input**:
- Histórico: Corrupción verificada (True)
- Actual: Propuestas problemáticas (True)

**Resultado**: ✅ `corruption_transparency_concern`: True

### Test 3: Sin Contradicciones

**Input**:
- Histórico: Sin evidencia problemática
- Actual: Sin propuestas problemáticas

**Resultado**: ✅ Ambos flags: False

---

## Algoritmo de Detección

### Lógica de Contradicciones

```python
# Contradicción 1: Histórico anti-democrático + Propuestas actuales problemáticas
if (has_historical_anti_democratic AND has_current_violations):
    → Flag: historical_current_contradiction (Alta severidad)

# Contradicción 2: Histórico corrupto + Propuestas actuales problemáticas
if (has_historical_corruption AND has_current_violations):
    → Flag: corruption_transparency_concern (Media severidad)

# Contradicción 3: Histórico problemático + Similitudes dictatoriales
if (has_historical_issues AND has_dictatorial_similarities):
    → Flag: historical_current_contradiction (Alta severidad)
```

---

## Ejemplo de Uso

### Caso: Candidato con Contradicción

**Evidencia histórica**:
- Comportamiento anti-democrático verificable (2020)

**Propuestas actuales**:
- "Eliminar la Asamblea Legislativa"
- "Gobernar por decreto sin Asamblea"

**Contradicción detectada**:
- ✅ `historical_current_contradiction`: True
- Evidencia histórica: "Comportamiento anti-democrático histórico verificable"
- Evidencia actual: "Propuestas actuales que violan principios constitucionales"
- Patrón: "Patrón consistente de comportamiento no democrático"

**Presentación al ciudadano**:
```
⚠️ Información Adicional

Este candidato muestra un patrón consistente:

📋 Contradicción Detectada:
├─ Histórico: Comportamiento anti-democrático verificable (2020)
└─ Actual: Propuestas que violan separación de poderes

⚠️ Patrón consistente de comportamiento no democrático

[Ver detalles] [Cerrar]
```

**Score**: NO se afecta (solo informa)

---

## Características de Implementación

### ✅ Neutralidad Mantenida

1. **Solo patrones objetivos**: Detecta consistencia entre histórico y actual
2. **No juzga ideología**: Solo detecta comportamientos verificables
3. **No penaliza**: Flags son informativos, NO afectan scoring
4. **Transparencia total**: Ciudadano puede verificar todas las evidencias

### ✅ Utilidad para el Ciudadano

**Información valiosa**:
- Patrones consistentes de comportamiento problemático
- Evidencia histórica combinada con propuestas actuales
- Alertas sobre riesgos de deterioro democrático

**Ayuda a entender**:
- Consistencia en comportamiento problemático
- Riesgos de implementación de propuestas problemáticas
- Necesidad de vigilancia ciudadana

---

## Resultados del Procesamiento

**Después de la implementación**:
- ✅ Estructura de flags de contradicciones agregada a todos los candidatos
- ✅ Sistema detecta contradicciones correctamente
- ✅ Flags NO afectan el score (solo informan)

**Estado actual**:
- Ningún candidato tiene contradicciones detectadas (normal si no hay evidencia histórica + propuestas problemáticas simultáneamente)
- Sistema listo para detectar contradicciones cuando existan

---

## Conclusión

### ✅ Fase 3 Implementada y Validada

**Funcionalidades implementadas**:
- ✅ Detección de contradicciones histórico-actual
- ✅ Detección de preocupaciones corrupción-transparencia
- ✅ Integración en sistema de flags informativos
- ✅ Pruebas validadas

**Resultado**:
- Sistema informativo completo
- Neutralidad mantenida (solo patrones objetivos)
- Utilidad para ciudadano (patrones consistentes)
- Transparencia total

---

**Fecha**: 2026-01-11  
**Estado**: Fase 3 implementada, sistema completo
